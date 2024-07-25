"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Establishment, a Firm…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import Firm, Establishment


class gas_consumption_tax(Variable):
    value_type = float
    entity = Establishment
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://law.gov.example/example_income_tax_flat"  # Always use the most official source

    def formula(establishment, period, parameters):
        """
        Income tax.

        The formula to compute the income tax for a given establishment at a given period
        """
        return establishment("gas_consumption", period) * parameters(period).energy.natural_gas
