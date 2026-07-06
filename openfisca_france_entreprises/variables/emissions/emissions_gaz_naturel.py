from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import Etablissement


class emissions_gaz_naturel_brute(Variable):
    value_type = float
    unit = "t CO2e"
    entity = Etablissement
    label = "Émissions de CO2 dues à la combustion de gaz naturel, toute consommation confondue"
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        conso = etablissement("consommation_gaz_naturel", period)
        facteur_emission = parameters(period).energies.facteurs_emission.gaz_naturel
        return conso * facteur_emission