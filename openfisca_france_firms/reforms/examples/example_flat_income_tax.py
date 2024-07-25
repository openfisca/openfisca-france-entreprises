"""
This file defines a reform.

A reform is a set of modifications to be applied to a reference tax and benefit system to carry out experiments.

See https://openfisca.org/doc/key-concepts/reforms.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.reforms import Reform
from openfisca_core.variables import Variable


class example_income_tax_flat(Variable):
    # Variable metadata don't need to be redefined. By default, the reference variable metadatas will be used.

    def formula(establishment, period, _parameters):
        """
        Social security contribution reform.

        Our reform replaces `income_tax_flat` (the "reference" variable) by the following variable.
        """
        return establishment("example_salary", period) * 0.03


class example_income_tax_flat(Reform):
    def apply(self):
        """
        Apply reform.

        A reform always defines an `apply` method that builds the reformed tax and benefit system from the reference one.
        See https://openfisca.org/doc/coding-the-legislation/reforms.html#writing-a-reform
        """
        self.update_variable(example_income_tax_flat)
