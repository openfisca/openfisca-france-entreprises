from openfisca_core.model_api import *
from openfisca_france_firms.entities import Establishment  # noqa F401

class consumption_natural_gas(Variable):
    value_type = float
    unit = 'MWh'
    entity = Establishment
    label = "Natural gas consumption of the establishment"
    definition_period = YEAR

class consumption_coal(Variable):
    value_type = float
    unit = 'tep'
    entity = Establishment
    label = "Coal consumption of the establishment"
    definition_period = YEAR

class consumption_heavy_fuel(Variable):
    value_type = float
    unit = 'tep'
    entity = Establishment
    label = "Heavy fuel consumption of the establishment"
    definition_period = YEAR

class consumption_light_fuel(Variable):
    value_type = float
    unit = 'tep'
    entity = Establishment
    label = "Heavy fuel consumption of the establishment"
    definition_period = YEAR

