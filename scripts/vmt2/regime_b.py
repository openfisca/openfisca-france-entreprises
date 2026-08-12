"""Régime B : mise en page tabulaire du tome II, PLF 2009 à 2019.

Une dépense fiscale y occupe une ligne de tableau — numéro, libellé, puis les
trois chiffrages alignés à droite — suivie d'un bloc de lignes `Clé : valeur` :

    800201 Taux réduit de TIC sur le gazole sous condition d'emploi, repris    1 770  1 700  1 790
           à l'indice 20 du tableau B de l'article 265 du code des douanes
             Mission et programme :   Agriculture… / Économie et développement… (P154)
             Objectif :               Aider les secteurs agricole et piscicole
             Création / modification : 1970 / 2013
             Code des Douanes :       265 (tableau B)

L'ancrage se fait sur `Création / modification`, seule clé présente sur toutes
les fiches et sur elles seules : les autres tableaux du document (norme fiscale
de référence, récapitulatifs par mission) reprennent les numéros et les libellés
mais jamais cette ligne. Les années sont lues sur l'en-tête de colonne réaffirmé
en tête de chaque page, et les montants leur sont appariés par position de
colonne, comme au régime C.
"""
from __future__ import annotations

import re
import unicodedata

from .commun import (DEPENSE_FISCALE, MODALITE_DE_CALCUL, RE_MONTANT,
                     apparie_par_colonne, colonnes, impot, normalise_montant,
                     statut_annee)

ANCRE = re.compile(r'Cr[ée]ation\s*/\s*modification\s*:')
#: en-tête de colonne : la ligne se termine par trois millésimes consécutifs.
#: Selon les années les libellés qui précèdent diffèrent (« Numéro de la mesure »,
#: « N° de la mesure », intitulé de l'impôt) : seule la queue est fiable.
ENTETE = re.compile(r'(\d{4})\s+(\d{4})\s+(\d{4})\s*$')
FICHE = re.compile(r'^\s{0,6}(\d{6})\s+(\S.*)$')
CLEVAL = re.compile(r'^\s*([^:]{3,60}?)\s*:\s*(.*)$')
PAGE = re.compile(r'^\s*(\d{1,3})\s{10,}PLF \d{4}\s*$')
#: mobilier de page que pdftotext laisse au milieu des fiches
BRUIT = re.compile(r'(?i)(voies et moyens|chiffrages des d[ée]penses fiscales|'
                   r'^\s*PLF \d{4}\s*$|en millions d.euros)')

#: clé du document (sans accents ni casse) -> colonne de sortie, alignée sur le
#: vocabulaire du régime C pour que les deux régimes produisent la même table.
CLES = {
    'mission et programme': 'mission',
    'objectif': 'finalite',
    'finalite': 'finalite',
    'methode de chiffrage': 'methode',
    'fiabilite': 'fiabilite',
    'fiabilite du realise': 'fiabilite',
    'fin du fait generateur': 'fin_fait_generateur',
    "fin d'incidence budgetaire": 'fin_incidence',
    'norme fiscale de reference': 'norme',
    'code des douanes': 'reference',
    'ref. cgi': 'reference',
    'reference': 'reference',
    'code general des impots': 'reference',
}
#: clés dont la valeur est un nombre de bénéficiaires ; le millésime figure dans
#: la clé elle-même (« Bénéficiaires 2013 : »), qu'on normalise donc à part.
RE_BENEF = re.compile(r'^b[ée]n[ée]ficiaires(\s+\d{4})?$', re.I)
RE_CREAMOD = re.compile(r'^\s*(\d{4}|-)?\s*/\s*(\d{4}|-)?\s*$')
#: signalement porté sur certaines fiches, sans clé, quand le chiffrage change
#: de méthode d'un millésime à l'autre — donc quand une rupture de série est
#: imputable à la mesure du coût et non à son évolution
CHANGEMENT = re.compile(r'(?i)^changement de m[ée]thode de chiffrage\s*$')
#: Ouverture de l'annexe des mesures déclassées, qui ferme la partie « chiffrages
#: des dépenses fiscales ». Deux formulations selon les millésimes : un en-tête
#: de page « MESURES CONSIDÉRÉES COMME DES MODALITÉS DE CALCUL DE L'IMPÔT »
#: (2009-2015) ou un titre de section « MODALITÉS DE CALCUL DE L'IMPÔT » seul
#: sur sa ligne (2016-2019). La seconde forme doit être ancrée : la locution
#: apparaît aussi dans des libellés de mesure (« … : Modalités de calcul »).
ANNEXE_MODALITES = re.compile(
    r'(?i)(mesures consid[ée]r[ée]es comme des modalit[ée]s de calcul de l.imp[ôo]t'
    r'|^\s*modalit[ée]s de calcul de l.imp[ôo]t\s*$)')


def _plat(s: str) -> str:
    s = unicodedata.normalize('NFD', s.strip().lower())
    return re.sub(r'\s+', ' ', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))


def _entetes(lignes: list[str], plf: int) -> list[tuple[int, tuple, list]]:
    """Positions et colonnes des en-têtes d'années valides pour ce millésime."""
    out = []
    for i, l in enumerate(lignes):
        m = ENTETE.search(l)
        if not m:
            continue
        a = [int(x) for x in m.groups()]
        if a[1] == a[0] + 1 and a[2] == a[1] + 1 and a[2] == plf:
            cols = colonnes(l[m.start():], re.compile(r'\d{4}'))
            cols = [(c + m.start(), t) for c, t in cols]
            out.append((i, tuple(a), cols))
    return out


def parse(lignes: list[str], plf: int) -> list[dict]:
    entetes = _entetes(lignes, plf)
    if not entetes:
        return [{'plf': plf, 'anomalie': "aucun en-tête d'années trouvé", 'ligne': 0}]
    positions = [e[0] for e in entetes]

    def entete_de(i: int):
        """En-tête de colonne en vigueur à la ligne i (le dernier au-dessus)."""
        prec = [e for e, p in zip(entetes, positions) if p <= i]
        return prec[-1] if prec else entetes[0]

    # frontière entre les dépenses fiscales et l'annexe des mesures déclassées :
    # la première page de l'annexe, en ignorant les renvois du sommaire
    bascule = next((i for i, l in enumerate(lignes)
                    if i > 2000 and ANNEXE_MODALITES.search(l)), len(lignes))

    n = len(lignes)
    fiches: list[dict] = []
    page = None
    for a in range(n):
        mp = PAGE.match(lignes[a])
        if mp:
            page = int(mp.group(1))
        if not ANCRE.search(lignes[a]):
            continue

        # --- remonter jusqu'à la ligne de tableau qui ouvre la fiche
        # Le seul discriminant est le numéro en tête de ligne : un libellé peut
        # contenir un « : » (« Exonération sous certaines conditions : - des
        # coopératives… ») et ne doit pas pour autant passer pour une clé.
        debut = None
        for b in range(a - 1, max(a - 24, -1), -1):
            if FICHE.match(lignes[b]):
                debut = b
                break
            if ANCRE.search(lignes[b]):
                break
        if debut is None:
            fiches.append({'plf': plf, 'anomalie': 'ligne de mesure introuvable', 'ligne': a})
            continue
        numero, reste = FICHE.match(lignes[debut]).groups()

        _, annees, cols_annees = entete_de(debut)
        # le libellé occupe la gauche de la ligne, les montants la droite : on
        # coupe un peu avant la première colonne d'année pour ne pas prendre un
        # nombre du libellé (« 5 ans », « E85 ») pour un chiffrage.
        coupe = int(cols_annees[0][0]) - 8
        gauche, droite = lignes[debut][:coupe], lignes[debut][coupe:]
        valeurs = [(c + coupe, t) for c, t in colonnes(droite, RE_MONTANT)]
        bruts = apparie_par_colonne(cols_annees, valeurs)

        # --- libellé : reste de la ligne d'ouverture puis lignes de continuation
        morceaux = [gauche[len(gauche) - len(gauche.lstrip()):].split(numero, 1)[-1].strip()
                    if numero in gauche else reste.strip()]
        kv: dict[str, str] = {}
        creation = modification = ''
        derniere = None
        for k in range(debut + 1, min(debut + 30, n)):
            if FICHE.match(lignes[k]):
                break
            s = lignes[k].strip()
            m = CLEVAL.match(lignes[k])
            cle = _plat(m.group(1)) if m else ''
            connue = bool(m) and (RE_BENEF.match(cle) or cle == 'creation / modification'
                                  or cle in CLES)
            if not connue:
                if not s or PAGE.match(lignes[k]) or BRUIT.search(lignes[k]):
                    continue
                if CHANGEMENT.match(s):
                    # mention isolée, sans clé : c'est un drapeau sur la fiche,
                    # pas la suite de la valeur qui précède
                    kv['changement_methode'] = 'oui'
                    continue
                if not kv:
                    # tant qu'aucune clé n'a été vue, ce qui suit la ligne
                    # d'ouverture est la suite du libellé, « : » compris
                    morceaux.append(s)
                elif derniere:
                    # sinon c'est la suite de la valeur précédente, que la mise
                    # en page a repliée sur une deuxième ligne
                    kv[derniere] = (kv[derniere] + ' ' + s).strip()
                continue
            val = m.group(2).strip()
            if RE_BENEF.match(cle):
                derniere = 'beneficiaires'
            elif cle == 'creation / modification':
                derniere = None
                mm = RE_CREAMOD.match(val)
                if mm:
                    creation, modification = (mm.group(1) or ''), (mm.group(2) or '')
                continue
            else:
                derniere = CLES[cle]
            kv.setdefault(derniere, val)

        libelle = re.sub(r'\s+', ' ', ' '.join(x for x in morceaux if x)).strip()
        for annee, brut in zip(annees, bruts):
            montant, chiffrage = normalise_montant(brut)
            fiches.append(dict(
                plf=plf, numero=numero, annee=annee, statut=statut_annee(annee, plf),
                montant=montant, chiffrage=chiffrage, montant_brut=(brut or ''),
                impot=impot(numero),
                perimetre=DEPENSE_FISCALE if debut < bascule else MODALITE_DE_CALCUL,
                libelle=libelle[:500],
                creation=creation, modification=modification,
                fin_fait_generateur=kv.get('fin_fait_generateur', ''),
                fin_incidence=kv.get('fin_incidence', ''),
                beneficiaires=kv.get('beneficiaires', ''), fiabilite=kv.get('fiabilite', ''),
                norme=kv.get('norme', ''), methode=kv.get('methode', ''),
                reference=kv.get('reference', ''), mission=kv.get('mission', ''),
                changement_methode=kv.get('changement_methode', ''),
                finalite=kv.get('finalite', ''), regime='B', page_source=page))
    return fiches


def nb_attendu(lignes: list[str]) -> int:
    """Contrôle d'exhaustivité : une ligne « Création / modification » par fiche."""
    return sum(1 for l in lignes if ANCRE.search(l))
