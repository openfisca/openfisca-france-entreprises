"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class taxe_interieure_consommation_charbon(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax e intérieure de consommation sur les houilles, lignites et cokes - TICC"
    reference = ""  #

    def formula_2007_01_01(etablissement, period, parameters):
        """
        Taxe sur la consommation de houilles, lignites, et cokes.
        """

        assiette_ticc = etablissement("assiette_ticc", period)
        ticc = assiette_ticc * parameters(period).energy

        return ticc


class assiette_ticc(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Coal consumption taxable according to TICC"
    reference = ""  #

    def formula_2007_01_01(etablissement, period, parameters):

        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_double_usage", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - conso_combustible_electricite_266qA) + conso_combustible_extraction + conso_combustible_particuliers)

        return assiette

    def formula_2008_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - conso_combustible_electricite_266qA) + conso_combustible_extraction + conso_combustible_particuliers + (conso_combustible_biomasse * euets))

        return assiette

    def formula_2009_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        facture_energie = etablissement("facture_energies")
        chiffre_affaires = etablissement.unite_legale("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - conso_combustible_electricite_266qA) + conso_combustible_extraction + conso_combustible_particuliers + (conso_combustible_biomasse * euets * condition_facture))

        return assiette

    def formula_2011_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)

        conso_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        facture_energie = etablissement("facture_energies")
        chiffre_affaires = etablissement.unite_legale("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - conso_combustible_electricite_266qA - conso_combustible_electricite_petits_producteurs) + conso_combustible_extraction + conso_combustible_particuliers + (conso_combustible_biomasse * euets * condition_facture))

        return assiette

    def formula_2014_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)
        contrat_achat_electricite_314 = etablissement("contrat_achat_electricite_314", period)

        conso_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        facture_energie = etablissement("facture_energies")
        chiffre_affaires = etablissement.unite_legale("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - (conso_combustible_electricite_266qA * contrat_achat_electricite_314) - conso_combustible_electricite_petits_producteurs) + conso_combustible_extraction + conso_combustible_particuliers + (conso_combustible_biomasse * euets * condition_facture))

        return assiette

    def formula_2016_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)
        contrat_achat_electricite_314 = etablissement("contrat_achat_electricite_314", period)

        conso_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        facture_energie = etablissement("facture_energies")
        chiffre_affaires = etablissement.unite_legale("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - (conso_combustible_electricite_266qA * contrat_achat_electricite_314) - conso_combustible_electricite_petits_producteurs) + conso_combustible_extraction + (conso_combustible_biomasse * euets * condition_facture))

        return assiette

    def formula_2018_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)

        conso_combustible_electricite_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)
        contrat_achat_electricite_314 = etablissement("contrat_achat_electricite_314", period)

        conso_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        facture_energie = etablissement("facture_energies")
        chiffre_affaires = etablissement.unite_legale("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (conso_non_combustible + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - (conso_combustible_electricite_266qA * contrat_achat_electricite_314) - conso_combustible_electricite_petits_producteurs) + conso_combustible_extraction + (conso_combustible_biomasse * euets * condition_facture))

        return assiette

    def formula_2020_01_01(etablissement, period, parameters):

        consommation_charbon = etablissement("consommation_charbon", period)

        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_carburant = etablissement("consommation_charbon_carburant", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)

        installation_cogeneration = etablissement("installation_cogeneration", period)

        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)

        conso_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)

        euets = etablissement("is_euets", period)

        facture_energie = etablissement("facture_energies")
        chiffre_affaires = etablissement.unite_legale("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (conso_non_combustible - (conso_carburant * installation_cogeneration) + conso_double_usage + conso_di26) - (conso_combustible_interne + (conso_combustible_prodelec - conso_combustible_electricite_petits_producteurs) + conso_combustible_extraction + (conso_combustible_biomasse * euets * condition_facture))

        return assiette
