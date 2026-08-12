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
#: mobilier de page de l'annexe, à écarter en lecture `raw` où il se retrouve
#: mêlé aux données faute de géométrie
MOBILIER = re.compile(r"(?i)^(\d{1,3}\s+)?Annexe au PLF|^\(en millions|"
                      r"^Num[ée]ro D[ée]pense fiscale|^Avertissement$|"
                      r"^Les listes suivantes|^titre principal|^subsidiaire\.?$")


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


def parse_raw(lignes: list[str], plf: int) -> dict[str, dict]:
    """Même annexe, lue dans l'ordre de lecture du PDF (`pdftotext -raw`).

    La mise en page y disparaît : chaque mesure se présente comme un numéro
    suivi de son libellé sur une ou plusieurs lignes, puis le chiffrage seul sur
    sa ligne. C'est la seule lecture exploitable des millésimes où `-layout`
    éclate le tableau en colonnes désynchronisées.
    """
    d = _debut(lignes)
    if d is None:
        return {}
    f = _fin(lignes, d)

    # Le mobilier de page — titre courant, unité, en-tête de colonnes et le
    # millésime seul sur sa ligne — doit disparaître avant toute lecture : ce
    # dernier ressemble trait pour trait à un chiffrage.
    utiles = [l.strip() for l in lignes[d:f]
              if l.strip() and not MOBILIER.search(l) and l.strip() != str(plf)]

    # découpage en blocs : un bloc commence à une ligne de mesure
    out: dict[str, dict] = {}
    mission = programme = ''
    bloc: list[str] = []
    numero = None

    def clore():
        if numero is None:
            return
        # le chiffrage est soit seul sur une ligne du bloc, soit collé en fin de
        # la ligne d'ouverture quand le libellé y tenait tout entier
        seuls = [s for s in bloc[1:] if RE_MONTANT.fullmatch(s)]
        if seuls:
            brut = seuls[-1]
        else:
            m = re.search(r'\s(' + RE_MONTANT.pattern + r')$', bloc[0])
            brut = m.group(1) if m else None
        montant, chiffrage = normalise_montant(brut)
        if numero not in out or out[numero]['chiffrage'] == 'absent':
            out[numero] = dict(montant=montant, chiffrage=chiffrage,
                               mission=mission, programme=programme)

    for s in utiles:
        m = re.match(r'^(\d{6})\s+(\S.*)$', s)
        if m:
            clore()
            numero, bloc = m.group(1), [m.group(2)]
            continue
        if PROGRAMME.match(s):
            clore()
            numero, bloc, programme = None, [], s
            continue
        if numero is not None:
            bloc.append(s)
        elif len(s) > 3 and not RE_MONTANT.fullmatch(s):
            mission = s
    clore()
    return out


#: En deçà de cette part de mesures chiffrées, on considère que l'annexe ne
#: publie pas de montants — c'est le cas au PLF 2021 — plutôt que de croire les
#: quelques valeurs isolées qu'une lecture opportuniste finit toujours par
#: trouver. Le recoupement se replie alors sur les seuls identifiants.
SEUIL_CHIFFRAGE = 0.5


def parse_meilleure(lignes_layout: list[str], lignes_raw: list[str], plf: int):
    """Retient la lecture qui chiffre le plus de mesures, et dit laquelle.

    Les deux extractions se valent sur la plupart des millésimes ; le critère de
    choix est objectif et vérifiable — la part de mesures dotées d'un chiffrage —
    plutôt qu'une liste de millésimes codée en dur.
    """
    candidats = {'layout': parse(lignes_layout, plf), 'raw': parse_raw(lignes_raw, plf)}

    def chiffrees(t):
        return sum(1 for v in t.values() if v['chiffrage'] != 'absent')

    mode = max(candidats, key=lambda k: chiffrees(candidats[k]))
    table = candidats[mode]
    if not table:
        return table, mode
    if chiffrees(table) < SEUIL_CHIFFRAGE * len(table):
        for v in table.values():
            v['montant'], v['chiffrage'] = None, 'absent'
        return table, mode + ' (sans montants)'
    return table, mode


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
