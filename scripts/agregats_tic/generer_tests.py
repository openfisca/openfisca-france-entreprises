"""Génération des tests OpenFisca à partir des agrégats 2040-TIC.

Chaque case de la déclaration est une cellule tarifaire homogène : un couple
(produit, régime, tarif). L'accise y étant linéaire, l'agrégat sur l'ensemble
des redevables se comporte comme un redevable unique. On peut donc injecter la
quantité agrégée comme assiette et attendre le montant agrégé.

**Toute cellule que le modèle sait calculer est émise**, y compris quand son résultat
contredit la déclaration : ces cas portent une annotation « DÉSACCORD » et laissent
la suite rouge. Le principe du chantier est que la déclaration fiscale a raison et
que le calculateur — comme le barème — peut avoir tort ; un désaccord rangé hors du
chemin est un désaccord tu.

Seules restent écartées les cellules pour lesquelles le modèle n'a ni variable ni
entrée : il n'y a alors rien à confronter. Ce sont des lacunes de couverture, et
elles sont recensées comme telles par `audit.py` et par AGREGATS_TIC.md.

Usage :
    .venv/bin/python -m scripts.agregats_tic.generer_tests
"""

from __future__ import annotations

import os
import sys
import textwrap

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


def _entete(titre: str, avertissement: str = "") -> str:
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
        f"{avertissement}"
        "\n"
    )


AVERTISSEMENT_DESACCORDS = (
    "#\n"
    "# CERTAINS CAS ÉCHOUENT, ET C'EST VOULU — c'est même la raison d'être du fichier.\n"
    "# Toute cellule que le modèle sait calculer est émise, y compris quand son résultat\n"
    "# contredit la déclaration. Ces cas portent une annotation « DÉSACCORD » qui en dit\n"
    "# la nature et renvoie au constat correspondant d'AGREGATS_TIC.md.\n"
    "#\n"
    "# Le principe : la déclaration fiscale a raison ; le calculateur — et le barème —\n"
    "# peuvent avoir tort. Un désaccord rangé hors du chemin est un désaccord tu.\n"
    "#\n"
    "# Ne pas « réparer » la suite en recalculant ces attendus sur ce que rend le modèle :\n"
    "# ce sont des montants réellement déclarés, ils vérifient le droit. Les aligner sur\n"
    "# le calcul ferait disparaître le désaccord au lieu de le résoudre.\n"
)


def _cas(
    nom: str,
    periode: int,
    entrees: dict[str, object],
    variable: str,
    attendu: float,
    marge: float,
    commentaire: str,
    alerte: str = "",
) -> str:
    lignes = [f"# {ligne}" for ligne in alerte.splitlines()]
    lignes += [f'- name: "{nom}"', f"  period: {periode}", f"  absolute_error_margin: {marge:.6g}", "  input:"]
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


def _moyenne_mensuelle(cellule: correspondance.Cellule, annee: int) -> float | None:
    """Moyenne mensuelle du tarif, si et seulement s'il change au cours de l'année.

    Le modèle lit ses tarifs par `tarif_moyen_annuel`, qui suppose la consommation
    répartie uniformément sur l'année. La déclaration, elle, ségrège les tarifs en
    cases distinctes : une case porte la quantité taxée à *son* tarif, et le nomme
    souvent dans son propre libellé. Les deux conventions ne coïncident que si le
    tarif est constant sur l'année.

    Renvoie la moyenne mensuelle quand le tarif varie — c'est-à-dire la valeur que
    le modèle rendra, à opposer au tarif déclaré — et None quand il est constant,
    auquel cas les deux conventions se rejoignent et le test passe.
    """
    if cellule.parametre is None:
        return None
    valeurs = [donnees.valeur_parametre(cellule.parametre, annee, mois=mois) for mois in range(1, 13)]
    valeurs = [valeur for valeur in valeurs if valeur is not None]
    if len(valeurs) < 12 or len({round(valeur, 6) for valeur in valeurs}) == 1:
        return None
    return sum(valeurs) / len(valeurs)


def _desaccords(
    cellule: correspondance.Cellule,
    implicite: float,
    millesime: int,
    periode: int,
) -> list[tuple[str, str]]:
    """Les désaccords chiffrables entre la cellule déclarée et le calculateur.

    Renvoie une liste de couples (résumé d'une ligne, texte long pour le YAML). Une
    cellule peut en cumuler plusieurs — un constat de modélisation et un tarif
    infra-annuel, par exemple.
    """
    trouves = []

    if cellule.constat:
        trouves.append((
            "constat de modélisation",
            "DÉSACCORD — le modèle ne restitue pas cette cellule.\n"
            + "\n".join(textwrap.wrap(cellule.constat, 76)),
        ))

    if not _concordante(cellule, implicite, millesime):
        annee = cellule.annee_tarif or millesime
        barometre = next(
            (
                valeur
                for valeur in (donnees.valeur_parametre(cellule.parametre, annee, mois=mois) for mois in (2, 1))
                if valeur is not None
            ),
            None,
        ) if cellule.parametre else None
        au_bareme = f"{barometre:.4f}" if barometre is not None else "absent du barème"
        trouves.append((
            f"tarif déclaré {implicite:.4f} contre {au_bareme} au barème",
            "DÉSACCORD — le tarif déclaré ne concorde pas avec le barème.\n"
            f"La déclaration applique {implicite:.4f} €/MWh ; le barème porte {au_bareme}.\n"
            "La déclaration fait foi : c'est le barème qu'il faut instruire.",
        ))

    moyenne = _moyenne_mensuelle(cellule, periode)
    if moyenne is not None:
        ecart = 100 * (moyenne - implicite) / implicite
        trouves.append((
            f"tarif infra-annuel, moyenne mensuelle {moyenne:.4f} ({ecart:+.2f} %)",
            "DÉSACCORD — tarif infra-annuel, voir AGREGATS_TIC.md constat n° 8.\n"
            f"La case déclare {implicite:.4f} €/MWh, constant sur la période qu'elle\n"
            f"couvre ; le tarif du barème, lui, varie dans l'année — moyenne mensuelle\n"
            f"{moyenne:.4f} €/MWh, soit {ecart:+.2f} %.\n"
            "Le cas ÉCHOUE si la formule lit par tarif_moyen_annuel, et passe si elle\n"
            "force un instant, comme le fait le bouclier avec Instant((AAAA, 2, 1)).",
        ))

    return trouves


def generer_cellules(valeurs, libelles) -> tuple[str, int, list[str], list[str]]:
    contenu = _entete(
        "Cellules tarifaires — quantité déclarée → montant déclaré",
        AVERTISSEMENT_DESACCORDS,
    )
    nombre = 0
    ecartees: list[str] = []
    desaccords: list[str] = []

    for cellule in correspondance.CELLULES:
        # Seule exclusion subsistante : le modèle n'a ni variable ni entrée pour
        # cette cellule, donc il n'y a rien à confronter. C'est une lacune de
        # couverture, pas un désaccord — voir « Lacunes de couverture ».
        if cellule.variable is None or not cellule.entrees:
            ecartees.append(f"{cellule.case_quantite} : {cellule.remarque or cellule.constat or 'non restituable par le modèle'}")
            continue
        for millesime in cellule.millesimes:
            quantite = valeurs.get(millesime, {}).get(cellule.case_quantite)
            if not quantite:
                continue
            montant = sum(
                valeurs[millesime].get(case, 0.0) for case in cellule.cases_montant
            )
            implicite = montant / quantite
            entrees = {
                cle: (quantite if valeur == correspondance.ASSIETTE else valeur)
                for cle, valeur in cellule.entrees.items()
            }
            periode = cellule.annee_tarif or millesime

            trouves = _desaccords(cellule, implicite, millesime, periode)
            for resume, _ in trouves:
                desaccords.append(f"{cellule.case_quantite} {periode} — {cellule.intitule} : {resume}")

            contenu += _cas(
                nom=f"{cellule.case_quantite} — {cellule.intitule} (millésime {millesime})",
                periode=periode,
                entrees=entrees,
                variable=cellule.variable,
                attendu=montant,
                marge=max(1.0, TOLERANCE_RELATIVE * abs(montant)),
                commentaire=f"{quantite:,.0f} MWh × {implicite:.4f} €/MWh",
                alerte="\n".join(texte for _, texte in trouves),
            )
            nombre += 1
    return contenu, nombre, ecartees, desaccords


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

    contenu_cellules, nombre_cellules, ecartees, desaccords = generer_cellules(valeurs, libelles)
    chemin = os.path.join(DESTINATION, "test_cellules_tarifaires.yaml")
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(contenu_cellules.rstrip("\n") + "\n")
    print(f"{nombre_cellules:3d} cas écrits dans {os.path.relpath(chemin, donnees.RACINE)}")

    contenu_exonerations, nombre_exonerations = generer_exonerations(valeurs, libelles)
    chemin = os.path.join(DESTINATION, "test_exonerations.yaml")
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(contenu_exonerations.rstrip("\n") + "\n")
    print(f"{nombre_exonerations:3d} cas écrits dans {os.path.relpath(chemin, donnees.RACINE)}")

    print(
        f"\n{len(ecartees)} cellules écartées — lacunes de couverture, le modèle n'a "
        "ni variable ni entrée :",
    )
    for motif in ecartees:
        print(f"  - {motif}")

    if desaccords:
        print(f"\n{len(desaccords)} désaccords émis en test (la suite est rouge, c'est voulu) :")
        for motif in desaccords:
            print(f"  - {motif}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
