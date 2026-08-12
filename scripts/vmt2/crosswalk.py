"""Suivi des identifiants de dépenses fiscales d'un millésime à l'autre.

Les numéros à six chiffres sont stables la plupart du temps, mais pas toujours :
le tome II les renumérote, en classe de nouveaux, en déclasse d'autres, et il
lui arrive d'éclater une dépense en plusieurs. Sans crosswalk, une série longue
mélange des périmètres — la 800210 passe de 903 M€ à 8 M€ entre le PLF 2020 et
le PLF 2021 non pas parce que son coût s'est effondré, mais parce que le gaz et
les charbons en ont été sortis pour former les 830201 et 840201.

Ce module lit ce que le document publie lui-même en sous-partie III « Évolution
depuis le précédent PLF », disponible à partir du PLF 2009. Il ne devine rien :
les entrées et sorties d'identifiants qu'aucune table ne justifie sont écrites
telles quelles dans `mouvements.csv` avec la mention `inexplique`, pour
arbitrage humain.
"""
from __future__ import annotations

import csv
import os
import re

from .commun import DEPENSE_FISCALE, REGIMES, SOURCES, texte

NUM = re.compile(r'\b(\d{6})\b')

TITRE_RENUM = re.compile(r'(?i)reclassement de d[ée]penses fiscales par renum[ée]rotation')
AUCUNE_RENUM = re.compile(r'(?i)aucun(e)? (reclassement par )?renum[ée]rotation')
TITRE_CLASS = re.compile(r'(?i)d[ée]penses fiscales class[ée]es')
TITRE_DECLASS = re.compile(r'(?i)d[ée]penses fiscales d[ée]class[ée]es')
AUCUN_CLASS = re.compile(r'(?i)aucun classement')
AUCUN_DECLASS = re.compile(r'(?i)aucun d[ée]classement')
# créations et suppressions : deux sections en sous-partie III (mesures adoptées
# depuis le précédent PLF) et deux en sous-partie IV (mesures proposées). Elles
# expliquent l'essentiel des entrées et sorties d'identifiants.
#: Les tables portent des intitulés variables selon la sous-partie et le
#: millésime : « CRÉATIONS », « Créations votées », « Créations de dépenses
#: fiscales proposées ». On reconnaît une ligne courte, sans chiffre ni
#: ponctuation de phrase, ouverte par le mot-clé — ce qui exclut la prose.
TITRE_CREATION = re.compile(r'(?i)^\s*cr[ée]ations?\b[^.\d]{0,45}$')
TITRE_SUPPRESSION = re.compile(r'(?i)^\s*suppressions?\b[^.\d]{0,45}$')
AUCUNE_CREATION = re.compile(r'(?i)aucune cr[ée]ation')
AUCUNE_SUPPRESSION = re.compile(r'(?i)aucune suppression')
#: une section s'arrête au titre de la suivante, quelle qu'elle soit
TITRES = (TITRE_RENUM, TITRE_CLASS, TITRE_DECLASS, TITRE_CREATION, TITRE_SUPPRESSION)
# bornes possibles d'une section : le titre de la sous-partie suivante
FIN_SECTION = re.compile(r'(?i)(sous.partie IV|[ée]volution propos[ée]e dans le pr[ée]sent PLF|'
                         r'cr[ée]ations et augmentations)')

#: Éclatements opérés par la revue des taxes intérieures de consommation de 2020,
#: décrits en prose et dans un tableau ad hoc du seul PLF 2021 (sous-partie III,
#: p. 34-35). Ils ne suivent aucun gabarit réutilisé ailleurs dans le corpus :
#: les transcrire ici est plus sûr que de parser une table unique au fonds.
#: Source : « Ainsi, la dépense fiscale n° 800118 est désormais décomposée en
#: n° 800118 et n° 830101, la dépense fiscale n° 800210 en n° 800210, n° 830201
#: et n° 840201, la dépense fiscale n° 800211 en n° 800211, n° 830202 et
#: n° 840202 et enfin la n° 800405 renumérotée n° 800229 en n° 800229 et
#: n° 830204. »
ECLATEMENTS = {
    2021: {
        '800118': ['800118', '830101'],
        '800210': ['800210', '830201', '840201'],
        '800211': ['800211', '830202', '840202'],
        '800229': ['800229', '830204'],
    },
}
SOURCE_ECLATEMENTS = "PLF2021 sous-partie III, revue des TIC (p. 34-35)"


def _section(lignes: list[str], titre: re.Pattern, taille: int = 80) -> list[str]:
    """Lignes de la dernière occurrence de `titre`, jusqu'à la section suivante.

    On retient la dernière occurrence : la première est le renvoi de sommaire.
    """
    debuts = [i for i, l in enumerate(lignes) if titre.search(l)]
    if not debuts:
        return []
    i = debuts[-1]
    fin = min(i + taille, len(lignes))
    for j in range(i + 3, fin):
        if FIN_SECTION.search(lignes[j]):
            fin = j
            break
    return lignes[i:fin]


def renumerotations(lignes: list[str], plf: int) -> list[dict]:
    """Table « ancien numéro -> nouveau numéro » de la sous-partie III."""
    bloc = _section(lignes, TITRE_RENUM, taille=120)
    if not bloc or any(AUCUNE_RENUM.search(l) for l in bloc[:6]):
        return []
    out = []
    for l in bloc:
        # une ligne d'enregistrement commence par l'ancien numéro et porte le
        # nouveau plus à droite ; les lignes de continuation n'ont pas de numéro
        if not re.match(r'^\s{0,8}\d{6}\b', l):
            continue
        nums = NUM.findall(l)
        if len(nums) < 2:
            continue
        libelle = NUM.sub(' ', l).strip()
        out.append(dict(plf_effet=plf, numero_ancien=nums[0], numero_nouveau=nums[-1],
                        type='renumerotation', libelle=re.sub(r'\s+', ' ', libelle)[:300],
                        source=f'PLF{plf} sous-partie III, reclassement par renumérotation'))
    return out


def _numeros_section(lignes: list[str], titre: re.Pattern, aucun: re.Pattern,
                     toutes: bool = False) -> list[str]:
    """Numéros cités dans une section. `toutes` balaie chaque occurrence du titre."""
    debuts = [i for i, l in enumerate(lignes) if titre.search(l)]
    if not debuts:
        return []
    vus: list[str] = []
    autres = [t for t in TITRES if t is not titre]
    for i in (debuts if toutes else debuts[-1:]):
        fin = min(i + 120, len(lignes))
        for j in range(i + 3, fin):
            if FIN_SECTION.search(lignes[j]) or any(t.search(lignes[j]) for t in autres):
                fin = j
                break
        bloc = lignes[i:fin]
        if any(aucun.search(l) for l in bloc[:8]):
            continue
        for l in bloc[1:]:
            # le numéro est en colonne de gauche du tableau, juste après le code
            # d'impôt ; le chercher plus loin ramasserait des références légales
            m = re.search(r'\b(\d{6})\b', l[:45])
            if m and m.group(1) not in vus:
                vus.append(m.group(1))
    return vus


def mouvements_declares(lignes: list[str], plf: int) -> list[dict]:
    """Renumérotations, éclatements, classements et déclassements d'un millésime."""
    out = renumerotations(lignes, plf)
    for ancien, nouveaux in ECLATEMENTS.get(plf, {}).items():
        for nouveau in nouveaux:
            out.append(dict(plf_effet=plf, numero_ancien=ancien, numero_nouveau=nouveau,
                            type='eclatement', libelle='', source=SOURCE_ECLATEMENTS))
    entrees = [
        ('classement', TITRE_CLASS, AUCUN_CLASS, False, 'sous-partie III, classements'),
        ('creation', TITRE_CREATION, AUCUNE_CREATION, True,
         'sous-parties III et IV, créations'),
    ]
    sorties = [
        ('declassement', TITRE_DECLASS, AUCUN_DECLASS, False,
         'sous-partie III, déclassements'),
        ('suppression', TITRE_SUPPRESSION, AUCUNE_SUPPRESSION, True,
         'sous-parties III et IV, suppressions'),
    ]
    for genre, titre, aucun, toutes, src in entrees:
        for num in _numeros_section(lignes, titre, aucun, toutes):
            out.append(dict(plf_effet=plf, numero_ancien='', numero_nouveau=num,
                            type=genre, libelle='', source=f'PLF{plf} {src}'))
    for genre, titre, aucun, toutes, src in sorties:
        for num in _numeros_section(lignes, titre, aucun, toutes):
            out.append(dict(plf_effet=plf, numero_ancien=num, numero_nouveau='',
                            type=genre, libelle='', source=f'PLF{plf} {src}'))
    return out


def diff_identifiants(presence: dict[int, set[str]], cw: list[dict]) -> list[dict]:
    """Entrées et sorties d'identifiants entre millésimes consécutifs.

    Chaque mouvement est marqué `explique` si une ligne du crosswalk prise au
    même millésime le justifie, `inexplique` sinon. Aucun appariement n'est
    déduit d'une ressemblance de libellé : ce qui reste inexpliqué est signalé,
    pas résolu.
    """
    entrants = {}
    sortants = {}
    for c in cw:
        p = c['plf_effet']
        if c['numero_nouveau']:
            entrants.setdefault((p, c['numero_nouveau']), []).append(c['type'])
        if c['numero_ancien']:
            sortants.setdefault((p, c['numero_ancien']), []).append(c['type'])

    out = []
    for plf in sorted(presence):
        if plf - 1 not in presence:
            continue
        for num in sorted(presence[plf] - presence[plf - 1]):
            just = entrants.get((plf, num), [])
            out.append(dict(plf_effet=plf, numero=num, sens='entree',
                            statut='explique' if just else 'inexplique',
                            justification=','.join(sorted(set(just)))))
        for num in sorted(presence[plf - 1] - presence[plf]):
            just = sortants.get((plf, num), [])
            out.append(dict(plf_effet=plf, numero=num, sens='sortie',
                            statut='explique' if just else 'inexplique',
                            justification=','.join(sorted(set(just)))))
    return out


def construire(cache: str, sortie: str, de: int = 2009, a: int = 2025) -> int:
    from . import regime_b, regime_c
    parseurs = {'B': regime_b, 'C': regime_c}

    cw, presence = [], {}
    for plf in range(de, a + 1):
        if plf not in SOURCES or REGIMES[plf] not in parseurs:
            continue
        lignes = texte(plf, cache)
        cw += mouvements_declares(lignes, plf)
        # seules les dépenses fiscales entrent dans le suivi : les mesures de
        # l'annexe « modalités de calcul de l'impôt » ne sont plus du périmètre
        # et leur disparition entre deux millésimes n'est pas un mouvement
        presence[plf] = {f['numero'] for f in parseurs[REGIMES[plf]].parse(lignes, plf)
                         if f.get('numero') and f.get('perimetre') == DEPENSE_FISCALE}
        n = sum(1 for c in cw if c['plf_effet'] == plf)
        print(f"  PLF{plf} : {len(presence[plf]):4d} identifiants, {n:3d} mouvement(s) déclaré(s)")

    mvt = diff_identifiants(presence, cw)
    os.makedirs(sortie, exist_ok=True)
    for nom, lignes_csv in (('crosswalk.csv', cw), ('mouvements.csv', mvt)):
        dest = os.path.join(sortie, nom)
        with open(dest, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(lignes_csv[0]), delimiter=';')
            w.writeheader()
            w.writerows(lignes_csv)
        print(f"-> {dest} : {len(lignes_csv)} lignes")

    inexpl = [m for m in mvt if m['statut'] == 'inexplique']
    print(f"\n{len(mvt) - len(inexpl)} mouvement(s) expliqué(s), {len(inexpl)} inexpliqué(s)")
    par_plf: dict[int, int] = {}
    for m in inexpl:
        par_plf[m['plf_effet']] = par_plf.get(m['plf_effet'], 0) + 1
    for plf in sorted(par_plf):
        print(f"  PLF{plf} : {par_plf[plf]}")

    ener = [m for m in mvt if m['numero'].startswith('8')]
    ko = [m for m in ener if m['statut'] == 'inexplique']
    print(f"\nÉnergie (8xxxxx) : {len(ener)} mouvement(s), {len(ko)} inexpliqué(s)")
    for m in ko:
        print(f"  ? PLF{m['plf_effet']} {m['numero']} {m['sens']}")
    return 0
