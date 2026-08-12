"""Régime A : mise en page d'origine du tome II, PLF 2001 à 2008.

    80 01 01 Exonération de TIPP pour les produits pétroliers utilisés par   1 400   1 480   1 520
             certains bateaux
                Objectifs (38) :   Aider le secteur de la pêche et celui du
                                   commerce maritime
                Bénéficiaires    : Entreprises
                Code des Douanes: 190
                Observations :     Coût incluant l'incidence TVA
                Ministère(s)   :   Agriculture et pêche

Deux différences avec les régimes suivants commandent ce parseur.

**Le numéro est écrit par groupes de deux chiffres** (« 80 01 01 »), et cette
ligne d'ouverture est un ancrage idéal : elle est strictement unique dans chaque
document du corpus, contrairement au régime B où les numéros sont repris par
d'autres tableaux.

**Les années ne sont pas toujours introduites par « pour »**. L'en-tête de
colonne se replie différemment selon le millésime — « Résultat estimé pour 2003 »
tient sur deux lignes en 2005, sur trois en 2008 où « 2006 » se retrouve seul
avec l'unité. On repère donc les millésimes comme de simples nombres à quatre
chiffres formant un triplet consécutif fermé sur l'année du PLF.

**Attention à l'unité** : le PLF 2001 chiffre en millions de **francs**, tous les
suivants en millions d'euros. Voir `commun.unite_du_millesime` et
`commun.en_millions_euros`.
"""
from __future__ import annotations

import re
import unicodedata

from .commun import (DEPENSE_FISCALE, RE_MONTANT, apparie_par_colonne, colonnes,
                     en_millions_euros, impot, normalise_montant, statut_annee,
                     unite_du_millesime)

FICHE = re.compile(r'^\s{0,4}(\d\d \d\d \d\d)\s+(\S.*)$')
ENTETE = re.compile(r'^\s*Num[ée]ro\b')
ANNEE = re.compile(r'\b((?:19|20)\d{2})\b')
CLEVAL = re.compile(r'^\s*([^:]{3,60}?)\s*:\s*(.*)$')
PAGE = re.compile(r'^\s*(\d{1,3})\s*$')
BRUIT = re.compile(r'(?i)(voies et moyens|^\s*P\.?L\.?F\.? ?\d{4}|\(en (MF|M€|millions))')

#: clé du document (sans accents, sans casse, numéro d'objectif retiré) ->
#: colonne de sortie. Le vocabulaire d'avant la LOLF n'a pas d'équivalent exact :
#: « Ministère(s) » tient la place que « Mission et programme » prendra en 2006,
#: et « Chiffrage » celle de « Méthode de chiffrage ».
CLES = {
    'beneficiaires': 'beneficiaires',
    'nombre de beneficiaires': 'nombre_beneficiaires',
    'objectifs': 'finalite',
    'objectif': 'finalite',
    'ministere(s)': 'mission',
    'ministere': 'mission',
    'mission / programme': 'mission',
    'mission et programme': 'mission',
    'ref. cgi': 'reference',
    'code des douanes': 'reference',
    'code general des impots': 'reference',
    'observations': 'observations',
    'chiffrage': 'methode',
    'fiabilite': 'fiabilite',
    'annee de creation de la depense': 'creation',
    # la clé « Année de dernière modification substantielle de la dépense » est
    # coupée en deux lignes par la mise en page : seule la seconde porte la valeur
    'substantielle de la depense': 'modification',
    'changement de methode de chiffrage': 'changement_methode',
}
#: rattachements secondaires, sans intérêt ici mais à reconnaître pour qu'ils ne
#: soient pas pris pour la suite d'un libellé
IGNOREES = {'titre subsidiaire', 'a titre subsidiaire'}
#: Premier morceau d'une clé que la mise en page coupe en deux — la valeur est
#: portée par la seconde ligne (« substantielle de la dépense : 1978 »). Sans
#: cette liste, le fragment serait recollé à la valeur qui précède, et l'année
#: de création deviendrait « 1928 Année de dernière modification ».
FRAGMENTS_DE_CLE = re.compile(r'(?i)^ann[ée]e de derni[èe]re modification\s*$')


def _plat(s: str) -> str:
    s = unicodedata.normalize('NFD', s.strip().lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'\(\d+\)', '', s)).strip()


def _entetes(lignes: list[str], plf: int) -> list[tuple[int, tuple, list]]:
    """En-têtes de colonne valides : trois millésimes consécutifs finissant sur `plf`."""
    attendus = (plf - 2, plf - 1, plf)
    out = []
    for i, l in enumerate(lignes):
        if not ENTETE.match(l):
            continue
        trouves: dict[int, float] = {}
        for k in range(i, min(i + 6, len(lignes))):
            for c, t in colonnes(lignes[k], ANNEE):
                trouves.setdefault(int(t), c)
        if all(a in trouves for a in attendus):
            out.append((i, attendus, [(trouves[a], str(a)) for a in attendus]))
    return out


def parse(lignes: list[str], plf: int) -> list[dict]:
    entetes = _entetes(lignes, plf)
    if not entetes:
        return [{'plf': plf, 'anomalie': "aucun en-tête d'années trouvé", 'ligne': 0}]
    positions = [e[0] for e in entetes]
    unite = unite_du_millesime(plf)

    def entete_de(i: int):
        prec = [e for e, p in zip(entetes, positions) if p <= i]
        return prec[-1] if prec else entetes[0]

    n = len(lignes)
    fiches: list[dict] = []
    page = None
    for debut in range(n):
        mp = PAGE.match(lignes[debut])
        if mp:
            page = int(mp.group(1))
        m = FICHE.match(lignes[debut])
        if not m:
            continue
        numero = m.group(1).replace(' ', '')

        _, annees, cols_annees = entete_de(debut)
        coupe = max(int(min(c for c, _ in cols_annees)) - 8, 0)
        gauche, droite = lignes[debut][:coupe], lignes[debut][coupe:]
        valeurs = [(c + coupe, t) for c, t in colonnes(droite, RE_MONTANT)]
        bruts = apparie_par_colonne(cols_annees, valeurs)

        morceaux = [gauche.split(m.group(1), 1)[-1].strip()]
        kv: dict[str, str] = {}
        derniere = None
        for k in range(debut + 1, min(debut + 30, n)):
            if FICHE.match(lignes[k]):
                break
            s = lignes[k].strip()
            mc = CLEVAL.match(lignes[k])
            cle = _plat(mc.group(1)) if mc else ''
            if mc and cle in IGNOREES:
                derniere = None
                continue
            if not mc or cle not in CLES:
                if not s or PAGE.match(lignes[k]) or BRUIT.search(lignes[k]):
                    continue
                if FRAGMENTS_DE_CLE.match(s):
                    continue
                if not kv:
                    # avant la première clé, c'est la suite du libellé — qui peut
                    # lui-même porter un « : » et ressembler à une clé inconnue
                    morceaux.append(s)
                elif derniere:
                    kv[derniere] = (kv[derniere] + ' ' + s).strip()
                continue
            derniere = CLES[cle]
            kv.setdefault(derniere, mc.group(2).strip())

        libelle = re.sub(r'\s+', ' ', ' '.join(x for x in morceaux if x)).strip()
        for annee, brut in zip(annees, bruts):
            montant, chiffrage = normalise_montant(brut)
            fiches.append(dict(
                plf=plf, numero=numero, annee=annee, statut=statut_annee(annee, plf),
                montant=montant, chiffrage=chiffrage, montant_brut=(brut or ''),
                unite=unite, montant_meur=en_millions_euros(montant, unite),
                impot=impot(numero), perimetre=DEPENSE_FISCALE,
                libelle=libelle[:500], finalite=kv.get('finalite', ''),
                creation=kv.get('creation', ''), modification=kv.get('modification', ''),
                fin_fait_generateur='', fin_incidence='',
                beneficiaires=kv.get('beneficiaires', ''),
                nombre_beneficiaires=kv.get('nombre_beneficiaires', ''),
                fiabilite=kv.get('fiabilite', ''), norme='',
                methode=kv.get('methode', ''), reference=kv.get('reference', ''),
                mission=kv.get('mission', ''), observations=kv.get('observations', ''),
                changement_methode=kv.get('changement_methode', ''),
                regime='A', page_source=page))
    return fiches


def nb_attendu(lignes: list[str]) -> int:
    """Contrôle d'exhaustivité : une ligne d'ouverture par dépense fiscale.

    Ce décompte est fiable ici parce que le motif « 80 01 01 » en tête de ligne
    n'apparaît nulle part ailleurs : sur les huit millésimes du régime A, aucun
    numéro n'est vu deux fois.
    """
    return len({FICHE.match(l).group(1) for l in lignes if FICHE.match(l)})
