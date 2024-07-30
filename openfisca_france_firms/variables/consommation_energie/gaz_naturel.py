from openfisca_core.model_api import *
from openfisca_france_firms.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class consommation_gaz_naturel(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Natural gas consumption of the etablissement"
    definition_period = YEAR

