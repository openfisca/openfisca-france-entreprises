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

class tax_consumption_natural_gas(Variable):
    value_type = float
    entity = Establishment
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://law.gov.example/example_income_tax_flat"  #

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
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2007_01_01(establishment, period, parameters):
        """
        (en plus de précédemment,)
        TODO:
        Le gaz utilisé pour la production d'électricité est exonéré.
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2008_04_01(establishment, period, parameters):
        """
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

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2009_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation des autorités régionales et locales ou des autres organismes de droit public pour les activités ou opérations qu'ils accomplissent en tant qu'autorités publiques
            n'est plus exonérée à partir du 1er janvier 2009.
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2011_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation du gaz utilisé pour la production d'électricité par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales.
            n'est plus exonérée à partir du 1er janvier 2011.
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2019_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Le tarif de la taxe applicable au produit consommé pour déshydrater les légumes et plantes aromatiques, autres que les pommes de terres, les champignons et les truffes, par les entreprises pour lesquelles cette consommation est supérieure à 800 wattheures par euro de valeur ajoutée, est fixé à 1,6 € par mégawattheure.
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

        return  tax

    def formula_2020_01_01(establishment, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Réintégration des usages carburants dans le champ de la TICGN ?
            https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168
        """

        seuil = parameters(period).energy.ticgn_seuil_exoneration
        abattement = parameters(period).energy.ticgn_abattement * 12
        conso = establishment("consumption_natural_gas", period)
        rate = parameters(period).energy.natural_gas
        tax = (conso > seuil) * (conso - abattement) * rate

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
