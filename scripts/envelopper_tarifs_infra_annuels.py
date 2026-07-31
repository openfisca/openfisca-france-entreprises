"""Enveloppe dans `tarif_moyen_annuel` les lectures de tarifs entrant en vigueur en cours d'année.

Le modèle raisonne en périodes annuelles et lit chaque tarif au 1er janvier : un tarif qui change
en cours d'année bascule donc toute l'année sur un seul de ses deux niveaux. Ce script réécrit ces
lectures pour qu'elles passent par la moyenne mensuelle.

Il s'appuie sur `audit_tarifs_infra_annuels.py` pour la liste des paramètres concernés et la
localisation AST de leurs lectures (alias et appels multi-lignes résolus), puis remplace des
tranches de source — et non l'AST reconstruit — afin de préserver commentaires et mise en forme.
Les remplacements sont appliqués de la fin vers le début du fichier pour que les décalages restent
valides.

Le résultat doit être repassé à `ruff format`.

Usage : python scripts/envelopper_tarifs_infra_annuels.py [--dry-run]
"""

import argparse
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_tarifs_infra_annuels import (  # noqa: E402
    FORMULES,
    Visiteur,
    infra_annuels,
)

# Sites où la moyenne doit compter zéro (ou un tarif de repli) sur les mois où le paramètre
# n'existe pas — abrogations et créations infra-annuelles tranchées dans
# ARBITRAGES_JURIDIQUES_ENERGIES.md. Clé : nœud de paramètre ; valeur : expression de repli.
DEFAUTS = {
    # §5 — l'émulsion eau-gazole quitte le tableau B de l'article 265 du code des douanes au
    # 2020-07-01 : plus de tarif propre ensuite, les mois postérieurs comptent zéro.
    "autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres": "0",
    "autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions": "0",
}


def enveloppe(noeud, indentation):
    """Texte remplaçant une lecture, indenté pour s'insérer à la place de l'expression."""
    marge = " " * indentation
    defaut = DEFAUTS.get(noeud)
    lignes = [
        "tarif_moyen_annuel(",
        f"{marge}    period,",
        f"{marge}    lambda mois: parameters(mois).energies.{noeud},",
    ]
    if defaut is not None:
        lignes.append(f"{marge}    defaut_si_absent={defaut},")
    lignes.append(f"{marge})")
    return "\n".join(lignes)


def cibles_du_fichier(chemin, infra):
    """Nœuds AST à remplacer, avec leur nœud de paramètre résolu."""
    source = chemin.read_text(encoding="utf-8")
    v = Visiteur(chemin.name)
    v.visit(ast.parse(source))
    out = []
    for noeud_ast, chemin_param, _periode, deja in v.lectures_ast:
        if deja:
            continue
        cible = None
        for candidat in infra:
            if chemin_param == candidat or chemin_param.startswith(candidat + "."):
                if cible is None or len(candidat) > len(cible):
                    cible = candidat
        if cible:
            out.append((noeud_ast, cible))
    return source, out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    infra = infra_annuels()
    total = 0
    for chemin in sorted(FORMULES.glob("*.py")):
        source, cibles = cibles_du_fichier(chemin, infra)
        if not cibles:
            continue
        lignes = source.splitlines(keepends=True)
        debuts = [0]
        for ligne in lignes:
            debuts.append(debuts[-1] + len(ligne))

        def offset(lineno, col):
            return debuts[lineno - 1] + col

        # de la fin vers le début : les décalages amont restent valides
        remplacements = sorted(
            cibles,
            key=lambda c: (c[0].lineno, c[0].col_offset),
            reverse=True,
        )
        texte = source
        for noeud_ast, param in remplacements:
            debut = offset(noeud_ast.lineno, noeud_ast.col_offset)
            fin = offset(noeud_ast.end_lineno, noeud_ast.end_col_offset)
            texte = texte[:debut] + enveloppe(param, noeud_ast.col_offset) + texte[fin:]
        total += len(remplacements)
        print(f"  {len(remplacements):4d}  {chemin.name}")
        if not a.dry_run:
            chemin.write_bytes(texte.encode("utf-8").replace(b"\r\n", b"\n"))

    print(f"\n{total} lectures enveloppées" + (" (simulation)" if a.dry_run else ""))
    print("Repasser `uv run ruff format` sur les fichiers modifiés.")


if __name__ == "__main__":
    main()
