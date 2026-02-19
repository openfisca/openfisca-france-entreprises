"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import Etablissement


class example_income_tax_flat(Variable):
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    label = "Income tax"
    reference = "https://law.gov.example/example_income_tax_flat"  # Always use the most official source

    def formula(etablissement, period, parameters):
        """
        Income tax.

        The formula to compute the income tax for a given etablissement at a given period
        """
        return (
            etablissement("example_salary", period)
            * parameters(period).example_taxes.example_income_tax_rate_flat
        )


class example_income_tax_progressive(Variable):
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    label = "Income tax"
    reference = "https://law.gov.example/example_income_tax_progressive"  # Always use the most official source

    def formula(etablissement, period, parameters):
        """
        Income tax.

        The formula to compute the income tax for a given etablissement at a given period
        """
        scale = parameters(period).example_taxes.example_income_tax_rate_progressive
        basis = etablissement("example_salary", period)

        return scale.calc(basis)
