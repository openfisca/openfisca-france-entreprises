"""Annexe « Répartition des dépenses fiscales par mission et programme ».

Cette annexe redonne, indépendamment des fiches, la liste des dépenses fiscales
et — depuis le PLF 2022 — leur chiffrage pour l'année du PLF. Elle fournit donc
un **recoupement interne au document** : si la fiche et l'annexe donnent le même
montant pour le même numéro, l'extraction est vérifiée par une seconde source
plutôt que supposée correcte.

Disponibilité : absente du PLF 2020 ; présente sans montants au PLF 2021
(recoupement sur les seuls identifiants) ; avec montants de 2022 à 2025.
"""
from __future__ import annotations

import re

from .commun import RE_MONTANT, normalise_montant

# le titre du corps est en capitales et coupé avant « ET PROGRAMME » selon les
# millésimes ; celui du sommaire est en bas de casse et suivi d'un numéro de page.
TITRE = re.compile(r'(?i)r[ée]partition des d[ée]penses fiscales par mission')
PROGRAMME = re.compile(r'^\s{0,6}P\d{3}\s*[-–—]\s*\S')
MISSION_FIN = re.compile(r'Correspondance juridique des d[ée]penses fiscales')
# ligne de mesure : numéro, libellé, puis éventuellement un montant en fin de ligne
MESURE = re.compile(r'^\s{0,4}(\d{6})\s*(?:[-–—]\s*)?(.*?)\s*$')


def _debut(lignes: list[str]) -> int | None:
    """Première ligne du corps de l'annexe (après le renvoi de sommaire)."""
    titres = [i for i, l in enumerate(lignes) if TITRE.search(l)]
    for i in titres:
        for j in range(i + 1, min(i + 60, len(lignes))):
            if PROGRAMME.match(lignes[j]):
                return i
    return None


def _fin(lignes: list[str], debut: int) -> int:
    for i in range(debut, len(lignes)):
        if MISSION_FIN.search(lignes[i]) and i > debut + 20:
            return i
    return len(lignes)


def parse(lignes: list[str], plf: int) -> dict[str, dict]:
    """numéro -> {'montant', 'chiffrage', 'mission', 'programme'} pour l'année du PLF."""
    d = _debut(lignes)
    if d is None:
        return {}
    f = _fin(lignes, d)
    out: dict[str, dict] = {}
    mission = programme = ''
    for l in lignes[d:f]:
        if PROGRAMME.match(l):
            programme = l.strip()
            continue
        m = MESURE.match(l)
        if not m:
            s = l.strip()
            # un intitulé de mission est seul sur sa ligne, sans numéro ni montant
            if s and not RE_MONTANT.fullmatch(s) and len(s) > 3 and not s.isdigit():
                mission = s
            continue
        numero, reste = m.group(1), m.group(2)
        # le montant, s'il existe, ferme la ligne après au moins deux espaces
        mm = re.search(r'\s\s+(' + RE_MONTANT.pattern + r')\s*$', reste)
        brut = mm.group(1) if mm else None
        montant, chiffrage = normalise_montant(brut)
        # Une même mesure peut figurer sous plusieurs programmes : le chiffrage
        # n'est porté que par le rattachement à titre principal, les autres
        # occurrences ont une cellule vide. On ne laisse jamais une occurrence
        # muette écraser celle qui porte le montant.
        if numero in out and chiffrage == 'absent' and out[numero]['chiffrage'] != 'absent':
            continue
        out[numero] = dict(montant=montant, chiffrage=chiffrage,
                           mission=mission, programme=programme)
    return out


def recoupement(fiches: list[dict], annexe: dict[str, dict], plf: int) -> dict:
    """Confronte le montant de l'année du PLF, fiche contre annexe."""
    par_num = {f['numero']: f for f in fiches
               if f.get('annee') == plf and f.get('numero')}
    if not annexe:
        return dict(plf=plf, disponible=False)

    manquants_annexe = sorted(set(par_num) - set(annexe))
    manquants_fiches = sorted(set(annexe) - set(par_num))

    compares = accords = 0
    desaccords = []
    for num, a in annexe.items():
        f = par_num.get(num)
        if f is None or a['chiffrage'] == 'absent':
            continue
        compares += 1
        if f['montant'] == a['montant'] and f['chiffrage'] == a['chiffrage']:
            accords += 1
        else:
            desaccords.append(dict(plf=plf, numero=num, fiche=f['montant'],
                                   fiche_chiffrage=f['chiffrage'], annexe=a['montant'],
                                   annexe_chiffrage=a['chiffrage'],
                                   libelle=f['libelle'][:80]))
    return dict(plf=plf, disponible=True, n_annexe=len(annexe), compares=compares,
                accords=accords, desaccords=desaccords,
                absents_annexe=manquants_annexe, absents_fiches=manquants_fiches)
