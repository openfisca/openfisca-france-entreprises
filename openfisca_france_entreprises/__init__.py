"""This file defines our country's tax and benefit system.

A tax and benefit system is the higher-level instance in OpenFisca.
Its goal is to model the legislation of a country.
Basically a tax and benefit system contains simulation variables (source code) and legislation parameters (data).

See https://openfisca.org/doc/key-concepts/tax_and_benefit_system.html
"""

from pathlib import Path

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france_entreprises import entities
from openfisca_france_entreprises.situation_examples import couple

COUNTRY_DIR = Path(__file__).resolve().parent


# Our country tax and benefit class inherits from the general TaxBenefitSystem class.
# The name CountryTaxBenefitSystem must not be changed, as all tools of the
# OpenFisca ecosystem expect a CountryTaxBenefitSystem class to be exposed in
# the __init__ module of a country package.
class CountryTaxBenefitSystem(TaxBenefitSystem):
    """France entreprises tax and benefit system."""

    def __init__(self):
        """Initialize the France entreprises tax and benefit system.

        Sets up entities, loads variables from the variables directory,
        loads parameters from the parameters directory, and configures OpenAPI examples.
        """
        # We initialize our tax and benefit system with the general constructor
        super().__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(COUNTRY_DIR / "variables")

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        param_path = COUNTRY_DIR / "parameters"
        self.load_parameters(param_path)

        # We define which variable, parameter and simulation example will be used in the OpenAPI specification
        self.open_api_config = {
            "variable_example": "apet",
            "parameter_example": "energies.autres_produits_energetiques.major_regionale_ticpe_gazole.ile_france",
            "simulation_example": couple,
        }
