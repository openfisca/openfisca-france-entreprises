"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

from datetime import date

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import where

from openfisca_core.periods import ETERNITY, MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import Etablissement


# This variable is a pure input: it doesn't have a formula
class example_birth(Variable):
    value_type = date
    default_value = date(1970, 1, 1)  # By default, if no value is set for a simulation, we consider the people involved in a simulation to be born on the 1st of Jan 1970.
    entity = Etablissement
    label = "example_birth date"
    definition_period = ETERNITY  # This variable cannot change over time.
    reference = "https://en.wiktionary.org/wiki/example_birthdate"


class example_age(Variable):
    value_type = int
    entity = Etablissement
    definition_period = MONTH
    label = "Etablissement's example_age (in years)"

    def formula(etablissement, period, _parameters):
        """
        Etablissement's example_age (in years).

        A etablissement's example_age is computed according to its example_birth date.
        """
        example_birth = etablissement("example_birth", period)
        example_birth_year = example_birth.astype("datetime64[Y]").astype(int) + 1970
        example_birth_month = example_birth.astype("datetime64[M]").astype(int) % 12 + 1
        example_birth_day = (example_birth - example_birth.astype("datetime64[M]") + 1).astype(int)

        is_example_birthday_past = (example_birth_month < period.start.month) + (example_birth_month == period.start.month) * (example_birth_day <= period.start.day)

        return (period.start.year - example_birth_year) - where(is_example_birthday_past, 0, 1)  # If the example_birthday is not passed this year, subtract one year
