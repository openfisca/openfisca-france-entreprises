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


class taxe_interieure_consommation_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        ticgn = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)

        return ticgn

    def formula_2014_04_01(etablissement, period, parameters):
        euets = etablissement("installation_euets", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice", period)

        ticgn_normal = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)
        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        return (euets * grande_consommatrice * ticgn_grande_conso) + ((1 - euets * grande_consommatrice) * ticgn_normal)

    def formula_2015_01_01(etablissement, period, parameters):
        euets = etablissement("installation_euets", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice", period)

        electrointensive = etablissement("installation_electrointensive", period)
        risque_fuite = etablissement.unite_legale("entreprises_risque_de_fuite_carbone", period)

        ticgn_normal = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)
        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)
        ticgn_electrointensive = etablissement("taxe_interieure_consommation_gaz_naturel_electrointensive", period)

        ticgn = (euets * grande_consommatrice * ticgn_grande_conso) + ((1 - euets) * electrointensive * risque_fuite * ticgn_electrointensive) + ((1 - ((euets * grande_consommatrice) + ((1 - euets) * electrointensive * risque_fuite))) * ticgn_normal)

        return ticgn


class taxe_interieure_consommation_gaz_naturel_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_1986_01_01(etablissement, period, parameters):
        seuil = 5000000
        # parameters(period).taxation_energies.ticgn_seuil_exoneration
        abattement = 400000
        # parameters(period).taxation_energies.ticgn.ticgn_abattement * 12
        assiette = etablissement("assiette_ticgn", period)
        taux = parameters(period).taxation_energies.natural_gas
        taxe = (assiette > seuil) * (assiette - abattement) * taux

        return taxe

    def formula_2008_04_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux = parameters(period).taxation_energies.natural_gas
        taxe = assiette * taux

        return taxe

    def formula_2014_04_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux_pci = parameters(period).taxation_energies.natural_gas
        taux = taux_pci / 1.11
        # facteur de conversion PCI/PCS, cf. Circulaire du 29 avril 2014 "Taxe intérieure de consommation sur le gaz naturel (TICGN) NOR FCPD1408602C"
        taxe = assiette * taux

        return taxe


class taxe_interieure_consommation_gaz_naturel_grande_consommatrice(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_2014_04_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux = parameters("2013-12-31").taxation_energies.natural_gas
        taxe = assiette * taux

        return taxe

    def formula_2016_04_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux = parameters("2013-12-31").taxation_energies.natural_gas
        majoration = .33
        # majoration = parameters(period).taxation_energies.taux_reduit_grande_consommatrice
        taxe = assiette * (taux + majoration)

        return taxe


class taxe_interieure_consommation_gaz_naturel_electrointensive(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_2015_01_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux_pci = parameters("2014-12-31").taxation_energies.natural_gas
        taux = taux_pci / 1.11
        # facteur de conversion PCI/PCS, cf. Circulaire du 29 avril 2014 "Taxe intérieure de consommation sur le gaz naturel (TICGN) NOR FCPD1408602C"
        taxe = assiette * taux

        return taxe

    def formula_2016_01_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux_pci = parameters("2014-12-31").taxation_energies.natural_gas
        taux = taux_pci / 1.11
        # facteur de conversion PCI/PCS, cf. Circulaire du 29 avril 2014 "Taxe intérieure de consommation sur le gaz naturel (TICGN) NOR FCPD1408602C"
        majoration = .33
        # majoration = parameters(period).taxation_energies.taux_reduit_grande_consommatrice
        taxe = assiette * (taux + majoration)

        return taxe


class assiette_ticgn(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_1986_01_01(etablissement, period, parameters):
        """
        Taxe sur la consommation de gaz naturel.
        TODO:
        Le gaz consommé :
            - comme matière première
            - comme combustible pour la fabrication d'huiles minérales
            - à destination du chauffage des immeubles d'habitation
            est exonéré.
        """

        conso = etablissement("consommation_gaz_naturel", period)

        return conso

    def formula_2007_01_01(etablissement, period, parameters):
        """
        (en plus de précédemment,)
        TODO:
        Le gaz utilisé pour la production d'électricité est exonéré.
        -> séparer les types de consommations dans ../energy_consumption/
        """

        conso = etablissement("consommation_gaz_naturel", period)

        return conso

    def formula_2008_04_01(etablissement, period, parameters):
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

        conso = etablissement("consommation_gaz_naturel", period)

        return conso

    def formula_2009_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation des autorités régionales et locales ou des autres organismes de droit public pour les activités ou opérations qu'ils accomplissent en tant qu'autorités publiques
            n'est plus exonérée à partir du 1er janvier 2009.
        """

        conso = etablissement("consommation_gaz_naturel", period)

        return conso

    def formula_2011_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation du gaz utilisé pour la production d'électricité par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales.
            n'est plus exonérée à partir du 1er janvier 2011.
        """

        conso = etablissement("consommation_gaz_naturel", period)

        return conso

    def formula_2019_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Le tarif de la taxe applicable au produit consommé pour déshydrater les légumes et plantes aromatiques, autres que les pommes de terres, les champignons et les truffes, par les entreprises pour lesquelles cette consommation est supérieure à 800 wattheures par euro de valeur ajoutée, est fixé à 1,6 € par mégawattheure.
        """

        conso = etablissement("consommation_gaz_naturel", period)

        return conso

    def formula_2020_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Réintégration des usages carburants dans le champ de la TICGN ?
            https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168
        """

        conso = etablissement("consommation_gaz_naturel", period)

        return conso


class taxe_interieure_consommation_gaz_naturel_ifp(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption for the benefit of the French Institute for Petroleum"
    reference = ""  # Always use the most official source

    def formula(etablissement, period, parameters):
        """
        Income tax.

        The formula to compute the income tax for a given etablissement at a given period
        """

        return etablissement("consommation_gaz_naturel", period) * parameters(period).taxation_energies.natural_gas
