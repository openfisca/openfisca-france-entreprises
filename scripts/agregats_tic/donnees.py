"""Lecture et mise en forme des agrégats 2040-TIC."""

from __future__ import annotations

import csv
import datetime
import os
import re
from dataclasses import dataclass

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHEMIN_AGREGATS = os.path.join(RACINE, "assets", "agregats.csv")
CHEMIN_PARAMETRES = os.path.join(RACINE, "openfisca_france_entreprises", "parameters")

# Les libellés du fichier source sont tronqués à 200 caractères : le suffixe
# « Quantité » / « Montant » peut arriver amputé (« Quant », « Mon », « T »…).
_SUFFIXES_QUANTITE = ("quantite", "quantites", "quantit", "quanti", "quant", "quan", "qua", "qu", "q")
_SUFFIXES_MONTANT = ("montant", "montants", "montan", "monta", "mont", "mon", "mo", "m")


@dataclass(frozen=True)
class Observation:
    """Une case de la déclaration, pour un millésime."""

    millesime: int
    case: str
    valeur: float
    libelle: str
    nombre_declarants: int


def _sans_accents(texte: str) -> str:
    remplacements = {"é": "e", "è": "e", "ê": "e", "à": "a", "î": "i", "ô": "o", "û": "u", "ç": "c"}
    for source, cible in remplacements.items():
        texte = texte.replace(source, cible).replace(source.upper(), cible)
    return texte


def segment_final(libelle: str) -> str:
    """Dernier segment d'un libellé, les séparateurs étant « - » et « _ »."""
    segments = [s.strip() for s in re.split(r"\s+-\s+|_", libelle) if s.strip()]
    return segments[-1] if segments else ""


def nature(libelle: str) -> str | None:
    """« quantite », « montant » ou None, d'après le dernier segment du libellé."""
    final = _sans_accents(segment_final(libelle)).lower()
    if final in _SUFFIXES_QUANTITE or final.startswith("quantite"):
        return "quantite"
    if final in _SUFFIXES_MONTANT or final.startswith("montant"):
        return "montant"
    # Les lignes d'exonération portent « QUANTITES EXEMPTEES » / « QUANTITES EXONEREES ».
    if "quantite" in final:
        return "quantite"
    if "montant" in final:
        return "montant"
    return None


def tarifs_annonces(libelle: str) -> list[float]:
    """Tarifs explicitement cités dans le libellé, en €/MWh.

    Beaucoup de cases nomment leur propre tarif (« Tarif à 33,70 €/MWh »), ce qui
    permet de recouper le tarif implicite sans passer par le barème.
    """
    trouves = re.findall(r"([\d]+(?:,\d+)?)\s*€\s*/?\s*MWh", libelle)
    return [float(t.replace(",", ".")) for t in trouves]


def charger(chemin: str = CHEMIN_AGREGATS) -> list[Observation]:
    with open(chemin, encoding="utf-8") as fichier:
        return [
            Observation(
                millesime=int(ligne["millesime"]),
                case=ligne["case"],
                valeur=float(ligne["sum"]),
                libelle=ligne["label"],
                nombre_declarants=int(ligne["ntot"]),
            )
            for ligne in csv.DictReader(fichier)
        ]


def indexer(observations: list[Observation]) -> tuple[dict[int, dict[str, float]], dict[str, str]]:
    """Retourne (valeurs[millésime][case], libellés[case])."""
    valeurs: dict[int, dict[str, float]] = {}
    libelles: dict[str, str] = {}
    for observation in observations:
        valeurs.setdefault(observation.millesime, {})[observation.case] = observation.valeur
        libelles.setdefault(observation.case, observation.libelle)
    return valeurs, libelles


def apparier(libelles: dict[str, str]) -> list[tuple[str, tuple[str, ...]]]:
    """Apparie chaque case de quantité aux cases de montant qui la suivent.

    La 2040-TIC numérote les cases par couples consécutifs (quantité, montant).
    Depuis le millésime 2025, une quantité peut porter deux montants : la
    fraction de droit commun et la majoration ZNI, déclarées séparément.
    """
    cases = sorted(libelles)
    numero = {case: int(case[1:]) for case in cases}
    natures = {case: nature(libelles[case]) for case in cases}

    couples: list[tuple[str, tuple[str, ...]]] = []
    for rang, case in enumerate(cases):
        if natures[case] != "quantite":
            continue
        montants: list[str] = []
        for suivante in cases[rang + 1 : rang + 4]:
            if numero[suivante] != numero[case] + len(montants) + 1:
                break
            if natures[suivante] != "montant":
                break
            # Une régularisation n'est pas une composante du tarif de la cellule.
            if "egularisation" in libelles[suivante]:
                break
            montants.append(suivante)
        if montants:
            couples.append((case, tuple(montants)))
    return couples


def tarif_implicite(
    valeurs: dict[int, dict[str, float]],
    millesime: int,
    case_quantite: str,
    cases_montant: tuple[str, ...],
) -> float | None:
    """Rapport montant / quantité pour une cellule et un millésime."""
    quantite = valeurs.get(millesime, {}).get(case_quantite)
    if not quantite:
        return None
    montant = sum(valeurs[millesime].get(case, 0.0) for case in cases_montant)
    return montant / quantite


# --------------------------------------------------------------------------
# Lecture directe des paramètres YAML
#
# Instancier le système socio-fiscal complet pour lire quelques tarifs coûte
# plusieurs minutes (l'arbre des majorations régionales TICPE est volumineux) :
# on lit donc les fichiers de paramètres directement.
# --------------------------------------------------------------------------


def _date(cle: object) -> datetime.date:
    if isinstance(cle, datetime.date):
        return cle
    return datetime.date.fromisoformat(str(cle))


def valeur_parametre(chemin_parametre: str, millesime: int, mois: int = 1) -> float | None:
    """Valeur d'un paramètre du barème à une date, par lecture directe du YAML.

    `chemin_parametre` suit la notation OpenFisca, par exemple
    « energies.gaz_naturel.accise.carburants.tarif_normal ».
    """
    import yaml

    segments = chemin_parametre.split(".")
    for coupure in range(len(segments), 0, -1):
        chemin_fichier = os.path.join(CHEMIN_PARAMETRES, *segments[:coupure]) + ".yaml"
        if os.path.exists(chemin_fichier):
            reste = segments[coupure:]
            break
    else:
        return None

    with open(chemin_fichier, encoding="utf-8") as fichier:
        document = yaml.safe_load(fichier)
    for cle in reste:
        if not isinstance(document, dict) or cle not in document:
            return None
        document = document[cle]
    if not isinstance(document, dict) or "values" not in document:
        return None

    reference = datetime.date(millesime, mois, 1)
    retenue = None
    for cle in sorted(document["values"], key=_date):
        if _date(cle) <= reference:
            retenue = document["values"][cle]
    if isinstance(retenue, dict):
        return retenue.get("value")
    return retenue
