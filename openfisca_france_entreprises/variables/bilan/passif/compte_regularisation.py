"""Variables and formulas for this module."""

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import UniteLegale


class produits_constates_avance(Variable):
    cerfa_field = "EB"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits constatés d'avance"
    definition_period = YEAR
