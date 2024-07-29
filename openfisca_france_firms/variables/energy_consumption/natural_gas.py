from openfisca_core.model_api import *
from openfisca_france_firms.entities import Establishment  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class consumption_natural_gas(Variable):
    value_type = float
    unit = 'MWh'
    entity = Establishment
    label = "Natural gas consumption of the establishment"
    definition_period = YEAR

