from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement, UniteLegale  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable


class consommation_energie(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation d'énergie totale de l'établissement"
    definition_period = YEAR

    def formula(etablissement, period):
        gaz = etablissement("consommation_gaz_naturel", period)
        charbon = etablissement("consommation_charbon", period)
        electricite = etablissement("consommation_electricite", period)
        autres_produits = etablissement("consommation_autres_produits", period)

        return (gaz + charbon + electricite + autres_produits)


class intensite_energetique_unite_legale(Variable):
    value_type = float
    unit = 'kWh/€'
    entity = UniteLegale
    label = "Intensité énergétique de l'entreprise"
    definition_period = YEAR

    def formula(unite_legale, period):
        conso_i = unite_legale.members("consommation_energie", period)
        conso = unite_legale.sum(conso_i)

        va = unite_legale("valeur_ajoutee", period)

        return conso / va


class intensite_energetique_etablissement(Variable):
    value_type = float
    unit = 'kWh/€'
    entity = Etablissement
    label = "Intensité énergétique de l'établissement"
    definition_period = YEAR

    def formula(etablissement, period):
        intensite = etablissement.unite_legale("intensite_energetique_unite_legale", period)

        return intensite


class etablissement_electrointensif(Variable):
    value_type = bool
    entity = Etablissement
    label = "Etablissement électrointensif"
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        intensite = etablissement("intensite_energetique_etablishment", period)
        seuil = parameters(period).energies.eu.seuil_electrointensivite

        return intensite >= seuil


class entreprise_electro_intensive(Variable):
    value_type = bool
    entity = UniteLegale
    label = "Entreprise électrointensive"
    definition_period = YEAR

    def formula(unite_legale, period, parameters):
        intensite = unite_legale("intensite_energetique_unite_legale", period)
        seuil = parameters(period).energies.eu.seuil_electrointensivite

        return intensite >= seuil
