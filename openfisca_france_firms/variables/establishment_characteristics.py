"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Establishment, a Firm…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import Firm, Establishment

class apet(Variable):
    value_type = str
    entity = Establishment
    label = "Effectifs en fin d'année, ETP"
    definition_period = YEAR
    set_input = set_input_dispatch_by_period

class postal_code(Variable):
    value_type = str
    max_length = 5
    entity = Establishment
    definition_period = MONTH
    label = "Postal code of the establishment"

class effectif_3112_et(Variable):
    value_type = float
    entity = Establishment
    label = "Effectifs en fin d'année, ETP"
    definition_period = YEAR
    set_input = set_input_dispatch_by_period

