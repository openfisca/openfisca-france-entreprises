"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale


class example_total_benefits(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "Sum of the benefits perceived by a unite_legale"
    reference = "https://stats.gov.example/benefits"

    def formula(unite_legale, period, _parameters):
        """Total benefits."""
        example_basic_income_i = unite_legale.members("example_basic_income", period)  # Calculates the value of example_basic_income for each member of the unite_legale

        return (
            + unite_legale.sum(example_basic_income_i)  # Sum the unite_legale members basic incomes
            + unite_legale("example_housing_allowance", period)
            )


class example_total_taxes(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "Sum of the taxes paid by a unite_legale"
    reference = "https://stats.gov.example/taxes"

    def formula(unite_legale, period, _parameters):
        """Total taxes."""
        example_income_tax_flat_i = unite_legale.members("example_income_tax_flat", period)
        example_income_tax_progressive_i = unite_legale.members("example_income_tax_progressive", period)

        return (
            + unite_legale.sum(example_income_tax_flat_i)
            + unite_legale.sum(example_income_tax_progressive_i)
            )
