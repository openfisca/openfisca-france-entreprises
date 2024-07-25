"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Establishment, a Firm…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import Firm


class example_total_benefits(Variable):
    value_type = float
    entity = Firm
    definition_period = MONTH
    label = "Sum of the benefits perceived by a firm"
    reference = "https://stats.gov.example/benefits"

    def formula(firm, period, _parameters):
        """Total benefits."""
        example_basic_income_i = firm.members("example_basic_income", period)  # Calculates the value of example_basic_income for each member of the firm

        return (
            + firm.sum(example_basic_income_i)  # Sum the firm members basic incomes
            + firm("example_housing_allowance", period)
            )


class example_total_taxes(Variable):
    value_type = float
    entity = Firm
    definition_period = MONTH
    label = "Sum of the taxes paid by a firm"
    reference = "https://stats.gov.example/taxes"

    def formula(firm, period, _parameters):
        """Total taxes."""
        example_income_tax_flat_i = firm.members("example_income_tax_flat", period)
        example_income_tax_progressive_i = firm.members("example_income_tax_progressive", period)

        return (
            + firm.sum(example_income_tax_flat_i)
            + firm.sum(example_income_tax_progressive_i)
            )
