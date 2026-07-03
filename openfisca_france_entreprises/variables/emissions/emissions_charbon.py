from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import Etablissement


class emissions_charbon_brute(Variable):
    # Version brute : toute la consommation de charbon telle que déclarée dans "consommation_charbon" est prise en compte. Il faudra redétailler 
    value_type = float
    unit = "t CO2e"
    entity = Etablissement
    label = "Émissions de CO2 dues à la combustion de charbon, toute consommation confondue"
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        conso = etablissement("consommation_charbon", period)
        facteur_emission = parameters(period).energies.facteurs_emission.charbon
        return conso * facteur_emission