"""Shared vectorized logical helpers for taxation energy formulas."""

from functools import reduce

import numpy as np
from numpy import logical_and, logical_or
from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.model_api import MONTH, not_

_ABSENT = object()


def tarif_moyen_annuel(period, lire_tarif, defaut_si_absent=_ABSENT):
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

    Abrogation en cours d'année : si un produit est retiré du tarif (paramètre clôturé par
    ``value: null``) à une date infra-annuelle, passer ``defaut_si_absent=0`` fait compter zéro
    pour les mois postérieurs à la clôture — la moyenne reflète alors correctement les mois taxés
    puis les mois abrogés. Sans cet argument, un mois clôturé lève ``ParameterNotFoundError``,
    ce qui reste voulu ailleurs pour détecter une lecture de tarif avant son existence.

    :param period: la période annuelle de la formule appelante.
    :param lire_tarif: fonction prenant une période mensuelle et renvoyant le tarif applicable,
        typiquement ``lambda mois: parameters(mois).energies...``.
    :param defaut_si_absent: valeur substituée aux mois où le paramètre est absent/clôturé ;
        par défaut l'absence propage l'erreur.
    """
    mois = list(period.get_subperiods(MONTH))

    def _lire(m):
        if defaut_si_absent is _ABSENT:
            return lire_tarif(m)
        try:
            return lire_tarif(m)
        except ParameterNotFoundError:
            return defaut_si_absent

    return sum(_lire(m) for m in mois) / len(mois)


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
