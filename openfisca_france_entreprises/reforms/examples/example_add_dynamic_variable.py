"""
This file defines a reform to add a dynamic variable, based on input data.

A reform is a set of modifications to be applied to a reference tax and benefit system to carry out experiments.

See https://openfisca.org/doc/key-concepts/reforms.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.reforms import Reform
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import Etablissement


def create_dynamic_variable(name, **variable):
    """Create new variable dynamically."""
    NewVariable = type(name, (Variable,), {
        "value_type": variable["value_type"],
        "entity": variable["entity"],
        "default_value": variable["default_value"],
        "definition_period": variable["definition_period"],
        "label": variable["label"],
        "reference": variable["reference"],
        })

    return NewVariable


class add_dynamic_variable(Reform):
    def apply(self):
        """
        Apply reform.

        A reform always defines an `apply` method that builds the reformed tax
        and benefit system from the reference one.

        See https://openfisca.org/doc/coding-the-legislation/reforms.html#writing-a-reform
        """
        NewVariable = create_dynamic_variable(
            name = "is_euets",
            value_type = bool,
            entity = Etablissement,
            default_value = True,
            definition_period = MONTH,
            label = "The etablissement is subject to EUETS",
            reference = "https://law.gov.example/is_euets",
            )

        self.add_variable(NewVariable)
