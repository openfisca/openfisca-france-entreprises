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

class apen(Enum):
    value_type = str
    max_length = 5
    entity = Firm
    definition_period = MONTH
    label = "Sector of the firm"
    set_input = set_input_dispatch_by_period

class postal_code_firm(Variable):
    value_type = str
    max_length = 5
    entity = Firm
    definition_period = MONTH
    label = "Postal code of the firm"

    """
    We define the firm's postal code as the firm's headquarter establishment's postal code.
    """

    def formula(firm, period):
        hq = firm.members(has_role ="headquarters")

        return hq("postal_code", period)
