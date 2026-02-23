"""Variables and formulas for this module."""

from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import UniteLegale


class capital_souscrit_non_appele_brut(Variable):
    cerfa_field = "AA"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Capital souscrit non appelé"
    definition_period = YEAR
