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


class total_benefits(Variable):
    value_type = float
    entity = Firm
    definition_period = MONTH
    label = "Sum of the benefits perceived by a firm"
    reference = "https://stats.gov.example/benefits"

    def formula(firm, period, _parameters):
        """Total benefits."""
        basic_income_i = firm.members("basic_income", period)  # Calculates the value of basic_income for each member of the firm

        return (
            + firm.sum(basic_income_i)  # Sum the firm members basic incomes
            + firm("housing_allowance", period)
            )


class total_taxes(Variable):
    value_type = float
    entity = Firm
    definition_period = MONTH
    label = "Sum of the taxes paid by a firm"
    reference = "https://stats.gov.example/taxes"

    def formula(firm, period, _parameters):
        """Total taxes."""
        income_tax_i = firm.members("income_tax", period)
        social_security_contribution_i = firm.members("social_security_contribution", period)

        return (
            + firm.sum(income_tax_i)
            + firm.sum(social_security_contribution_i)
            + firm("housing_tax", period.this_year) / 12
            )
