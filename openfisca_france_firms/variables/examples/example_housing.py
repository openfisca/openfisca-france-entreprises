"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import UniteLegale


# This variable is a pure input: it doesn't have a formula
class example_accommodation_size(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "Size of the accommodation, in square metres"


# This variable is a pure input: it doesn't have a formula
class example_rent(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "Rent paid by the unite_legale"


# Possible values for the housing_occupancy_status variable, defined further down
# See more at <https://openfisca.org/doc/coding-the-legislation/20_input_variables.html#advanced-example-enumerations-enum>
class example_HousingOccupancyStatus(Enum):
    __order__ = "owner tenant free_lodger homeless"
    owner = "Owner"
    tenant = "Tenant"
    free_lodger = "Free lodger"
    homeless = "Homeless"


class example_housing_occupancy_status(Variable):
    value_type = Enum
    possible_values = example_HousingOccupancyStatus
    default_value = example_HousingOccupancyStatus.tenant
    entity = UniteLegale
    definition_period = MONTH
    label = "Legal housing situation of the unite_legale concerning their main residence"


class example_postal_code(Variable):
    value_type = str
    max_length = 5
    entity = UniteLegale
    definition_period = MONTH
    label = "Postal code of the unite_legale"
