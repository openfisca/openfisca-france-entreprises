"""Contrôle par le tableau « Coût des dépenses fiscales par impôt ».

La sous-partie II de chaque tome II publie, pour les trois années du millésime,
le coût agrégé des dépenses fiscales par impôt. Confronter la somme des fiches
extraites à ce total est le seul recoupement de **valeur** disponible avant le
PLF 2022, où l'annexe mission-programme prend le relais.

    Impôt                                              Coût 2013   Coût 2014   Coût 2015
    Impôt sur le revenu                                   36 481      34 361      33 391
      dont crédit d'impôt                                  7 989       7 203       7 090
    …
    Taxe intérieure de consommation sur les produits…      3 811       3 539       3 245

**Ce contrôle n'est pas exact, et ne doit jamais être présenté comme tel.** Trois
raisons irréductibles :

- les mesures `nc` (non chiffrables) entrent dans le total publié sans valeur
  sommable — l'écart qu'elles créent est structurel ;
- les mesures `ε` valent « moins de 0,5 M€ » et sont comptées 0 ici ;
- les lignes « dont crédit d'impôt » / « dont réduction d'impôt » sont des
  sous-totaux du poste qui précède, à ne pas additionner.

L'écart est donc chiffré et affiché, avec le nombre de `nc` en regard. Un écart
de quelques unités sur un poste qui compte des `nc` est attendu ; un écart de
plusieurs centaines de M€ sur un poste entièrement chiffré est un défaut
d'extraction.
"""
from __future__ import annotations

import re
import unicodedata

from .commun import (DEPENSE_FISCALE, RE_MONTANT, apparie_par_colonne, colonnes,
                     normalise_montant)

ENTETE = re.compile(r'Co[ûu]t\s+(\d{4}).*?Co[ûu]t\s+(\d{4})', re.S)
RE_ANNEE = re.compile(r'\b(19|20)\d{2}\b')
DONT = re.compile(r'^\s*dont\b', re.I)

#: intitulé du tableau -> préfixe de numéro de dépense fiscale. Les intitulés
#: varient d'un millésime à l'autre (« Taxe intérieure de consommation sur les
#: produits énergétiques » puis « Accise sur les énergies »), d'où la
#: normalisation sans accents et la reconnaissance par mot-clé.
#: Intitulés reconnus par préfixe et testés du plus long au plus court, pour que
#: « Impôt sur le revenu et impôt sur les sociétés » ne soit pas capté par
#: « Impôt sur le revenu ».
POSTES = sorted([
    ('impot sur le revenu et impot sur les societes', '2'),
    ('impot sur le revenu', '1'),
    ('impot sur les societes', '3'),
    ('taxe sur la valeur ajoutee', '7'),
    ("droits d'enregistrement et de timbre", '5'),
    # à partir du PLF 2021 le poste énergie est éclaté en quatre lignes, qui
    # correspondent aux sous-impôts 80, 82, 83 et 84 ; avant, une seule ligne
    # couvre l'ensemble du chapitre 8
    ('taxe interieure de consommation sur les produits energetiques', '80'),
    ("taxe interieure de consommation sur la fourniture d'electricite", '82'),
    ('taxe interieure de consommation sur le gaz naturel', '83'),
    ('taxe interieure de consommation sur les charbons', '84'),
    ('taxe interieure de consommation', '8'),
    ('taxes interieures de consommation', '8'),
    ('accise sur les energies', '8'),
], key=lambda t: -len(t[0]))


def _plat(s: str) -> str:
    s = unicodedata.normalize('NFD', s.strip().lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s).strip(' .')


def _poste(intitule: str) -> str | None:
    plat = _plat(intitule)
    for cle, prefixe in POSTES:
        if plat.startswith(cle):
            return prefixe
    return None


def parse(lignes: list[str], plf: int) -> dict[tuple[str, int], int]:
    """(préfixe d'impôt, année) -> coût publié, en M€."""
    # l'en-tête « Coût AAAA  Coût AAAA  Coût AAAA » ouvre le tableau
    debut = cols = annees = None
    for i, l in enumerate(lignes[:3000]):
        c = colonnes(l, re.compile(r'Co[ûu]t\s+\d{4}'))
        if len(c) == 3:
            annees = [int(RE_ANNEE.search(t).group(0)) for _, t in c]
            if annees[-1] == plf:
                debut, cols = i, c
                break
    if debut is None:
        return {}

    out: dict[tuple[str, int], int] = {}
    reste = ''  # intitulé d'une ligne précédente laissée sans montant
    for l in lignes[debut + 1:debut + 40]:
        if DONT.match(l):
            continue
        coupe = int(cols[0][0]) - 10
        intitule, droite = l[:coupe], l[coupe:]
        # Un intitulé long est replié sur deux ou trois lignes, les montants
        # restant sur celle du milieu : on recolle avant de reconnaître le poste.
        prefixe = _poste(intitule) or _poste(reste + ' ' + intitule.strip())
        if prefixe is None:
            if intitule.strip() and not RE_MONTANT.fullmatch(intitule.strip()):
                reste = (reste + ' ' + intitule.strip()).strip()
            continue
        reste = ''
        bruts = apparie_par_colonne(cols, [(c + coupe, t)
                                           for c, t in colonnes(droite, RE_MONTANT)])
        for annee, brut in zip(annees, bruts):
            montant, chiffrage = normalise_montant(brut)
            if chiffrage == 'chiffre':
                out[(prefixe, annee)] = montant

    # Avant le PLF 2021 le tableau ne connaît qu'une ligne « taxe intérieure de
    # consommation sur les produits énergétiques », qui couvre tout le chapitre 8,
    # électricité comprise ; à partir du PLF 2021 elle est doublée de lignes
    # électricité, gaz et charbons et ne vaut plus que pour le sous-impôt 80.
    detaille = any(p in ('82', '83', '84') for p, _ in out)
    if not detaille:
        out = {(('8' if p == '80' else p), y): v for (p, y), v in out.items()}
    else:
        out = {(p, y): v for (p, y), v in out.items() if p != '8'}
    return out


def recoupement(fiches: list[dict], publie: dict[tuple[str, int], int], plf: int) -> list[dict]:
    """Somme extraite contre total publié, poste par poste et année par année."""
    if not publie:
        return []
    out = []
    for (prefixe, annee), total in sorted(publie.items()):
        # les mesures déclassées sont chiffrées dans le document mais exclues
        # des totaux publiés : les inclure fausserait le contrôle
        lot = [f for f in fiches
               if f.get('annee') == annee and f['numero'].startswith(prefixe)
               and f.get('perimetre') == DEPENSE_FISCALE]
        # le poste 1 (IR) ne doit pas absorber le poste 2 (IR et IS) : les
        # préfixes sont exclusifs sur le premier chiffre, ce que garantit le
        # plan de numérotation du document.
        somme = sum(f['montant'] for f in lot if f['chiffrage'] == 'chiffre')
        out.append(dict(plf=plf, impot=prefixe, annee=annee, publie=total, extrait=somme,
                        ecart=somme - total, n_mesures=len(lot),
                        n_nc=sum(1 for f in lot if f['chiffrage'] == 'nc'),
                        n_epsilon=sum(1 for f in lot if f['chiffrage'] == 'epsilon')))
    return out
