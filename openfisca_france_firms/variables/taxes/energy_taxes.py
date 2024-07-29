"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Establishment, a Firm…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import Firm, Establishment

class assiette_ticc(Variable):
    value_type = float
    entity = Establishment
    definition_period = YEAR
    label = "Coal consumption taxable according to TICC"
    reference = ""  #

    def formula_2007_01_01(establishment, period, parameters):

        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_double_usage", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = establishment("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
                conso_combustible_prodelec - conso_combustible_electricite_266qA) +
            conso_combustible_extraction +
            conso_combustible_particuliers
            )

        return assiette

    def formula_2008_01_01(establishment, period, parameters):
        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = establishment("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)

        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - conso_combustible_electricite_266qA) +
            conso_combustible_extraction +
            conso_combustible_particuliers +
            (conso_combustible_biomasse * euets)
            )

        return assiette

    def formula_2009_01_01(establishment, period, parameters):
        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = establishment("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)

        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        facture_energie = establishment("facture_energies")
        chiffre_affaires = establishment.firm("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - conso_combustible_electricite_266qA) +
            conso_combustible_extraction +
            conso_combustible_particuliers +
            (conso_combustible_biomasse * euets * condition_facture)
            )

        return assiette

    def formula_2011_01_01(establishment, period, parameters):
        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = establishment("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)

        conso_combustible_electricite_petits_producteurs = establishment("consommation_charbon_combustible_electricite_petits_producteurs", period)

        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        facture_energie = establishment("facture_energies")
        chiffre_affaires = establishment.firm("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - conso_combustible_electricite_266qA - conso_combustible_electricite_petits_producteurs) +
            conso_combustible_extraction +
            conso_combustible_particuliers +
            (conso_combustible_biomasse * euets * condition_facture)
            )

        return assiette

    def formula_2011_01_01(establishment, period, parameters):
        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = establishment("consommation_charbon_combustible_particuliers", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)
        contrat_achat_electricite_314 = establishment("contrat_achat_electricite_314", period)

        conso_combustible_electricite_petits_producteurs = establishment("consommation_charbon_combustible_electricite_petits_producteurs", period)

        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        facture_energie = establishment("facture_energies")
        chiffre_affaires = establishment.firm("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - (conso_combustible_electricite_266qA * contrat_achat_electricite_314) - conso_combustible_electricite_petits_producteurs) +
            conso_combustible_extraction +
            conso_combustible_particuliers +
            (conso_combustible_biomasse * euets * condition_facture)
            )

        return assiette

    def formula_2014_04_01(establishment, period, parameters):
        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)
        contrat_achat_electricite_314 = establishment("contrat_achat_electricite_314", period)

        conso_combustible_electricite_petits_producteurs = establishment("consommation_charbon_combustible_electricite_petits_producteurs", period)

        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        facture_energie = establishment("facture_energies")
        chiffre_affaires = establishment.firm("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - (conso_combustible_electricite_266qA * contrat_achat_electricite_314) - conso_combustible_electricite_petits_producteurs) +
            conso_combustible_extraction +
            (conso_combustible_biomasse * euets * condition_facture)
            )

        return assiette

    def formula_2014_04_01(establishment, period, parameters):
        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)

        conso_combustible_electricite_266qA = establishment("consommation_charbon_combustible_electricite_266qA", period)
        contrat_achat_electricite_314 = establishment("contrat_achat_electricite_314", period)

        conso_combustible_electricite_petits_producteurs = establishment("consommation_charbon_combustible_electricite_petits_producteurs", period)
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        facture_energie = establishment("facture_energies")
        chiffre_affaires = establishment.firm("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (
            conso_non_combustible +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - (conso_combustible_electricite_266qA * contrat_achat_electricite_314) - conso_combustible_electricite_petits_producteurs) +
            conso_combustible_extraction +
            (conso_combustible_biomasse * euets * condition_facture)
            )

        return assiette

    def formula_2020_01_01(establishment, period, parameters):

        consommation_charbon = establishment("consommation_charbon", period)

        conso_non_combustible = establishment("consommation_charbon_non_combustible", period)
        conso_carburant = establishment("consommation_charbon_carburant", period)
        conso_double_usage = establishment("consommation_charbon_double_usage", period)
        conso_di26 = establishment("consommation_charbon_di26", period)

        installation_cogeneration = establishment("installation_cogeneration", period)

        conso_combustible_interne = establishment("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = establishment("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = establishment("consommation_charbon_combustible_extraction", period)

        conso_combustible_electricite_petits_producteurs = establishment("consommation_charbon_combustible_electricite_petits_producteurs", period)
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017
        
        conso_combustible_biomasse = establishment("consommation_charbon_combustible_biomasse", period)

        euets = establishment("is_euets", period)

        facture_energie = establishment("facture_energies")
        chiffre_affaires = establishment.firm("chiffre_affaires", period)
        condition_facture = facture_energie >= .03 * chiffre_affaires

        assiette = consommation_charbon - (
            (conso_non_combustible - (conso_carburant * installation_cogeneration)  +
            conso_double_usage +
            conso_di26
            ) - (
            conso_combustible_interne + (
            conso_combustible_prodelec - conso_combustible_electricite_petits_producteurs) +
            conso_combustible_extraction +
            (conso_combustible_biomasse * euets * condition_facture)
            )

        return assiette

class taxe_interieure_consommation_charbon(Variable):
    value_type = float
    entity = Establishment
    definition_period = YEAR
    label = "Tax e intérieure de consommation sur les houilles, lignites et cokes - TICC"
    reference = ""  #

    def formula_2007_01_01(establishment, period, parameters):
        """
        Taxe sur la consommation de houilles, lignites, et cokes.
        """

        assiette_ticc = establishment("assiette_ticc", period)
        ticc = assiette_ticc * parameters(period).energy

        return ticc

class tax_consumption_natural_gas(Variable):
    value_type = float
    entity = Establishment
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_1986_01_01(establishment, period, parameters):
        """
        Taxe sur la consommation de gaz naturel.
        TODO:
        Le gaz consommé :
            - comme matière première
            - comme combustible pour la fabrication d'huiles minérales
            - à destination du chauffage des immeubles d'habitation
            est exonéré.
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energies.ticgn.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2007_01_01(establishment, period, parameters):
        """
        (en plus de précédemment,)
        TODO:
        Le gaz utilisé pour la production d'électricité est exonéré.
        -> séparer les types de consommations dans ../energy_consumption/
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2008_04_01(establishment, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        TODO:
        Le gaz consommé :
            - autrement que comme combustible
            - à un double usage
            - dans un procédé de fabrication de produits minéraux non métalliques
            - dans les conditions prévues au III de l'article 265 C du CDD
            - pour la production d'électricité
                * sauf pour les installations visées à l'article 266 quinquies A
                    ++ sauf quand celles-ci ne bénéficient pas d'un tarif d'achat d'électricité dans le cadre l'article 10 de la loi n° 2000-108 du 10 février 2000
            - pour les besoins de l'extraction et de la production de gaz naturel
            - pour la consommation des particuliers
            - pour la consommation des autorités régionales et locales ou des autres organismes de droit public pour les activités ou opérations qu'ils accomplissent en tant qu'autorités publiques jusqu'au 1er janvier 2009
        """

        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = conso * rate

        return  tax

    def formula_2009_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation des autorités régionales et locales ou des autres organismes de droit public pour les activités ou opérations qu'ils accomplissent en tant qu'autorités publiques
            n'est plus exonérée à partir du 1er janvier 2009.
        """

        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = conso * rate

        return  tax

    def formula_2011_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation du gaz utilisé pour la production d'électricité par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales.
            n'est plus exonérée à partir du 1er janvier 2011.
        """

        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = conso * rate

        return  tax

    def formula_2019_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Le tarif de la taxe applicable au produit consommé pour déshydrater les légumes et plantes aromatiques, autres que les pommes de terres, les champignons et les truffes, par les entreprises pour lesquelles cette consommation est supérieure à 800 wattheures par euro de valeur ajoutée, est fixé à 1,6 € par mégawattheure.
        """

        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = conso * rate

        return  tax

    def formula_2020_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Réintégration des usages carburants dans le champ de la TICGN ?
            https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168
        """

        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = conso * rate

        return  tax

class tax_consumption_natural_gas_ifp(Variable):
    value_type = float
    entity = Establishment
    definition_period = YEAR
    label = "Tax on gas consumption for the benefit of the French Institute for Petroleum"
    reference = ""  # Always use the most official source

    def formula(establishment, period, parameters):
        """
        Income tax.

        The formula to compute the income tax for a given establishment at a given period
        """
        return establishment("gas_consumption", period) * parameters(period).energy.natural_gas
