from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_entreprises.entities import UniteLegale  # noqa F401


class produits_constates_avance(Variable):
    cerfa_field = "EB"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits constatés d'avance"
    definition_period = YEAR
