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
        "#\n"
        "# Les variables de consommation étant mensuelles, la quantité n'est pas répartie\n"
        "# sur l'année mais posée sur un mois où s'applique le tarif que la case déclare.\n"
        "# Une case de la 2040-TIC est en effet une cellule tarifaire homogène : elle porte\n"
        "# la quantité taxée à *son* tarif, qu'elle nomme souvent dans son propre libellé.\n"
        "# La répartir sur douze mois ferait calculer au modèle une moyenne annuelle que la\n"
        "# déclaration ne pratique jamais.\n"
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
    note_entree: str = "",
) -> str:
    lignes = [f"# {ligne}" for ligne in alerte.splitlines()]
    lignes += [f'- name: "{nom}"', f"  period: {periode}", f"  absolute_error_margin: {marge:.6g}", "  input:"]
    if note_entree:
        lignes.extend(f"    # {ligne}" for ligne in note_entree.splitlines())
    for cle, valeur in entrees.items():
        if isinstance(valeur, dict):
            lignes.append(f"    {cle}:")
            lignes.extend(f'      "{sous_periode}": {_litteral(v)}' for sous_periode, v in valeur.items())
        else:
            lignes.append(f"    {cle}: {_litteral(valeur)}")
    lignes.append("  output:")
    lignes.append(f"    # {commentaire}")
    lignes.append(f"    {variable}: {attendu:.2f}")
    return "\n".join(lignes) + "\n\n"


def _mois_du_tarif(cellule: correspondance.Cellule, annee: int, implicite: float) -> int | None:
    """Premier mois de l'année où le barème porte le tarif que la case déclare.

    Une case de la 2040-TIC est une cellule tarifaire homogène : elle porte la quantité
    taxée à *son* tarif, souvent nommé dans son propre libellé. Depuis que les variables
    de consommation sont mensuelles, la quantité peut donc être posée sur un mois où ce
    tarif s'applique, plutôt que répartie sur l'année — ce qui faisait autrefois calculer
    au modèle une moyenne annuelle que la déclaration ne pratique jamais.

    Renvoie None quand aucun mois de l'année ne porte le tarif déclaré : c'est alors un
    désaccord de fond entre la déclaration et le barème, pas un artefact d'annualisation.
    """
    if cellule.parametre is None:
        return None
    for mois in range(1, 13):
        barometre = donnees.valeur_parametre(cellule.parametre, annee, mois=mois)
        if barometre is None:
            continue
        if cellule.parametre_majoration:
            # Majoration ZNI : la declaration separe la fraction de droit commun et la
            # majoration en deux cases de montant, mais le tarif de la cellule est leur somme.
            barometre += donnees.valeur_parametre(cellule.parametre_majoration, annee, mois=mois) or 0
        if abs(implicite - barometre) <= 1e-4 * max(abs(barometre), 1.0):
            return mois
    return None


def _desaccords(
    cellule: correspondance.Cellule,
    implicite: float,
    periode: int,
    mois: int | None,
) -> list[tuple[str, str]]:
    """Les désaccords chiffrables entre la cellule déclarée et le calculateur.

    Renvoie une liste de couples (résumé d'une ligne, texte long pour le YAML). Une
    cellule peut en cumuler plusieurs.
    """
    trouves = []

    if cellule.constat:
        trouves.append((
            "constat de modélisation",
            "DÉSACCORD — le modèle ne restitue pas cette cellule.\n"
            + "\n".join(textwrap.wrap(cellule.constat, 76)),
        ))

    if mois is None:
        barometre = (
            next(
                (
                    valeur
                    for valeur in (
                        donnees.valeur_parametre(cellule.parametre, periode, mois=m) for m in range(1, 13)
                    )
                    if valeur is not None
                ),
                None,
            )
            if cellule.parametre
            else None
        )
        au_bareme = f"{barometre:.4f}" if barometre is not None else "absent du barème"
        resume = (
            f"tarif déclaré {implicite:.4f}, absent du barème"
            if barometre is None
            else f"tarif déclaré {implicite:.4f} contre {au_bareme} au barème"
        )
        trouves.append((
            resume,
            "DÉSACCORD — le tarif déclaré ne concorde avec aucun mois du barème.\n"
            f"La déclaration applique {implicite:.4f} €/MWh ; le barème porte {au_bareme}.\n"
            "Aucun des douze mois de l'année ne porte le tarif déclaré : ce n'est donc\n"
            "pas un artefact d'annualisation, mais un désaccord de fond.\n"
            "La déclaration fait foi : c'est le barème qu'il faut instruire.",
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
            periode = cellule.annee_tarif or millesime

            # La quantité se pose sur un mois où s'applique le tarif que la case déclare.
            # À défaut — aucun mois ne porte ce tarif —, elle se pose sur janvier, et le
            # désaccord avec le barème apparaît sans être mêlé d'annualisation.
            mois = _mois_du_tarif(cellule, periode, implicite)
            sous_periode = f"{periode}-{(mois or 1):02d}"
            if mois is not None:
                note_entree = (
                    f"Quantité posée sur {sous_periode}, mois où le barème porte le tarif\n"
                    f"déclaré de {implicite:.4f} €/MWh."
                )
            else:
                note_entree = (
                    f"Aucun mois de {periode} ne porte le tarif déclaré : la quantité est posée\n"
                    f"sur {sous_periode}, ce qui isole le désaccord de barème."
                )
            entrees = {
                cle: ({sous_periode: quantite} if valeur == correspondance.ASSIETTE else valeur)
                for cle, valeur in cellule.entrees.items()
            }

            trouves = _desaccords(cellule, implicite, periode, mois)
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
                note_entree=note_entree,
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
