from openfisca_core.model_api import *
from openfisca_france_firms.entities import Establishment, Firm  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class consommation_energie(Variable):
    value_type = float
    unit = 'MWh'
    entity = Establishment
    label = "Consommation d'énergie totale de l'établissement"
    definition_period = YEAR

    def formula(establishment, period):
        gaz = establishment("consommation_gaz_naturel", period)
        charbon = establishment("consommation_charbon", period)
        electricite = establishment("consommation_electricite", period)
        autres_produits = establishment("consommation_autres_produits", period)

        return (gaz +
                charbon +
                electricite +
                autres_produits)

class intensite_energetique(Variable):
    value_type = float
    unit = 'kWh/€'
    entity = Establishment
    label = "Intensité enrgétique de l'établissement"
    definition_period = YEAR

class intensite_energetique_firm(Variable):
    value_type = float
    unit = 'kWh/€'
    entity = Firm
    label = "Intensité enrgétique de l'établissement"
    definition_period = YEAR

