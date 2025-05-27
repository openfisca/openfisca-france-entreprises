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
    label = "Taxe intérieure de consommation sur les houilles, lignites et cokes - TICC"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"  #

    def formula_2007_01_01(etablissement, period, parameters):
        """
        Taxe sur la consommation de houilles, lignites, et cokes.
        """

        assiette_ticc = etablissement("assiette_ticc", period)
        ticc = assiette_ticc * parameters(period).energies.charbon.ticc

        return ticc

    def formula_2008_01_01(etablissement, period, parameters):
        #(2008) Par rapport à precedement: ajout conso_combustible_biomasse, seqe
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        #les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)
        seqe = etablissement("installation_seqe", period)

        if seqe == True and charbon_biomasse == True:
            taxe = 0
        else: 
            taxe = etablissement("taxe_interieure_taxation_consommation_charbon_taux_normal", period)
        

        return taxe
    
    
    def formula_2009_01_01(etablissement, period, parameters):
        #(2009) par rapport à précedement, ajout condition_facture 
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        #les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)

        installation_grande_consommatrice_energie = etablissement('installation_grande_consommatrice_energie', period) #grandes consommatrices d’énergie soumises à quota CO₂
        
        if installation_grande_consommatrice_energie and charbon_biomasse == True:
            taxe = 0
        else: 
            taxe = etablissement("taxe_interieure_taxation_consommation_charbon_taux_normal", period)
        
        return taxe    
    
        
    def formula_2022_01_01(etablissement, period, parameters):
        #par rapport à précedement, ajouté charbon_secteurs_aeronautique_et_naval, charbon_navigation_interieure, charbon_navigation_aerienne, charbon_fabrication_produits_mineraux_non_metalliques comme conditions d'exemption de la taxe

        #les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)
        installation_seqe = etablissement("installation_seqe", period)
        risque_de_fuite_carbone_eta = etablissement('risque_de_fuite_carbone_eta', period)
        intensite_energetique_valeur_production = etablissement('intensite_energetique_valeur_production', period)
        intensite_energetique_valeur_ajoutee = etablissement('intensite_energetique_valeur_ajoutee', period)

        #les suivant permettent une excemption de la taxe 
        charbon_navigation_interieure = etablissement("charbon_navigation_interieure", period)
        charbon_navigation_maritime = etablissement("charbon_navigation_maritime", period)
        charbon_navigation_aerienne = etablissement("charbon_navigation_aerienne", period)
        charbon_fabrication_produits_mineraux_non_metalliques = etablissement('charbon_fabrication_produits_mineraux_non_metalliques',period)
        charbon_secteurs_aeronautique_et_naval = etablissement("charbon_secteurs_aeronautique_et_naval", period)
        charbon_double_usage = etablissement('charbon_double_usage', period)


        if installation_seqe == True and intensite_energetique_valeur_production >= 0.03 and charbon_biomasse == True:
            taxe = 0
        elif charbon_navigation_interieure == True:
            taxe = 0
        elif charbon_navigation_maritime == True: 
            taxe = 0
        elif charbon_navigation_aerienne == True:
            taxe = 0
        elif charbon_fabrication_produits_mineraux_non_metalliques == True:
            taxe = 0
        elif charbon_secteurs_aeronautique_et_naval == True:
            taxe = 0
        elif charbon_double_usage == True:
            taxe = 0
        elif (installation_seqe == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taxe = etablissement('taxe_interieure_taxation_consommation_charbon_seqe')
            #***faut faire un test pour 
        elif (installation_seqe == False and risque_de_fuite_carbone_eta == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == False and risque_de_fuite_carbone_eta == True and  intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taxe = etablissement('taxe_interieure_taxation_consommation_charbon_concurrence_internationale')
            #***faut faire un test pour 
            #ça n'existe plus dès 2024
        else: 
            taxe = etablissement("taxe_interieure_taxation_consommation_charbon_taux_normal", period)
        

        return taxe
    def formula_2024_01_01(etablissement, period, parameters):

        #les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)
        installation_seqe = etablissement("installation_seqe", period)

        intensite_energetique_valeur_production = etablissement('intensite_energetique_valeur_production', period)
        intensite_energetique_valeur_ajoutee = etablissement('intensite_energetique_valeur_ajoutee', period)

        #les suivant permettent une excemption de la taxe 
        charbon_navigation_interieure = etablissement("charbon_navigation_interieure", period)
        charbon_navigation_maritime = etablissement("charbon_navigation_maritime", period)
        charbon_navigation_aerienne = etablissement("charbon_navigation_aerienne", period)
        charbon_fabrication_produits_mineraux_non_metalliques = etablissement('charbon_fabrication_produits_mineraux_non_metalliques',period)
        charbon_secteurs_aeronautique_et_naval = etablissement("charbon_secteurs_aeronautique_et_naval", period)
        charbon_double_usage = etablissement('charbon_double_usage', period)


        if installation_seqe == True and intensite_energetique_valeur_production >= 0.03 and charbon_biomasse == True:
            taxe = 0
        elif charbon_navigation_interieure == True:
            taxe = 0
        elif charbon_navigation_maritime == True: 
            taxe = 0
        elif charbon_navigation_aerienne == True:
            taxe = 0
        elif charbon_fabrication_produits_mineraux_non_metalliques == True:
            taxe = 0
        elif charbon_secteurs_aeronautique_et_naval == True:
            taxe = 0
        elif charbon_double_usage == True:
            taxe = 0
        elif (installation_seqe == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taxe = etablissement('taxe_interieure_taxation_consommation_charbon_seqe')
            #***faut faire un test pour 
        else: 
            taxe = etablissement("taxe_interieure_taxation_consommation_charbon_taux_normal", period)
        

        return taxe
    
    

class taxe_interieure_taxation_consommation_charbon_concurrence_internationale(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75"
    reference = ""  #
    def formula_2007_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        assiette_ticc = etablissement("assiette_ticc", period)
        taxe = assiette_ticc * parameters(period).energies.charbon.taux_reduit_concurrence_internationale

        return taxe

class taxe_interieure_taxation_consommation_charbon_seqe(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75"
    reference = ""  #
    def formula_2007_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        assiette_ticc = etablissement("assiette_ticc", period)
        taxe = assiette_ticc * parameters(period).energies.charbon.taux_reduit_seqe

        return taxe

class taxe_interieure_taxation_consommation_charbon_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-65"
    reference = ""  #
    def formula_2007_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        assiette_ticc = etablissement("assiette_ticc", period)
        taxe = assiette_ticc * parameters(period).energies.charbon.ticc

        return taxe


class assiette_ticc(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Coal consumption taxable according to TICC"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"  #

    def formula_2007_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement('consommation_autres_produits_energetique_ticc', period)

        #ces cinq sont à exclure de l'assiette
        consommation_charbon_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        consommation_charbon_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        consommation_charbon_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)
        consommation_charbon_combustible_electricite = etablissement("consommation_charbon_combustible_electricite", period)

        assiette = consommation_charbon + consommation_autres_produits_energetique_ticc - ( consommation_charbon_combustible_interne + consommation_charbon_combustible_electricite + consommation_charbon_combustible_extraction + consommation_charbon_combustible_particuliers )

        return assiette

    def formula_2011_01_01(etablissement, period, parameters):
        #par rapport à précedement, ajout consommation_charbon_combustible_electricite_petits_producteurs
        
        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement('consommation_autres_produits_energetique_ticc', period)


        #les quatres sont à exclure de l'assiette, également pour consommation_charbon_combustible_electricite
        consommation_charbon_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        consommation_charbon_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        consommation_charbon_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)
        
        #la dernière est exclus de consommation_charbon_combustible_electricite
        consommation_charbon_combustible_electricite = etablissement("consommation_charbon_combustible_electricite", period)
        consommation_charbon_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)

        assiette = consommation_charbon + consommation_autres_produits_energetique_ticc - ( consommation_charbon_combustible_interne + (consommation_charbon_combustible_electricite  - consommation_charbon_combustible_electricite_petits_producteurs) + consommation_charbon_combustible_extraction + consommation_charbon_combustible_particuliers )

        return assiette

    def formula_2016_01_01(etablissement, period, parameters):
        #par rapport à précedement, supprimer consommation_charbon_combustible_particuliers
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement('consommation_autres_produits_energetique_ticc', period)


        #ces trois  sont à exclure de l'assiette, également pour consommation_charbon_combustible_electricite
        consommation_charbon_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        consommation_charbon_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        
        #consommation_charbon_combustible_electricite_petits_producteurs est exclus de l'éxoneration
        consommation_charbon_combustible_electricite = etablissement("consommation_charbon_combustible_electricite", period)
        consommation_charbon_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)

        assiette = consommation_charbon + consommation_autres_produits_energetique_ticc - ( consommation_charbon_combustible_interne + (consommation_charbon_combustible_electricite - consommation_charbon_combustible_electricite_petits_producteurs) + consommation_charbon_combustible_extraction )

        return assiette
    def formula_2020_01_01(etablissement, period, parameters):
        #à partir de 2020, charbon utilisé comme carburant est prise en compte 
        
        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement('consommation_autres_produits_energetique_ticc', period)


        #les trois suivants sont des réductions net de l'assiette, également pour consommation_charbon_combustible_electricite
        consommation_charbon_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        consommation_charbon_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        
        #consommation_charbon_combustible_electricite_petits_producteurs est exclus de consommation_charbon_combustible_electricite
        consommation_charbon_combustible_electricite = etablissement("consommation_charbon_combustible_electricite", period)
        consommation_charbon_combustible_electricite_petits_producteurs = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        assiette = consommation_charbon  + consommation_autres_produits_energetique_ticc - ( consommation_charbon_combustible_interne + (consommation_charbon_combustible_electricite - consommation_charbon_combustible_electricite_petits_producteurs) + consommation_charbon_combustible_extraction )
        #ajout conso_carburant * installation_cogeneration, supprimer conso_combustible_electricite_266qA * contrat_achat_electricite_314, 

        return assiette

        #2022: autoconsommation (L312-17), consommation_charbon_combustible_electricite (-32), consommation_charbon_combustible_interne >= pense à changer à auto_conommation (-31)
        #également pour le charbon
        #NB -34, chaleur >= carburant 
        #ajouter un engin_non_routier (-35) ?
        

from openfisca_core.periods import Instant

class instant_electrite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Coal consumption taxable according to TICC"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"  #

    def formula_2007_01_01(etablissement, period, parameters):
      total = parameters(Instant((2023, 2, 1))).energies.bouclier_tarifaire.majoration_tccfe_maximum
      return total 
# parameters(Instant((YYYY, MM, DD)))