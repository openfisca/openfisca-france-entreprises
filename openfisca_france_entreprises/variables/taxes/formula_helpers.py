"""Shared vectorized logical helpers for taxation energy formulas."""

from functools import reduce

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
