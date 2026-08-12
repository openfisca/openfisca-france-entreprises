"""Briques communes aux trois régimes de mise en page du Voies et Moyens tome II."""
from __future__ import annotations

import os
import re
import subprocess

# --- emplacement des sources -------------------------------------------------

RACINE_LF = r"Z:\2-Documentation\Finances publiques\LF"

#: millésime de PLF -> chemin relatif du tome II sous RACINE_LF.
#: Le PLF 2000 est absent du fonds (seul le tome 1 est présent).
SOURCES = {
    2001: r"LF2001\PLF\PLF2001VoiesEtMoyens(vol2).pdf",
    2002: r"LF2002\PLF2002VoiesEtMoyens(vol2).pdf",
    2003: r"LF2003\PLF2003VoiesEtMoyens(vol2).pdf",
    2004: r"LF2004\PLF2004VoiesEtMoyens(vol2).pdf",
    2005: r"LF2005\vm22005.pdf",
    2006: r"LF2006\PLF2006VoiesEtMoyens(vol2).pdf",
    2007: r"LF2007\PLF2007(VoiesEtMoyensTome2).pdf",
    2008: r"LF2008\PLF2008(VoiesEtMoyensTome2).pdf",
    2009: r"LF2009\PLF2009(VoiesEtMoyensTome2).pdf",
    2010: r"LF2010\PLF2010VoiesEtMoyens(vol2).pdf",
    2011: r"LF2011\PLF2011VoiesEtMoyens(tome2).pdf",
    2012: r"LF2012\PLF2012VoiesetMoyens(Vol2).pdf",
    2013: r"LF2013\PLF 2013 Eval Voies et Moyens 2.pdf",
    2014: r"LF2014\PLF2014 Evaluation Voies et Moyens - Tome II.pdf",
    2015: r"LF2015\VMT2-2015.pdf",
    2016: r"LF2016\VMT2-2016.pdf",
    2017: r"LF2017\VMT2-2017.pdf",
    2018: r"LF2018\VMT2-2018.pdf",
    2019: r"LF2019\VMT2-2019.pdf",
    2020: r"LF2020\VMT_2-2020.pdf",
    2021: r"LF2021\PLF2021_VM_T2.pdf",
    2022: r"LF2022\PLF2022_VM_T2.pdf",
    2023: r"LF2023\PLF 2023 VM T2.pdf",
    2024: r"LF2024\PLF 2024 VM T2.pdf",
    2025: r"LF2025\PLF 2025 - Voies_et_moyens_Tome_2_Depenses fiscales.pdf",
    2026: r"LF2026\PLF pour 2026_V&M tome II.pdf",
}

#: régime de mise en page par millésime (cf. note d'exploration).
REGIMES = {y: 'A' for y in range(2001, 2009)}
REGIMES.update({y: 'B' for y in range(2009, 2020)})
REGIMES.update({y: 'C' for y in range(2020, 2027)})


def chemin_pdf(plf: int) -> str:
    return os.path.join(RACINE_LF, SOURCES[plf])


def texte(plf: int, cache: str, mode: str = 'layout') -> list[str]:
    """Renvoie le tome II du millésime `plf` sous forme de lignes.

    `mode='layout'` conserve la géométrie des tableaux : c'est ce qu'il faut pour
    les fiches, dont les montants sont appariés aux années par colonne.

    `mode='raw'` restitue l'ordre de lecture du PDF. Certains tableaux d'annexe
    y sont bien mieux reconstruits — au PLF 2026, `-layout` débite la répartition
    par mission en trois colonnes verticales décalées, où le numéro d'une mesure
    voisine le libellé d'une autre et le montant d'une troisième.

    Le texte est extrait une fois puis mis en cache ; la source PDF n'est jamais
    modifiée.
    """
    os.makedirs(cache, exist_ok=True)
    suffixe = '' if mode == 'layout' else f'_{mode}'
    dest = os.path.join(cache, f'VMT2_{plf}{suffixe}.txt')
    if not os.path.exists(dest):
        subprocess.run(['pdftotext', f'-{mode}', '-enc', 'UTF-8', '-q',
                        chemin_pdf(plf), dest], check=True)
    with open(dest, encoding='utf-8', errors='replace') as fh:
        return fh.read().splitlines()


# --- normalisation des montants ----------------------------------------------

ESPACES = '\u00a0\u202f\u2009 '
_ESP = re.compile('[' + ESPACES + ']')

#: Un montant tel qu'il figure dans les tableaux. Le séparateur de milliers est
#: **un seul** caractère d'espacement suivi d'exactement trois chiffres : c'est
#: ce qui distingue « 1 238 » (un montant) de « 24  34 » (deux colonnes). Une
#: tokenisation plus permissive recolle les colonnes voisines en un seul nombre.
_GROUPE = r'\d{1,3}(?:[' + ESPACES + r']\d{3})*'
JETON_MONTANT = r'(?:-[' + ESPACES + r']?' + _GROUPE + r'|' + _GROUPE + r'|nc|ε|-)'
RE_MONTANT = re.compile(JETON_MONTANT)


def normalise_montant(brut: str | None):
    """(montant numérique en M€ ou None, statut du chiffrage).

    Conventions du document :
      - `nc`   : mesure non chiffrable
      - `ε`    : coût inférieur à 0,5 M€ (compté 0, drapeau `epsilon`)
      - `-`    : mesure sans objet cette année-là (créée ou éteinte)
      - vide   : cellule non renseignée
    """
    if brut is None:
        return None, 'absent'
    s = _ESP.sub('', brut.strip())
    if s == '':
        return None, 'absent'
    if s == 'nc':
        return None, 'nc'
    if s == 'ε':
        return 0, 'epsilon'
    if s == '-':
        return None, 'sans_objet'
    m = re.fullmatch(r'(-?)(\d+)', s)
    if m:
        return int(m.group(1) + m.group(2)), 'chiffre'
    return None, 'illisible:' + s[:20]


def colonnes(ligne: str, motif: re.Pattern) -> list[tuple[float, str]]:
    """Jetons trouvés dans `ligne`, avec le centre de chacun en colonnes."""
    out = []
    for m in motif.finditer(ligne):
        t = m.group(0).strip()
        if t:
            out.append(((m.start() + m.end() - 1) / 2.0, t))
    return out


def apparie_par_colonne(ancres: list[tuple[float, str]],
                        valeurs: list[tuple[float, str]]) -> list[str | None]:
    """Associe à chaque ancre (année) la valeur qui lui revient.

    Quand il y a autant de valeurs que d'années, l'ordre de lecture tranche seul
    et sans ambiguïté. C'est le cas courant, et il faut le traiter à part : au
    PLF 2026 les années de la grille sont serrées à gauche tandis que les
    montants sont étalés sur toute la largeur, si bien que la colonne la plus
    proche de « 2026 » est celle du montant de 2025.

    Quand il manque des valeurs — cellule vide dans le PDF —, on retombe sur la
    proximité de colonne, en appariant par distance croissante pour qu'une valeur
    isolée ne soit pas happée par la mauvaise année. Les ancres non servies
    reçoivent None.
    """
    if len(valeurs) == len(ancres):
        return [t for _, t in valeurs]
    res: list[str | None] = [None] * len(ancres)
    paires = sorted(((abs(ca - cv), i, j) for i, (ca, _) in enumerate(ancres)
                     for j, (cv, _) in enumerate(valeurs)))
    pris_a, pris_v = set(), set()
    for _, i, j in paires:
        if i in pris_a or j in pris_v:
            continue
        res[i] = valeurs[j][1]
        pris_a.add(i)
        pris_v.add(j)
    return res


def statut_annee(annee: int, plf: int) -> str:
    """Position de `annee` dans le triptyque roulant du millésime `plf`."""
    return {plf - 2: 'realisation', plf - 1: 'prevision', plf: 'prevision_plf'}.get(annee, 'autre')


#: Parité irrévocable franc / euro, fixée par le règlement (CE) n° 2866/98.
#: Le PLF 2001 est le seul millésime du corpus chiffré en millions de francs ;
#: tous les suivants sont en millions d'euros.
FRANCS_PAR_EURO = 6.55957
DERNIER_MILLESIME_EN_FRANCS = 2001


def unite_du_millesime(plf: int) -> str:
    return 'MF' if plf <= DERNIER_MILLESIME_EN_FRANCS else 'MEUR'


def en_millions_euros(montant, unite: str):
    """Convertit un montant vers les millions d'euros.

    La conversion est exacte au sens juridique — la parité est irrévocable — mais
    elle transforme un entier imprimé en francs en un décimal : 1 400 MF valent
    213,4 M€. La valeur d'origine reste lisible dans `montant` et `montant_brut`,
    et `unite` dit toujours dans quelle monnaie le document a publié.
    """
    if montant is None:
        return None
    return round(montant / FRANCS_PAR_EURO, 1) if unite == 'MF' else montant


#: La table est normalisée en deux fichiers, joints sur (plf, numero) : une
#: fiche porte trois chiffrages, et répéter son libellé et ses métadonnées sur
#: chacun quintuplerait le volume pour la même information.
CHAMPS_CHIFFRAGE = ['plf', 'numero', 'annee', 'statut', 'montant', 'unite',
                    'montant_meur', 'chiffrage', 'montant_brut']
CHAMPS_FICHE = ['plf', 'numero', 'impot', 'perimetre', 'libelle', 'finalite',
                'creation', 'modification', 'fin_fait_generateur', 'fin_incidence',
                'beneficiaires', 'nombre_beneficiaires', 'fiabilite', 'norme',
                'methode', 'reference', 'mission', 'observations',
                'changement_methode', 'regime', 'page_source']

#: premier chiffre du numéro -> catégorie d'impôt, d'après la sous-partie
#: « Principes de numérotation des dépenses fiscales ». Stable sur tout le corpus,
#: à ceci près que la catégorie 8 s'intitulait « taxe intérieure de consommation »
#: avant le PLF 2022 et « accise sur les énergies » depuis (recodification CIBS).
IMPOTS = {
    '0': 'Impôts locaux',
    '1': 'Impôt sur le revenu',
    '2': 'Impôt sur le revenu et impôt sur les sociétés',
    '3': 'Impôt sur les sociétés',
    '4': 'Autres impôts directs',
    '5': "Droits d'enregistrement et de timbre",
    '7': 'Taxe sur la valeur ajoutée',
    '8': 'Accise sur les énergies',
    '9': 'Autres droits',
}

#: sous-catégories à deux chiffres, restreintes à ce qui sert à OFF-E.
#: Les sous-impôts 83 et 84 n'existent que depuis le PLF 2021 (revue des TIC de
#: 2020) : avant, gaz et charbons sont confondus dans 80.
IMPOTS_2 = {
    '80': 'TICPE / produits énergétiques hors gaz et charbons',
    '82': 'TICFE / électricité',
    '83': 'TICGN / gaz naturels',
    '84': 'TICC / charbons',
}


def impot(numero: str) -> str:
    return IMPOTS_2.get(numero[:2]) or IMPOTS.get(numero[:1], '?')


#: Périmètre d'une mesure. Les tomes II de 2009 à 2019 impriment, après les
#: chapitres de dépenses fiscales, une annexe « mesures considérées comme des
#: modalités de calcul de l'impôt » : mêmes fiches, mêmes chiffrages, mais ces
#: mesures ne sont plus des dépenses fiscales et n'entrent pas dans les totaux
#: publiés. Les confondre gonfle l'impôt sur les sociétés 2008 de 12,5 Md€ à
#: cause de la seule 320103.
DEPENSE_FISCALE = 'depense_fiscale'
MODALITE_DE_CALCUL = 'modalite_de_calcul'
