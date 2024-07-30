"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.holders import set_input_divide_by_period
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import Etablissement


# This variable is a pure input: it doesn't have a formula
class example_salary(Variable):
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    set_input = set_input_divide_by_period  # Optional attribute. Allows user to declare a example_salary for a year. OpenFisca will spread the yearly amount over the months contained in the year.
    label = "example_salary"
    reference = "https://law.gov.example/example_salary"  # Always use the most official source


class example_disposable_income(Variable):
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    label = "Actual amount available to the etablissement at the end of the month"
    reference = "https://stats.gov.example/example_disposable_income"  # Some variables represent quantities used in economic models, and not defined by law. Always give the source of your definitions.

    def formula(etablissement, period, _parameters):
        """Disposable income."""
        return (
            + etablissement("example_salary", period)
            + etablissement("example_basic_income", period)
            - etablissement("example_income_tax_flat", period)
            - etablissement("example_income_tax_progressive", period)
            )
