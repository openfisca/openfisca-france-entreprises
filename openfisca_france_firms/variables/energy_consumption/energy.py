from openfisca_core.model_api import *
from openfisca_france_firms.entities import Establishment  # noqa F401

class gas_consumption(Variable):
    cerfa_field = "DM"
    value_type = int
    unit = 'currency'
    entity = Establishment
    label = "Natural gas consumption of the establishment"
    definition_period = YEAR
