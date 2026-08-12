"""Régime C : mise en page « fiche » du tome II, PLF 2020 à 2025.

Chaque dépense fiscale occupe un encadré de la forme

    800201 – Tarif réduit des gazoles non routiers …
        Impact budgétaire (en M€)          Création                    1970
      Réalisation  Prévision  Prévision    Modification                2024
         2023        2024       2025       Fin du fait générateur      2029
        1 238       1 050       862        Fin d'incidence budgétaire  2030
    Bénéficiaires / Fiabilité du réalisé / Norme fiscale de référence /
    Méthode de chiffrage / Référence / Mission et programme

L'ancrage se fait sur les libellés de la colonne de droite, présents même
lorsque les cellules de gauche sont vides : « Fin du fait générateur » porte
la ligne des années, « Fin d'incidence budgétaire » celle des montants. Les
montants sont ensuite appariés aux années **par position de colonne**, seule
méthode qui survive aux cellules vides.
"""
from __future__ import annotations

import re
import unicodedata

from .commun import (DEPENSE_FISCALE, RE_MONTANT, apparie_par_colonne, colonnes,
                     impot, normalise_montant, statut_annee)

ANCRE = re.compile(r"Impact budg[ée]taire")
L_ANNEES = re.compile(r"Fin du fait g[ée]n[ée]rateur")
L_MONTANTS = re.compile(r"Fin d.incidence budg[ée]taire")
L_CREATION = re.compile(r"\bCr[ée]ation\b")
L_MODIF = re.compile(r"\bModification\b")

RE_ANNEE = re.compile(r'\b(19|20)\d{2}\b')
NUMERO = re.compile(r'^\s{0,24}(\d{6})\s*(?:[-–—]\s*)?(.*)$')
CLEVAL = re.compile(
    r'^\s*(B[ée]n[ée]ficiaires|Fiabilit[ée] du r[ée]alis[ée]|Norme fiscale de r[ée]f[ée]rence|'
    r'M[ée]thode de chiffrage|R[ée]f[ée]rence|Mission et programme)\s*(.*)$')
BRUIT = re.compile(
    r"Annexe au PLF|Voies et [Mm]oyens|PLF \d{4}|^\s*\d{1,3}\s*$|"
    r"^\s*(Exon[ée]rations?|Tarifs? r[ée]duits?|Taux r[ée]duits?|Modalit[ée]s|Divers|"
    r"Assiette et taux|R[ée]gimes?[^:]{0,40})\s*$")

#: libellé sans accents ni casse -> nom de colonne
CLES = {'beneficiaires': 'beneficiaires', 'fiabilite du realise': 'fiabilite',
        'norme fiscale de reference': 'norme', 'methode de chiffrage': 'methode',
        'reference': 'reference', 'mission et programme': 'mission'}


def _cle(libelle: str) -> str | None:
    plat = unicodedata.normalize('NFD', libelle.strip().lower())
    plat = ''.join(c for c in plat if unicodedata.category(c) != 'Mn')
    return CLES.get(re.sub(r'\s+', ' ', plat))

#: numéro de page imprimé, tel que pdftotext le laisse en pied/tête de page
PAGE = re.compile(r'^\s*(\d{1,3})\s*$')


def _valeur_droite(ligne: str, motif: re.Pattern) -> tuple[str, str]:
    """Découpe `ligne` au libellé `motif` : (partie gauche, valeur à droite)."""
    m = motif.search(ligne)
    if not m:
        return ligne, ''
    return ligne[:m.start()], ligne[m.end():].strip()


FINALITE = re.compile(r'^Finalit[ée]\s*:\s*(.*)$')


def _entete(lignes: list[str], a: int) -> tuple[str | None, str, str]:
    """Remonte depuis la grille pour retrouver le numéro et le libellé.

    Le numéro est une cellule de tableau verticalement centrée : selon le
    millésime il est seul sur sa ligne (2020, 2022) ou suivi du libellé
    (2021, 2023-2025), et le libellé peut déborder au-dessus comme en dessous.
    """
    for b in range(a - 1, max(a - 14, -1), -1):
        m = NUMERO.match(lignes[b])
        if not m:
            if lignes[b].strip() and CLEVAL.match(lignes[b]):
                break
            continue
        morceaux = []
        if m.group(2).strip():
            # le numéro et le début du libellé partagent la ligne (2021, 2023-2025,
            # et la plupart des fiches de 2020 et 2022) : rien à chercher au-dessus,
            # ce qui précède est un titre de rubrique.
            morceaux.append(m.group(2).strip())
        else:
            # cellule de numéro verticalement centrée : le libellé déborde au-dessus.
            # On n'accepte qu'un texte indenté dans la colonne du libellé, ce qui
            # exclut les titres de rubrique, alignés en marge.
            for c in range(b - 1, max(b - 4, -1), -1):
                s = lignes[c].strip()
                if not s:
                    continue
                indent = len(lignes[c]) - len(lignes[c].lstrip())
                if indent < 6 or BRUIT.search(lignes[c]) or NUMERO.match(lignes[c]) \
                   or CLEVAL.match(lignes[c]) or ANCRE.search(lignes[c]):
                    break
                morceaux.insert(0, s)
        # fragments entre la ligne du numéro et la grille, hors ligne « Finalité »
        finalite = ''
        for c in range(b + 1, a):
            s = lignes[c].strip()
            if not s or BRUIT.search(lignes[c]):
                continue
            mf = FINALITE.match(s)
            if mf:
                finalite = mf.group(1).strip()
            else:
                morceaux.append(s)
        return m.group(1), ' '.join(morceaux), finalite
    return None, '', ''


def parse(lignes: list[str], plf: int) -> list[dict]:
    n = len(lignes)
    fiches: list[dict] = []
    page = None
    for a in range(n):
        mp = PAGE.match(lignes[a])
        if mp:
            page = int(mp.group(1))
        if not ANCRE.search(lignes[a]):
            continue

        numero, libelle, finalite = _entete(lignes, a)
        if numero is None:
            fiches.append({'plf': plf, 'anomalie': 'numero introuvable', 'ligne': a})
            continue

        # --- la grille : deux lignes repérées par leur libellé de droite
        i_annees = i_montants = None
        meta = {}
        for k in range(a, min(a + 12, n)):
            if k > a and ANCRE.search(lignes[k]):
                break
            if i_annees is None and L_ANNEES.search(lignes[k]):
                i_annees = k
            if i_montants is None and L_MONTANTS.search(lignes[k]):
                i_montants = k
            if 'creation' not in meta and L_CREATION.search(lignes[k]):
                meta['creation'] = _valeur_droite(lignes[k], L_CREATION)[1]
            if 'modification' not in meta and L_MODIF.search(lignes[k]):
                meta['modification'] = _valeur_droite(lignes[k], L_MODIF)[1]
        if i_annees is None or i_montants is None:
            fiches.append({'plf': plf, 'numero': numero, 'anomalie': 'grille absente',
                           'ligne': a})
            continue

        g_annees, meta['fin_fait_generateur'] = _valeur_droite(lignes[i_annees], L_ANNEES)
        g_montants, meta['fin_incidence'] = _valeur_droite(lignes[i_montants], L_MONTANTS)

        ancres = [(c, t) for c, t in colonnes(g_annees, RE_ANNEE)]
        if len(ancres) != 3:
            fiches.append({'plf': plf, 'numero': numero,
                           'anomalie': f'{len(ancres)} années au lieu de 3', 'ligne': a})
            continue
        bruts = apparie_par_colonne(ancres, colonnes(g_montants, RE_MONTANT))

        # --- les six lignes clé/valeur sous la grille
        kv = {}
        for k in range(i_montants + 1, min(i_montants + 26, n)):
            if ANCRE.search(lignes[k]):
                break
            m = CLEVAL.match(lignes[k])
            if m:
                col = _cle(m.group(1))
                if col and col not in kv:
                    kv[col] = m.group(2).strip()

        for (_, annee), brut in zip(ancres, bruts):
            montant, chiffrage = normalise_montant(brut)
            fiches.append(dict(
                plf=plf, numero=numero, annee=int(annee),
                statut=statut_annee(int(annee), plf),
                montant=montant, chiffrage=chiffrage, montant_brut=(brut or ''),
                impot=impot(numero), perimetre=DEPENSE_FISCALE,
                libelle=libelle[:500], finalite=finalite[:300],
                creation=meta.get('creation', ''), modification=meta.get('modification', ''),
                fin_fait_generateur=meta.get('fin_fait_generateur', ''),
                fin_incidence=meta.get('fin_incidence', ''),
                regime='C', page_source=page, **{k: kv.get(k, '') for k in CLES.values()}))
    return fiches


def nb_attendu(lignes: list[str]) -> int:
    """Contrôle d'exhaustivité : une grille « Impact budgétaire » par dépense."""
    return sum(1 for l in lignes if ANCRE.search(l))
