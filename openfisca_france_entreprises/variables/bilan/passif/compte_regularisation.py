"""Variables and formulas for this module."""

from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import UniteLegale


class produits_constates_avance(Variable):
    cerfa_field = "EB"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits constatés d'avance"
    definition_period = YEAR
