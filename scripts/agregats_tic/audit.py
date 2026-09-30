"""Confrontation des agrégats 2040-TIC au barème et au modèle.

Usage :
    .venv/bin/python -m scripts.agregats_tic.audit
"""

from __future__ import annotations

import sys

from . import correspondance, donnees

TOLERANCE_RELATIVE = 1e-4


def _formate(valeur: float | None, largeur: int = 10) -> str:
    return "—".rjust(largeur) if valeur is None else f"{valeur:>{largeur}.4f}"


def audit_tarifs(valeurs, libelles) -> list[str]:
    """Compare, cellule par cellule, le tarif implicite au paramètre du barème."""
    anomalies = []
    print("\n" + "=" * 118)
    print("TARIFS IMPLICITES (montant / quantité) CONFRONTÉS AU BARÈME")
    print("=" * 118)
    print(f"{'case':9} {'mill.':6} {'implicite':>11} {'barème':>11} {'écart':>10}  intitulé")
    print("-" * 118)

    for cellule in correspondance.CELLULES:
        for millesime in cellule.millesimes:
            implicite = donnees.tarif_implicite(
                valeurs,
                millesime,
                cellule.case_quantite,
                cellule.cases_montant,
            )
            if implicite is None:
                continue
            # Le tarif d'une case est celui de son millésime d'ouverture, pas celui
            # de l'année de dépôt : c'est `annee_tarif` qui fait foi quand il est posé.
            annee = cellule.annee_tarif or millesime
            # Les tarifs de l'année sont fixés en février pour l'électricité et le
            # gaz (sortie du bouclier) : on retient la valeur applicable en février.
            barometre = cellule.parametre and donnees.valeur_parametre(
                cellule.parametre,
                annee,
                mois=2,
            )
            if barometre is None and cellule.parametre:
                barometre = donnees.valeur_parametre(cellule.parametre, annee, mois=1)

            if barometre is None:
                verdict = "absent du barème"
                anomalies.append(f"{cellule.case_quantite} {millesime} : {verdict} ({cellule.intitule})")
                ecart = None
            else:
                ecart = implicite - barometre
                concordant = abs(ecart) <= TOLERANCE_RELATIVE * max(abs(barometre), 1.0)
                verdict = "" if concordant else "ÉCART"
                if not concordant:
                    anomalies.append(
                        f"{cellule.case_quantite} {millesime} : implicite {implicite:.4f} "
                        f"vs barème {barometre:.4f} ({cellule.intitule})",
                    )
            print(
                f"{cellule.case_quantite:9} {millesime:<6} {_formate(implicite, 11)} "
                f"{_formate(barometre, 11)} {_formate(ecart):>10}  {cellule.intitule[:52]}"
                + (f"  <-- {verdict}" if verdict else ""),
            )
    return anomalies


def audit_exonerations(valeurs, libelles) -> None:
    print("\n" + "=" * 118)
    print("EXONÉRATIONS ET EXEMPTIONS (quantités déclarées sans montant)")
    print("=" * 118)
    for exoneration in correspondance.EXONERATIONS:
        quantites = " ".join(
            f"{millesime}={valeurs.get(millesime, {}).get(exoneration.case, 0):,.0f}"
            for millesime in sorted(valeurs)
        )
        couverture = exoneration.variable or "NON COUVERT"
        print(f"  {exoneration.case:9} {exoneration.intitule[:56]:58} {couverture:38} {quantites}")


def audit_totaux(valeurs) -> list[str]:
    print("\n" + "=" * 118)
    print("IDENTITÉS COMPTABLES DÉCLARÉES (total = somme des composantes)")
    print("=" * 118)
    anomalies = []
    for case_total, definition in correspondance.TOTAUX.items():
        print(f"\n  {case_total}  {definition['intitule']}")
        for millesime, composantes in sorted(definition["composantes"].items()):
            total = valeurs.get(millesime, {}).get(case_total)
            if total is None:
                continue
            somme = sum(valeurs[millesime].get(case, 0.0) for case in composantes)
            ecart = total - somme
            # Les agrégats sont sommés depuis le fichier micro : quelques MWh de
            # résidu d'arrondi sont attendus sur des totaux à neuf chiffres.
            concordant = abs(ecart) <= max(100.0, 1e-5 * abs(total))
            marque = "ok " if concordant else "ÉCART"
            print(
                f"     {marque} {millesime} : somme {somme:>18,.2f} | déclaré {total:>18,.2f} "
                f"| écart {ecart:>14,.2f}",
            )
            if not concordant:
                anomalies.append(f"{case_total} {millesime} : écart de {ecart:,.2f}")
    return anomalies


def audit_couverture(valeurs, libelles) -> None:
    """Cases appariables non encore rattachées à une variable du modèle."""
    couples = donnees.apparier(libelles)
    cartographiees = {cellule.case_quantite for cellule in correspondance.CELLULES}
    print("\n" + "=" * 118)
    print("COUVERTURE : cellules tarifaires non cartographiées")
    print("=" * 118)
    manquantes = 0
    for case_quantite, cases_montant in couples:
        if case_quantite in cartographiees:
            continue
        tarifs = {
            millesime: donnees.tarif_implicite(valeurs, millesime, case_quantite, cases_montant)
            for millesime in sorted(valeurs)
        }
        actifs = {m: t for m, t in tarifs.items() if t}
        if not actifs:
            continue  # cellule déclarée mais jamais servie : rien à tester
        manquantes += 1
        resume = " ".join(f"{m}={t:.4f}" for m, t in actifs.items())
        print(f"  {case_quantite:9} {libelles[case_quantite][:70]:72} {resume}")
    print(f"\n  → {manquantes} cellules servies restent hors correspondance.")

    sans_variable = [c for c in correspondance.CELLULES if c.variable is None]
    print(f"\n  → {len(sans_variable)} cellules cartographiées mais non restituables par le modèle :")
    for cellule in sans_variable:
        print(f"     {cellule.case_quantite}  {cellule.intitule}")
        print(f"                {cellule.remarque}")


def principal() -> int:
    observations = donnees.charger()
    valeurs, libelles = donnees.indexer(observations)

    print(f"Agrégats 2040-TIC : {len(observations)} lignes, {len(libelles)} cases, "
          f"millésimes {min(valeurs)}–{max(valeurs)}")

    anomalies_tarifs = audit_tarifs(valeurs, libelles)
    audit_exonerations(valeurs, libelles)
    anomalies_totaux = audit_totaux(valeurs)
    audit_couverture(valeurs, libelles)

    print("\n" + "=" * 118)
    print("SYNTHÈSE")
    print("=" * 118)
    print(f"  {len(anomalies_tarifs)} écarts de tarif :")
    for anomalie in anomalies_tarifs:
        print(f"     - {anomalie}")
    print(f"  {len(anomalies_totaux)} écarts d'identité comptable :")
    for anomalie in anomalies_totaux:
        print(f"     - {anomalie}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
