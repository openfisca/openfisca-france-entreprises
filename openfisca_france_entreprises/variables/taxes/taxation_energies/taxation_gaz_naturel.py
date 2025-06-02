"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html

Les commentaires avec *** indiquent qu'il y a des problèmes 
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement
from openfisca_france_entreprises.variables.naf import naf

class taxe_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        taxe = etablissement("taxe_interieure_consommation_gaz_naturel", period)
        return taxe 
    
    def formula_2022_01_01(etablissement, period, parameters):
        taxe = etablissement("taxe_accise_gaz_naturel", period)
        return taxe 

class taxe_interieure_consommation_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        
        taxe = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)

        return taxe
    
    def formula_1993_01_01(etablissement, period, parameters):
        #ajouté gaz_matiere_premiere
        
        gaz_matiere_premiere = etablissement("gaz_matiere_premiere", period)

        if gaz_matiere_premiere == True:
            taxe = 0
        else :
            taxe = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)

        return taxe

    
    
    def formula_2003_01_01(etablissement, period, parameters):
        #ajouté gaz_huiles_minerales
        
        gaz_huiles_minerales = etablissement('gaz_huiles_minerales', period)
        gaz_matiere_premiere = etablissement("gaz_matiere_premiere", period)

        if gaz_matiere_premiere == True:
            taxe = 0
        elif gaz_huiles_minerales == True:
            taxe = 0
        else:
            taxe = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)

        return taxe



    def formula_2008_01_01(etablissement, period, parameters):
        """
        ajouté   
            -gaz_production_mineraux_non_metalliques
            -gaz_extraction_production
            -gaz_double_usage

        combiné  
            -gaz_huiles_minerales
            -gaz_matiere_premiere    
        en les transformant en     
            -consommation_gaz_usage_non_combustible 
            > supprimé
        pour conformant plus à la langage de la loi 
        """
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        gaz_extraction_production = etablissement('gaz_extraction_production', period)
        gaz_double_usage = etablissement('gaz_double_usage', period)


        if gaz_production_mineraux_non_metalliques == True : 
            taxe = 0
        elif gaz_double_usage == True:
            taxe = 0
        elif gaz_extraction_production == True:
            taxe = 0

        else: 
            taxe = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)

        return taxe



    def formula_2014_01_01(etablissement, period, parameters):
        '''
        ajouté
        -installation_grande_consommatrice, qui est lié à une modification de taux, voir les paramètres pour plus d'info
        -les conditions qui elle sont liées 
        '''
        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        taxe_interieure_consommation_gaz_naturel_taux_normal = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)
        taxe_interieure_consommation_gaz_naturel_grande_consommatrice = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)
        
        gaz_double_usage = etablissement('gaz_double_usage', period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        gaz_extraction_production = etablissement('gaz_extraction_production', period)

        if gaz_production_mineraux_non_metalliques == True : 
            taxe = 0
        elif gaz_double_usage == True:
            taxe = 0
        elif gaz_extraction_production == True:
            taxe = 0
        elif seqe == True and grande_consommatrice == True:
            taxe = taxe_interieure_consommation_gaz_naturel_grande_consommatrice
        else: 
            taxe = taxe_interieure_consommation_gaz_naturel_taux_normal
        return taxe 
    
    def formula_2019_01_01(etablissement, period, parameters):
        """
        ajouté 
        -Le tarif de la taxe applicable au produit consommé pour déshydrater les légumes et plantes aromatiques, autres que les pommes de terres, les champignons et les truffes, par les entreprises pour lesquelles cette consommation est supérieure à 800 wattheures par euro de valeur ajoutée, est fixé à 1,6 € par mégawattheure.
            calculer, creer une variable value_ajouté, et ensuit appelle la variable ici, si ça depasse le seuil
        
        """
        
        gaz_double_usage = etablissement('gaz_double_usage', period)
        gaz_extraction_production = etablissement('gaz_extraction_production', period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)


        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        taxe_interieure_consommation_gaz_naturel_taux_normal = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)
        taxe_interieure_consommation_gaz_naturel_grande_consommatrice = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement("gaz_dehydration_legumes_et_plantes_aromatiques", period)

        consommation_par_valeur_ajoutee = etablissement("consommation_par_valeur_ajoutee", period)

        if gaz_double_usage == True:
            taxe = 0
        elif gaz_production_mineraux_non_metalliques == True : 
            taxe = 0
        elif gaz_extraction_production == True:
            taxe = 0
        elif gaz_dehydration_legumes_et_plantes_aromatiques == True and consommation_par_valeur_ajoutee >= parameters(period).energies.gaz_naturel.ticgn.seuil_conso_par_va_legumes : #0,0008 MWh par Euro
                taxe = etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period)
                #***cette condition est valide jusqu'à 2022
        elif seqe == True and grande_consommatrice == True:
            taxe = taxe_interieure_consommation_gaz_naturel_grande_consommatrice
        else: 
            taxe = taxe_interieure_consommation_gaz_naturel_taux_normal

        return taxe
    
    def formula_2020_01_01(etablissement, period, parameters):
        """
        ajouté 
        -gaz_travaux_agricoles_et_forestiers
        """
        gaz_double_usage = etablissement('gaz_double_usage', period)
        gaz_travaux_agricoles_et_forestiers = etablissement('gaz_travaux_agricoles_et_forestiers', period)
        gaz_extraction_production = etablissement('gaz_extraction_production', period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)

        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        ticgn_normal = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)
        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)
        

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement("gaz_dehydration_legumes_et_plantes_aromatiques", period)
        consommation_par_valeur_ajoutee = etablissement("consommation_par_valeur_ajoutee", period)


        if gaz_double_usage == True:
            taxe = 0
        elif gaz_extraction_production == True:
            taxe = 0
        elif gaz_production_mineraux_non_metalliques == True : 
            taxe = 0
        elif gaz_travaux_agricoles_et_forestiers == True:
            taxe = 0
        elif gaz_dehydration_legumes_et_plantes_aromatiques == True and consommation_par_valeur_ajoutee >= parameters(period).energies.gaz_naturel.ticgn.seuil_conso_par_va_legumes : #0.0008 MWh par Euro
                taxe = etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period)
                #***cette condition est valide jusqu'à 2022
        elif seqe == True and grande_consommatrice == True:
            taxe = ticgn_grande_conso
        else: 
            taxe = ticgn_normal

        return taxe


class taxe_accise_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Pour combiner les gaz naturels combustible et carburant"
    reference = ""  #
    def formula_2022_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        totale = etablissement("taxe_accise_gaz_naturel_combustible", period) +  etablissement("taxe_accise_gaz_naturel_carburant", period)

        return totale


class taxe_accise_gaz_naturel_combustible(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Pour combiner les gaz naturels combustible et carburant"
    reference = ""  #
    def formula_2022_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        gaz_double_usage = etablissement('gaz_double_usage', period)
        gaz_travaux_agricoles_et_forestiers = etablissement('gaz_travaux_agricoles_et_forestiers', period)
        gaz_extraction_production = etablissement('gaz_extraction_production', period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        consommation_gaz_usage_non_combustible = etablissement('consommation_gaz_usage_non_combustible', period)


        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)
        risque_de_fuite_carbone_eta = etablissement('risque_de_fuite_carbone_eta', period)
        intensite_energetique_valeur_production = etablissement('intensite_energetique_valeur_production', period)
        intensite_energetique_valeur_ajoutee = etablissement('intensite_energetique_valeur_ajoutee', period)


        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement("gaz_dehydration_legumes_et_plantes_aromatiques", period)
        intensite_energetique = etablissement('intensite_energetique', period)

        if gaz_double_usage == True:
            taxe = 0
        elif gaz_travaux_agricoles_et_forestiers == True:
            taxe =  etablissement('consommation_gaz_combustible', period) * parameters(period).energies.gaz_naturel.accise.travaux_agricoles_forestaires
        elif gaz_production_mineraux_non_metalliques == True : 
            taxe = 0
        elif gaz_extraction_production == True:
            taxe = 0
        elif consommation_gaz_usage_non_combustible == True:
            taxe = 0
        elif gaz_dehydration_legumes_et_plantes_aromatiques == True and intensite_energetique >= parameters(period).energies.gaz_naturel.ticgn.seuil_facture_energie_par_va: 
                #le niveau d'intensité énergetique en valeur ajoutée est au moins égale à 0,6744 %.
            taxe = etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period)
                #cette condition est mis en effet dès 2022
        elif (seqe == True and intensite_energetique_valeur_production >= 0.03) or (seqe == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taxe = etablissement('taxe_interieure_taxation_consommation_gaz_naturel_seqe')
            #***faut faire un test pour .
        elif (seqe == False and risque_de_fuite_carbone_eta == True and intensite_energetique_valeur_production >= 0.03) or (seqe == False and risque_de_fuite_carbone_eta == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taxe = etablissement('taxe_interieure_taxation_consommation_gaz_naturel_concurrence_internationale')
            #***faut faire un test pour 
            #ça n'existe plus dès 2024
        elif seqe == True and grande_consommatrice == True:
            taxe = ticgn_grande_conso
        else: 
            taxe = etablissement('consommation_gaz_combustible', period) *  parameters(period).energies.gaz_naturel.accise.taux_normal_combustible
        #*** c'est plus l'assiette mais les consommation individuelle
        return taxe
    
class taxe_accise_gaz_naturel_carburant(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Pour combiner les gaz naturels combustible et carburant"
    reference = ""  #
    def formula_2022_01_01(etablissement, period, parameters):
        gaz_double_usage = etablissement('gaz_double_usage', period)
        gaz_travaux_agricoles_et_forestiers = etablissement('gaz_travaux_agricoles_et_forestiers', period)
        gaz_extraction_production = etablissement('gaz_extraction_production', period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)


        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)


        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)


        if gaz_double_usage == True:
            taxe = 0
        elif gaz_travaux_agricoles_et_forestiers == True:
            taxe =  etablissement('consommation_gaz_combustible', period) * parameters(period).energies.gaz_naturel.accise.travaux_agricoles_forestaires
        elif gaz_production_mineraux_non_metalliques == True : 
            taxe = 0
        elif gaz_extraction_production == True:
            taxe = 0
        elif seqe == True and grande_consommatrice == True:
            taxe = ticgn_grande_conso
        else: 
            taxe = etablissement('consommation_gaz_carburant', period) *  parameters(period).energies.gaz_naturel.accise.taux_normal_carburant

        return taxe

class taxe_interieure_taxation_consommation_gaz_naturel_concurrence_internationale(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75/77"
    reference = ""  #
    def formula_2007_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        assiette_ticgn = etablissement("assiette_ticgn", period)
        taxe = assiette_ticgn * parameters(period).energies.gaz_naturel.taux_reduit_concurrence_internationale

        return taxe


class taxe_interieure_taxation_consommation_gaz_naturel_seqe(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75/76"
    reference = ""  #
    def formula_2007_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        assiette_ticgn = etablissement("assiette_ticgn", period)
        taxe = assiette_ticgn * parameters(period).energies.gaz_naturel.taux_reduit_seqe

        return taxe

class taxe_interieure_consommation_gaz_naturel_legumes(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037988864/2019-01-01/"  
    def formula_2019_01_01(etablissement, period, parameters):
        assiette = etablissement("assiette_ticgn", period)
        taux = parameters(period).energies.gaz_naturel.ticgn.taux_reduit_legumes
        taxe = assiette * taux

        return taxe


class taxe_interieure_consommation_gaz_naturel_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_1986_01_01(etablissement, period, parameters):
        seuil = parameters(period).energies.gaz_naturel.ticgn.seuil_exoneration
        #5000000 
        abattement = parameters(period).energies.gaz_naturel.ticgn.abattement * 12
        #400000
        assiette = etablissement("assiette_ticgn", period)
        taux = parameters(period).energies.gaz_naturel.ticgn.taux_normal
        taxe = (assiette >= seuil) * (assiette - abattement) * taux

        return taxe

    def formula_2008_01_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux = parameters(period).energies.gaz_naturel.ticgn.taux_normal
        taxe = assiette * taux

        return taxe

    def formula_2014_01_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        [à noter : le 1.11 serve à convertir le taux en pci au taux en pcs. On assume que pcs est au courant tout le temps]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux_pci = parameters(period).energies.gaz_naturel.ticgn.taux_normal
        taux = taux_pci * parameters(period).energies.gaz_naturel.ticgn.conversion_pcs_pci
        # facteur de conversion PCI/PCS, cf. Circulaire du 29 avril 2014 "Taxe intérieure de consommation sur le gaz naturel (TICGN) NOR FCPD1408602C"
        # ***faut vérrifier si cette calculation est valide. Paul a dit que l'assumption est que le PCS est tjrs valide
        taxe = assiette * taux
        return taxe


class taxe_interieure_consommation_gaz_naturel_grande_consommatrice(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"  #

    def formula_2014_01_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        """

        assiette = etablissement("assiette_ticgn", period)
        taux = parameters(period).energies.gaz_naturel.ticgn.taux_reduit_grandes_consommatrices
        taxe = assiette * taux

        return taxe

class taxe_interieure_consommation_gaz_naturel_ifp(Variable):
    #pas encore intégrée
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption for the benefit of the French Institute for Petroleum"
    reference = ""  # Always use the most official source
    """je ne trouve que ce résultat bizzare : https://www.legifrance.gouv.fr/search/all?tab_selection=all&searchField=ALL&query=institut+fran%C3%A7ais+du+p%C3%A9trole&searchType=ALL&fonds=CODE&typePagination=DEFAULT&pageSize=10&page=1&tab_selection=all#all"""

    def formula(etablissement, period, parameters):
        """
        Income tax.
        The formula to compute the income tax for a given etablissement at a given period
        """

        return etablissement("consommation_gaz_naturel", period) * parameters(period).taxation_energies.natural_gas



class assiette_ticgn(Variable):
    #dès 1986, seules les usages comme combustible sont soumis à la TICGN. 
    #dès 2020, les usages comme carbrant y sont somis aussi. 
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

        conso = etablissement("consommation_gaz_combustible", period)
        
        conso_exoneree = (etablissement("consommation_gaz_chauffage_habitation", period)
        )
        consommation = max(0, conso - conso_exoneree)
        return consommation
    

    def formula_2000_01_01(etablissement, period, parameters):
        """
        Taxe sur la consommation de gaz naturel.
        TODO:
        Le gaz consommé :
            - comme matière première
            - comme combustible pour la fabrication d'huiles minérales
            - à destination du chauffage des immeubles d'habitation
            est exonéré.
        """

        conso = etablissement("consommation_gaz_combustible", period)

        date_installation_cogeneration = etablissement("date_installation_cogeneration", period)

        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (date_installation_cogeneration < 2007):
            cogeneration_exoneree = True
        
        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period) +
            [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )
        consommation = max(0, conso - conso_exoneree)
        return consommation


    def formula_2006_01_01(etablissement, period, parameters):
        """
        ajouté consommation_gaz_production_electricite
        """
        conso = etablissement("consommation_gaz_combustible", period)

        date_installation_cogeneration = etablissement("date_installation_cogeneration", period)
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (date_installation_cogeneration < 2007):
            cogeneration_exoneree = True

        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period) +
            etablissement("consommation_gaz_production_electricite", period) +
            [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )
        consommation = max(0, conso - conso_exoneree)
        return consommation
    
    def formula_2007_01_01(etablissement, period, parameters):
        """
        ajouté consommation_autres_produits_energetique_ticgn
        """
        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)

        date_installation_cogeneration = etablissement("date_installation_cogeneration", period)
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (date_installation_cogeneration < 2007):
            cogeneration_exoneree = True

        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period) +
            etablissement("consommation_gaz_production_electricite", period) +
            [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )
        consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
        return consommation
    

    def formula_2008_01_01(etablissement, period, parameters):
        """
        [à noter : plus de seuil ni d'abattement]
        TODO:
        Ajout des nouvelles exonérations du gaz consommé :
            - autrement que comme combustible
            - à un double usage
            - dans un procédé de fabrication de produits minéraux non métalliques
            - dans les conditions prévues au III de l'article 265 C du CDD (consommation_gaz_fabrication_soi)
            - pour la production d'électricité
                * sauf pour les installations visées à l'article 266 quinquies A (cogeneration, qui existe depuis longtemps)
            ^par rapport à précedement, doit-on en créer un nouveau ? 
            - pour les besoins de l'extraction et de la production de gaz naturel (gaz_extraction_production)
            - pour la consommation des particuliers (consommation_gaz_particuliers)
        """
        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)


        date_installation_cogeneration = etablissement('date_installation_cogeneration', period)
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (date_installation_cogeneration < 2007):
            cogeneration_exoneree = True

        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period) +
            etablissement("consommation_gaz_fabrication_soi", period) +
            etablissement("consommation_gaz_production_electricite", period) +
            etablissement("consommation_gaz_particuliers", period) +
            etablissement("consommation_gaz_nc_4401_4402", period) +
            etablissement("consommation_gaz_nc_2705", period) +
            [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )

        consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
        return consommation

    def formula_2011_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            la consommation du gaz utilisé pour la production d'électricité par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales.
            n'est plus exonérée à partir du 1er janvier 2011. Cette condition est intégrée comme une exception de consommation_gaz_production_electricite
        """
    
        date_installation_cogeneration = etablissement('date_installation_cogeneration', period)
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (date_installation_cogeneration < 2007):
            cogeneration_exoneree = True

        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)
        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period) +
            etablissement("consommation_gaz_fabrication_soi", period) +
            etablissement("consommation_gaz_production_electricite", period) 
            - etablissement("consommation_gaz_electricite_petits_producteurs", period) +
            etablissement("consommation_gaz_particuliers", period) +
            etablissement("consommation_gaz_nc_4401_4402", period) +
            etablissement("consommation_gaz_nc_2705", period) +
            [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]

        )

        consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
        return consommation
    
    def formula_2014_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
        ajouté 
        -consommation_gaz_nc_2711_29
        suprimmé 
        -consommation_gaz_chauffage_habitation
        -cogéneration car 2011 était la dernière année qu'il était possible de beneficier à une telle éxoneration
        """

        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)

        conso_exoneree = (
            etablissement("consommation_gaz_fabrication_soi", period) +
            etablissement("consommation_gaz_production_electricite", period) 
            - etablissement("consommation_gaz_electricite_petits_producteurs", period) +
            etablissement("consommation_gaz_particuliers", period) +
            etablissement("consommation_gaz_nc_4401_4402", period) +
            etablissement("consommation_gaz_nc_2705", period) + 
            etablissement('consommation_gaz_nc_2711_29', period)
        )

        consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
        return consommation


    def formula_2020_01_01(etablissement, period, parameters):
        """
        TODO:
        (par rapport à précédemment, )
            Réintégration des usages carburants dans le champ de la TICGN >= consommation_gaz_carburant est ajoutée dans la formule de la variable consommation_gaz_naturel 
            https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168
        avant c'était consideré comme un produit petrolier, et en 2020 il sont dit qu'ils sont desormais consideré comme du gaz naturel  
        """

        conso = etablissement("consommation_gaz_combustible", period) + etablissement('consommation_gaz_carburant', period)
        consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)
        conso_exoneree = (
            etablissement("consommation_gaz_fabrication_soi", period) +
            etablissement("consommation_gaz_production_electricite", period) 
            - etablissement("consommation_gaz_electricite_petits_producteurs", period) +
            etablissement("consommation_gaz_particuliers", period) +
            etablissement("consommation_gaz_nc_4401_4402", period) +
            etablissement("consommation_gaz_nc_2705", period) +
            etablissement('consommation_gaz_nc_2711_29', period)
        )
        consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
        return consommation
    
    def formula_2021_01_01(etablissement, period, parameters):
        """suprimmé consommation_gaz_nc_2705
        """
        conso = etablissement("consommation_gaz_combustible", period) + etablissement('consommation_gaz_carburant', period)
        consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)
        conso_exoneree = (
            etablissement("consommation_gaz_fabrication_soi", period) +
            etablissement("consommation_gaz_production_electricite", period) 
            - etablissement("consommation_gaz_electricite_petits_producteurs", period) +
            etablissement("consommation_gaz_particuliers", period) +
            etablissement("consommation_gaz_nc_4401_4402", period) +
            etablissement('consommation_gaz_nc_2711_29', period)
        )

        consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
        return consommation
    

    #pas de ticgn à partir de 2022
    # def formula_2022_01_01(etablissement, period, parameters):
    #     """suprimmé consommation_gaz_nc_4401_4402
    #     """
    #     conso = etablissement("consommation_gaz_combustible", period) + etablissement('consommation_gaz_carburant', period)
    #     consommation_autres_produits_energetique_ticgn = etablissement('consommation_autres_produits_energetique_ticgn', period)
    #     conso_exoneree = (
    #         etablissement("consommation_gaz_fabrication_soi", period) +
    #         etablissement("consommation_gaz_production_electricite", period) 
    #         - etablissement("consommation_gaz_electricite_petits_producteurs", period) +
    #         etablissement("consommation_gaz_particuliers", period) +
    #         etablissement('consommation_gaz_nc_2711_29', period)
    #     )

    #     consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
    #     return consommation
    




