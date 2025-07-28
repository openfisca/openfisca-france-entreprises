"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class apen(Enum):
    value_type = str
    max_length = 5
    entity = UniteLegale
    definition_period = MONTH
    label = "Sector of the unite_legale"
    set_input = set_input_dispatch_by_period


class postal_code_unite_legale(Variable):
    value_type = str
    max_length = 5
    entity = UniteLegale
    definition_period = MONTH
    label = "Postal code of the unite_legale"

    """
    We define the unite_legale's postal code as the unite_legale's siege_social etablissement's postal code.
    """

    def formula(unite_legale, period):
        hq = unite_legale.members(has_role ="siege_social")

        return hq("postal_code", period)


class effectif_3112_ul(Variable):
    #le nombre de personnes qui travaillent 
    value_type = float
    entity = UniteLegale
    label = "Effectifs en fin d'année, ETP, au niveau d'unité legale"
    definition_period = YEAR