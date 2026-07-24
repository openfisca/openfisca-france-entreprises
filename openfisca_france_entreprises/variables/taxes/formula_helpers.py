"""Shared vectorized logical helpers for taxation energy formulas."""

from functools import reduce

import numpy as np
from numpy import logical_and, logical_or
from openfisca_core.model_api import MONTH, not_


def tarif_moyen_annuel(period, lire_tarif):
    """Moyenne mensuelle d'un tarif sur l'année.

    Le modèle raisonne en périodes annuelles, mais de nombreux tarifs entrent en vigueur en
    cours d'année (TICC au 2014-04-01, TICGN, tarifs d'accise au 2025-02-01, bouclier au
    2023-02-01…). Lire le paramètre au 1er janvier applique alors le tarif ancien — ou le
    nouveau — à toute l'année.

    La consommation étant répartie uniformément sur l'année, la taxe due vaut
    ``somme sur les mois (conso / 12 * tarif du mois)``, soit ``conso * moyenne des tarifs``.
    Cette fonction renvoie cette moyenne, de sorte que les formules conservent leur forme
    ``assiette * tarif`` tout en devenant exactes sur les entrées en vigueur infra-annuelles.

    Exemple - TICC 2014 (1,19 jusqu'au 31 mars, 2,29 a partir du 1er avril) : la moyenne vaut
    (3 * 1,19 + 9 * 2,29) / 12 = 2,015, au lieu de 1,19 en lisant le seul 1er janvier.

    :param period: la période annuelle de la formule appelante.
    :param lire_tarif: fonction prenant une période mensuelle et renvoyant le tarif applicable,
        typiquement ``lambda mois: parameters(mois).energies...``.
    """
    mois = list(period.get_subperiods(MONTH))
    return sum(lire_tarif(m) for m in mois) / len(mois)


def _and(*args):
    """Vectorized logical and over two or more arrays."""
    r = args[0]
    for a in args[1:]:
        r = logical_and(r, a)
    return r


def _or(*args):
    """Vectorized logical or over two or more arrays."""
    r = args[0]
    for a in args[1:]:
        r = logical_or(r, a)
    return r


def _not(x):
    """Vectorized logical not."""
    return not_(x)


def _dep_in(departement, codes):
    """Vectorized: True where departement is in codes."""
    if len(codes) == 1:
        return departement == codes[0]
    return reduce(lambda a, b: a | b, (departement == c for c in codes))


def departement_commune(etablissement, period):
    """Clé (département, commune) pour indexation des paramètres TCCFE/TDCFE.

    Retourne le vecteur au format "dep_commune" (ex. "1_1", "02A_123").
    Pour les tests : (dep="manqu", commune="ant") retourne "manquant".
    """
    dep = etablissement("departement", period).astype("U32")
    comm = etablissement("commune", period).astype("U32")
    key = np.char.add(np.char.add(dep, "_"), comm)
    return np.where((dep == "manqu") & (comm == "ant"), "manquant", key)
