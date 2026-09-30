"""Variables and formulas for this module."""

from openfisca_core.model_api import ADD, YEAR, Variable

from openfisca_france_entreprises.entities import (
    Etablissement,
    UniteLegale,
)


class consommation_energie(Variable):
    value_type = float
    unit = "MWh"
    entity = Etablissement
    label = "Consommation d'énergie totale de l'établissement"
    definition_period = YEAR

    def formula(etablissement, period):
        # Les consommations sont mensuelles depuis la bascule ; le total annuel en est la
        # somme sur les douze mois.
        gaz = etablissement("consommation_gaz_naturel", period, options=[ADD])
        charbon = etablissement("consommation_charbon", period, options=[ADD])
        electricite = etablissement("consommation_electricite", period, options=[ADD])
        autres_produits = etablissement("consommation_autres_produits", period)

        return gaz + charbon + electricite + autres_produits


class intensite_energetique_unite_legale(Variable):
    value_type = float
    unit = "kWh/€"
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
    unit = "kWh/€"
    entity = Etablissement
    label = "Intensité énergétique de l'établissement"
    definition_period = YEAR

    def formula(etablissement, period):
        return etablissement.unite_legale(
            "intensite_energetique_unite_legale",
            period,
        )


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
