"""Génération des tests OpenFisca à partir des agrégats 2040-TIC.

Chaque case de la déclaration est une cellule tarifaire homogène : un couple
(produit, régime, tarif). L'accise y étant linéaire, l'agrégat sur l'ensemble
des redevables se comporte comme un redevable unique. On peut donc injecter la
quantité agrégée comme assiette et attendre le montant agrégé.

Ne sont émises que les cellules dont le tarif implicite concorde avec le barème :
les autres sont des désaccords à arbitrer, recensés par `audit.py` et le rapport,
et il serait trompeur de les figer en tests.

Usage :
    .venv/bin/python -m scripts.agregats_tic.generer_tests
"""

from __future__ import annotations

import os
import sys

from . import correspondance, donnees

DESTINATION = os.path.join(
    donnees.RACINE,
    "openfisca_france_entreprises",
    "tests",
    "taxes",
    "taxes_energies",
    "agregats",
)

# Les montants agrégés portent sur des centaines de millions d'euros : une
# tolérance relative serait plus juste, mais OpenFisca ne propose qu'une marge
# absolue. On la cale sur l'ordre de grandeur du montant attendu.
TOLERANCE_RELATIVE = 1e-6


def _litteral(valeur: object) -> str:
    if isinstance(valeur, bool):
        return "true" if valeur else "false"
    if isinstance(valeur, float) and valeur.is_integer():
        return str(int(valeur))
    return str(valeur)


def _entete(titre: str) -> str:
    return (
        f"# {titre}\n"
        "#\n"
        "# Fichier généré par scripts/agregats_tic/generer_tests.py — ne pas éditer à la main.\n"
        "# Source : assets/agregats.csv, agrégats annuels de la déclaration 2040-TIC\n"
        "# déposée par les fournisseurs d'énergie.\n"
        "#\n"
        "# Chaque cas reprend la quantité et le montant réellement déclarés pour une case\n"
        "# et un millésime. Le millésime est l'année de dépôt ; la période du test est\n"
        "# l'année du tarif porté par la case.\n"
        "\n"
    )


def _cas(
    nom: str,
    periode: int,
    entrees: dict[str, object],
    variable: str,
    attendu: float,
    marge: float,
    commentaire: str,
) -> str:
    lignes = [f'- name: "{nom}"', f"  period: {periode}", f"  absolute_error_margin: {marge:.6g}", "  input:"]
    lignes.extend(f"    {cle}: {_litteral(valeur)}" for cle, valeur in entrees.items())
    lignes.append("  output:")
    lignes.append(f"    # {commentaire}")
    lignes.append(f"    {variable}: {attendu:.2f}")
    return "\n".join(lignes) + "\n\n"


def _concordante(cellule: correspondance.Cellule, implicite: float, millesime: int) -> bool:
    if cellule.parametre is None:
        return False
    annee = cellule.annee_tarif or millesime
    for mois in (2, 1):
        barometre = donnees.valeur_parametre(cellule.parametre, annee, mois=mois)
        if barometre is not None:
            return abs(implicite - barometre) <= 1e-4 * max(abs(barometre), 1.0)
    return False


def generer_cellules(valeurs, libelles) -> tuple[str, int, list[str]]:
    contenu = _entete("Cellules tarifaires — quantité déclarée → montant déclaré")
    nombre = 0
    ecartees: list[str] = []

    for cellule in correspondance.CELLULES:
        if cellule.constat:
            ecartees.append(f"{cellule.case_quantite} : {cellule.constat}")
            continue
        if cellule.variable is None or not cellule.entrees:
            ecartees.append(f"{cellule.case_quantite} : {cellule.remarque or 'non restituable par le modèle'}")
            continue
        for millesime in cellule.millesimes:
            quantite = valeurs.get(millesime, {}).get(cellule.case_quantite)
            if not quantite:
                continue
            montant = sum(
                valeurs[millesime].get(case, 0.0) for case in cellule.cases_montant
            )
            implicite = montant / quantite
            if not _concordante(cellule, implicite, millesime):
                ecartees.append(
                    f"{cellule.case_quantite} {millesime} : tarif implicite {implicite:.4f} "
                    f"non concordant avec le barème",
                )
                continue

            entrees = {
                cle: (quantite if valeur == correspondance.ASSIETTE else valeur)
                for cle, valeur in cellule.entrees.items()
            }
            periode = cellule.annee_tarif or millesime
            contenu += _cas(
                nom=f"{cellule.case_quantite} — {cellule.intitule} (millésime {millesime})",
                periode=periode,
                entrees=entrees,
                variable=cellule.variable,
                attendu=montant,
                marge=max(1.0, TOLERANCE_RELATIVE * abs(montant)),
                commentaire=f"{quantite:,.0f} MWh × {implicite:.4f} €/MWh",
            )
            nombre += 1
    return contenu, nombre, ecartees


def generer_exonerations(valeurs, libelles) -> tuple[str, int]:
    contenu = _entete("Exonérations et exemptions — quantité déclarée, accise nulle")
    nombre = 0
    for exoneration in correspondance.EXONERATIONS:
        if exoneration.variable is None:
            continue
        for millesime in sorted(valeurs):
            quantite = valeurs[millesime].get(exoneration.case)
            if not quantite:
                continue
            entrees = {
                cle: (quantite if valeur == correspondance.ASSIETTE else valeur)
                for cle, valeur in exoneration.entrees.items()
            }
            contenu += _cas(
                nom=f"{exoneration.case} — {exoneration.intitule} (millésime {millesime})",
                periode=millesime,
                entrees=entrees,
                variable=exoneration.variable,
                attendu=0.0,
                marge=1.0,
                commentaire=f"{quantite:,.0f} MWh déclarés en quantités exemptées : accise nulle",
            )
            nombre += 1
    return contenu, nombre


def principal() -> int:
    observations = donnees.charger()
    valeurs, libelles = donnees.indexer(observations)
    os.makedirs(DESTINATION, exist_ok=True)

    contenu_cellules, nombre_cellules, ecartees = generer_cellules(valeurs, libelles)
    chemin = os.path.join(DESTINATION, "test_cellules_tarifaires.yaml")
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(contenu_cellules.rstrip("\n") + "\n")
    print(f"{nombre_cellules:3d} cas écrits dans {os.path.relpath(chemin, donnees.RACINE)}")

    contenu_exonerations, nombre_exonerations = generer_exonerations(valeurs, libelles)
    chemin = os.path.join(DESTINATION, "test_exonerations.yaml")
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(contenu_exonerations.rstrip("\n") + "\n")
    print(f"{nombre_exonerations:3d} cas écrits dans {os.path.relpath(chemin, donnees.RACINE)}")

    print(f"\n{len(ecartees)} cellules écartées (désaccord à arbitrer, voir AGREGATS_TIC.md) :")
    for motif in ecartees:
        print(f"  - {motif}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
