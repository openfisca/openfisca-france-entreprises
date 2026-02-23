"""Shared vectorized logical helpers for taxation energy formulas."""

from functools import reduce

import numpy as np
from numpy import logical_and, logical_or
from openfisca_core.model_api import not_


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
    departement = etablissement("departement", period).astype(str)
    commune = etablissement("commune", period).astype(str)
    key = departement + "_" + commune
    # Permettre de tester la clé "manquant" via (manqu, ant)
    return np.where((departement == "manqu") & (commune == "ant"), "manquant", key)
