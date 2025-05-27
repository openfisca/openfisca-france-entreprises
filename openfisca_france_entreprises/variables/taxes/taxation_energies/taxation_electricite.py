from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class taxe_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""  #
    def formula_2002_01_01(etablissement, period, parameters):
        taxe_contribution_service_public_electricite = etablissement('taxe_contribution_service_public_electricite', period)


        total = taxe_contribution_service_public_electricite

        return total 


    def formula_2011_01_01(etablissement, period, parameters):
        taxe_interieure_sur_consommation_finale_electricite = etablissement('taxe_interieure_sur_consommation_finale_electricite', period)
        taxe_communale_consommation_finale_electricite = etablissement('taxe_communale_consommation_finale_electricite', period)
        taxe_departementale_consommation_finale_electricite = etablissement('taxe_departementale_consommation_finale_electricite', period)
        #on a pas de données pour les tdcfe et tccfe avant 2011 
        taxe_contribution_service_public_electricite = etablissement('taxe_contribution_service_public_electricite', period)
        #la cspe est mis en compte pour la totale jusqu'à 2015 (inclus)


        total = taxe_contribution_service_public_electricite + taxe_interieure_sur_consommation_finale_electricite + taxe_communale_consommation_finale_electricite + taxe_departementale_consommation_finale_electricite
        return total 
    
    def formula_2016_01_01(etablissement, period, parameters):
        #la cspe n'existait plus dès cette année
        #dès 2020, les parametres des tdcfe et tccfe sont généré sous l'hypothese que les coefficients ont une tendance de s'augmenter dès 2021 jusqu'à la borne, avant de s'intégrer dans l'accise
        taxe_interieure_sur_consommation_finale_electricite = etablissement('taxe_interieure_sur_consommation_finale_electricite', period)
        taxe_communale_consommation_finale_electricite = etablissement('taxe_communale_consommation_finale_electricite', period)
        taxe_departementale_consommation_finale_electricite = etablissement('taxe_departementale_consommation_finale_electricite', period)

        total = taxe_interieure_sur_consommation_finale_electricite + taxe_communale_consommation_finale_electricite + taxe_departementale_consommation_finale_electricite
        return total 
    

    def formula_2022_01_01(etablissement, period, parameters):
        #en 2022, la tdcfe est intégrée dans l'accise, un ans avant ça n'arrive à la tccfe
        #mais exceptionellement, on a le bouclier tarifaire qui remplace le rôle de l'accise 
        #due au fait que les montants sont calculés en unité des années, on divise le grand montant par 12
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)
        taxe_electricite_bouclier_tarifaire = etablissement('taxe_electricite_bouclier_tarifaire', period)
        taxe_communale_consommation_finale_electricite = etablissement('taxe_communale_consommation_finale_electricite', period)
        if taxe_accise_electricite == 0: 
            total = taxe_communale_consommation_finale_electricite 
        else : 
            total = taxe_accise_electricite/12 + taxe_electricite_bouclier_tarifaire*11/12 + taxe_communale_consommation_finale_electricite 
        return total 
    
    def formula_2023_01_01(etablissement, period, parameters):
        #la difference entre 2022 et 2023 est que en 2023, on a pas d'accise et qu'un mois de la tccfe qui égale celle en 2022
        #en 2022, la tdcfe est intégrée dans l'accise, un an avant ça n'arrive à la tccfe
        #mais exceptionellement, on a le bouclier tarifaire qui remplace le rôle de l'accise 
        #due au fait que les montants sont calculés en unité des années, on divise le grand montant par 12
        taxe_electricite_bouclier_tarifaire = etablissement('taxe_electricite_bouclier_tarifaire', period) #2024-02-01
        taxe_communale_consommation_finale_electricite = etablissement('taxe_communale_consommation_finale_electricite', period)
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)

        if taxe_accise_electricite == 0:
            total = taxe_communale_consommation_finale_electricite/12 # pour janvier
        else :
            total = taxe_electricite_bouclier_tarifaire + taxe_communale_consommation_finale_electricite/12 # pour janvier
        return total 
    
    def formula_2024_01_01(etablissement, period, parameters):
        #exceptionalement, le premier mois en 2022 nous appelle l'usage continue de la tccfe. et les taux - on assume - sont pareils que ceux de 2022
        taxe_electricite_bouclier_tarifaire = etablissement('taxe_electricite_bouclier_tarifaire', period)
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)

        if taxe_accise_electricite == 0:
            total = 0
        else :
            total = taxe_electricite_bouclier_tarifaire
        return total 
    
    def formula_2025_01_01(etablissement, period, parameters):
        #exceptionalement, le premier mois en 2022 nous appelle l'usage continue de la tccfe. et les taux - on assume - sont pareils que ceux de 2022
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)
        taxe_electricite_bouclier_tarifaire = etablissement('taxe_electricite_bouclier_tarifaire', period)

        if taxe_accise_electricite == 0:
            total = 0
        else :
            total = taxe_accise_electricite*11/12 + taxe_electricite_bouclier_tarifaire/12 #que pour janvier
        return total 
        

class taxe_contribution_service_public_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Contribution au Servie Public de l'Électricité"
    reference = ""  #
    def formula_2002_01_01(etablissement, period, parameters):
        
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        montant = assiette_taxe_electricite * parameters(period).energies.electricite.cspe

        return montant
    
    #condition d'application est pareil jusqu'à 2011

class taxe_interieure_sur_consommation_finale_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""  #
    def formula_2011_01_01(etablissement, period, parameters):
        """
        https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=1.-,Il%20est%20institu%C3%A9,-une%20taxe%20int%C3%A9rieure
        """
        electricite_production_a_bord = etablissement("electricite_production_a_bord", period)
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement('electricite_transport_guide',period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement('electricite_fabrication_produits_mineraux_non_metalliques',period)
        electricite_production_biens_electro_intensive = etablissement('electricite_production_biens_electro_intensive',period)
        electricite_production_electricite = etablissement('electricite_production_electricite', period)
        installation_grande_consommatrice_energie = etablissement('installation_grande_consommatrice_energie', period)

        amperage = etablissement("amperage", period)

        if amperage != 0 and amperage <= parameters(period).energies.electricite.ticfe.categorie_fiscale_haut_puissance  : #la taxe s'applique seulement aux grandes consommatrice d'électricité
            taxe = 0                                                                    
            #faut avoir un amperage pour s'exonerer de cette taxe 
        elif electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0
        elif electricite_production_a_bord == True:
            taxe = 0
        elif electricite_production_electricite == True:
            taxe = 0
        elif electricite_transport_guide == True: 
            taxe = 0
        elif installation_grande_consommatrice_energie == True:
            taxe = 0
        else : 
            taxe = etablissement("taxe_accise_electricite_taux_normal", period)
        

        summation = taxe 
        return summation
    
    def formula_2016_01_01(etablissement, period, parameters):
        """
        https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=1.-,Il%20est%20institu%C3%A9,-une%20taxe%20int%C3%A9rieure
        """
        electricite_production_a_bord = etablissement("electricite_production_a_bord", period)
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement('electricite_fabrication_produits_mineraux_non_metalliques',period)
        electricite_production_biens_electro_intensive = etablissement('electricite_production_biens_electro_intensive',period)
        electricite_production_electricite = etablissement('electricite_production_electricite', period)
        electricite_installations_industrielles_electro_intensives = etablissement('electricite_installations_industrielles_electro_intensives', period)
        electricite_installations_industrielles_hyper_electro_intensives = etablissement('electricite_installations_industrielles_hyper_electro_intensives', period)
        electricite_transport_guide = etablissement('electricite_transport_guide', period)
        risque_de_fuite_carbone_eta = etablissement('risque_de_fuite_carbone_eta', period)



        if electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0   
        elif electricite_production_a_bord == True:
            taxe = 0
        elif electricite_production_electricite == True:
            taxe = 0
        elif electricite_installations_industrielles_hyper_electro_intensives == True:
            taxe = etablissement('taxe_electricite_installations_industrielles_hyper_electro_intensives', period)
        elif electricite_installations_industrielles_electro_intensives == True:
            taxe = etablissement('taxe_electricite_installations_industrielles_electro_intensives', period)
        elif electricite_transport_guide == True: 
            taxe = etablissement("taxe_electricite_transport_guide",period)
            #dès 1 janvier 2017, ça comprends l'autobus hybride rechargeable ou électrique
        elif risque_de_fuite_carbone_eta == True:
            taxe = etablissement('taxe_electricite_risque_de_fuite_de_carbone', period)
            
        else : 
            taxe = etablissement("taxe_accise_electricite_taux_normal", period)


        summation = taxe 
        return summation
    
    
    def formula_2019_01_01(etablissement, period, parameters):
        """
        https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=1.-,Il%20est%20institu%C3%A9,-une%20taxe%20int%C3%A9rieure
        """
        electricite_production_a_bord = etablissement("electricite_production_a_bord", period)
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement('electricite_fabrication_produits_mineraux_non_metalliques',period)
        electricite_production_biens_electro_intensive = etablissement('electricite_production_biens_electro_intensive',period)
        electricite_production_electricite = etablissement('electricite_production_electricite', period)
        electricite_installations_industrielles_electro_intensives = etablissement('electricite_installations_industrielles_electro_intensives', period)
        electricite_installations_industrielles_hyper_electro_intensives = etablissement('electricite_installations_industrielles_hyper_electro_intensives', period)
        electricite_transport_guide = etablissement('electricite_transport_guide', period)
        risque_de_fuite_carbone_eta = etablissement('risque_de_fuite_carbone_eta', period)
        electricite_centres_de_stockage_donnees = etablissement('electricite_centres_de_stockage_donnees', period)
        electricite_exploitation_aerodrome = etablissement('electricite_exploitation_aerodrome', period)



        if electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0   
        elif electricite_production_a_bord == True:
            taxe = 0
        elif electricite_production_electricite == True:
            taxe = 0
        elif electricite_installations_industrielles_hyper_electro_intensives == True:
            taxe = etablissement('taxe_electricite_installations_industrielles_hyper_electro_intensives', period)
        elif electricite_installations_industrielles_electro_intensives == True:
            taxe = etablissement('taxe_electricite_installations_industrielles_electro_intensives', period)
        elif electricite_transport_guide == True: 
            taxe = etablissement("taxe_electricite_transport_guide",period)
            #dès 1 janvier 2017, ça comprends l'autobus hybride rechargeable ou électrique
        elif risque_de_fuite_carbone_eta == True:
            taxe = etablissement('taxe_electricite_risque_de_fuite_de_carbone', period)
        elif electricite_centres_de_stockage_donnees == True:
            taxe = etablissement("taxe_electricite_centres_de_stockage_donnees",period)
        elif electricite_exploitation_aerodrome == True :        
            taxe = etablissement("taxe_electricite_exploitation_aerodrome",period)
        else : 
            taxe = etablissement("taxe_accise_electricite_taux_normal", period)


        summation = taxe 
        return summation
    
    
#taxe_accise_electricite
#Taxe Intérieure sur la Consommation Finale d'Électricité (TICFE), anciennement appelée CSPE (Contribution au Service Public de l'Électricité). 
class taxe_accise_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""  #
    #aussi ticfe selon la période 
    def formula_2022_01_01(etablissement, period, parameters):
        """à partir de maintenant, c'est l'accise 
        """
        #voici les conditions à appliquer 
        electro_intensive_activite_industrielle = etablissement("electro_intensive_activite_industrielle", period)
        electro_intensive_concurrence_internationale  = etablissement("electro_intensive_concurrence_internationale", period)
        electricite_centres_de_stockage_donnees = etablissement('electricite_centres_de_stockage_donnees', period)
        electricite_transport_collectif_personnes = etablissement('electricite_transport_collectif_personnes', period)
        electricite_exploitation_aerodrome = etablissement('electricite_exploitation_aerodrome', period)
        electricite_production_a_bord = etablissement("electricite_production_a_bord", period)
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement('electricite_transport_guide',period)
        electricite_alimentation_a_quai = etablissement('electricite_alimentation_a_quai', period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement('electricite_fabrication_produits_mineraux_non_metalliques',period)
        electricite_production_biens_electro_intensive = etablissement('electricite_production_biens_electro_intensive',period)
        electro_intensite = etablissement('electro_intensite', period)
        electricite_production_electricite = etablissement('electricite_production_electricite', period)


        if electricite_production_a_bord == True:
            taxe = 0
        elif electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0   
        elif electricite_production_electricite == True:
            taxe = 0
        elif electricite_transport_guide == True: 
            taxe = etablissement("taxe_electricite_transport_guide",period)
        elif electricite_transport_collectif_personnes == True:        
            taxe = etablissement("taxe_electricite_transport_collectif_personnes",period)
        elif electricite_alimentation_a_quai == True:
            taxe = etablissement('taxe_electricite_alimentation_a_quai',period)
        elif electro_intensive_concurrence_internationale == True:
            taxe = etablissement("taxe_accise_electricite_electro_intensive_concurrence_internationale",period)
        elif electro_intensive_activite_industrielle == True:
            taxe = etablissement("taxe_accise_electricite_electro_intensive_activite_industrielle",period)
        elif electricite_exploitation_aerodrome == True and electro_intensite > parameters(period).energies.electricite.ticfe.aerodromes_electro_intensite.yaml:        
            taxe = etablissement("taxe_electricite_exploitation_aerodrome",period)
        elif electricite_centres_de_stockage_donnees == True:
            taxe = etablissement("taxe_electricite_centres_de_stockage_donnees",period)
        else: 
            taxe = etablissement("taxe_accise_electricite_taux_normal", period)
        
        #voici toutes les autres formes de la taxe

        summation = taxe 
        return summation
    
    def formula_2023_01_01(etablissement, period, parameters):
        """par rapport à précedement, ajouté manutention_portuaire, réf : L312-48
        """
        #voici les conditions à appliquer 
        electro_intensive_activite_industrielle = etablissement("electro_intensive_activite_industrielle", period)
        electro_intensive_concurrence_internationale  = etablissement("electro_intensive_concurrence_internationale", period)
        electricite_centres_de_stockage_donnees = etablissement('electricite_centres_de_stockage_donnees', period)
        electricite_transport_collectif_personnes = etablissement('electricite_transport_collectif_personnes', period)
        electricite_manutention_portuaire = etablissement('electricite_manutention_portuaire',  period)
        electricite_exploitation_aerodrome = etablissement('electricite_exploitation_aerodrome', period)
        electricite_production_a_bord = etablissement("electricite_production_a_bord", period)
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement('electricite_transport_guide',period)
        electricite_alimentation_a_quai = etablissement('electricite_alimentation_a_quai', period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement('electricite_fabrication_produits_mineraux_non_metalliques',period)
        electricite_production_biens_electro_intensive = etablissement('electricite_production_biens_electro_intensive',period)
        electricite_production_electricite = etablissement('electricite_production_electricite', period)


        if electricite_production_a_bord == True:
            taxe = 0
        elif electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0
        elif electricite_production_electricite == True:
            taxe = 0
        elif electricite_transport_guide == True: 
            taxe = etablissement("taxe_electricite_transport_guide",period)
        elif electricite_transport_collectif_personnes == True:        
            taxe = etablissement("taxe_electricite_transport_collectif_personnes",period)
        elif electricite_manutention_portuaire == True:        
            taxe = etablissement("taxe_electricite_manutention_portuaire",period)
        elif electricite_alimentation_a_quai == True:
            taxe = etablissement('taxe_electricite_alimentation_a_quai',period)
        elif electro_intensive_concurrence_internationale == True:
            taxe = etablissement("taxe_accise_electricite_electro_intensive_concurrence_internationale",period)
        elif electro_intensive_activite_industrielle == True:
            taxe = etablissement("taxe_accise_electricite_electro_intensive_activite_industrielle",period)
        elif electricite_exploitation_aerodrome == True:        
            taxe = etablissement("taxe_electricite_exploitation_aerodrome",period)
        elif electricite_centres_de_stockage_donnees == True:
            taxe = etablissement("taxe_electricite_centres_de_stockage_donnees",period)
        else: 
            taxe = etablissement("taxe_accise_electricite_taux_normal", period)
        
        #voici toutes les autres formes de la taxe

        summation = taxe 
        return summation
    
    def formula_2025_01_01(etablissement, period, parameters):
        """par rapport à précedement, ajouté consommation_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques et consommation_alimentation_aeronefs_stationnement_aerodromes_activites_economiques
        """
        #voici les conditions à appliquer 
        electro_intensive_activite_industrielle = etablissement("electro_intensive_activite_industrielle", period)
        electro_intensive_concurrence_internationale  = etablissement("electro_intensive_concurrence_internationale", period)
        electricite_centres_de_stockage_donnees = etablissement('electricite_centres_de_stockage_donnees', period)
        electricite_transport_collectif_personnes = etablissement('electricite_transport_collectif_personnes', period)
        electricite_manutention_portuaire = etablissement('electricite_manutention_portuaire',  period)
        electricite_exploitation_aerodrome = etablissement('electricite_exploitation_aerodrome', period)
        electricite_production_a_bord = etablissement("electricite_production_a_bord", period)
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement('electricite_transport_guide',period)
        electricite_alimentation_a_quai = etablissement('electricite_alimentation_a_quai', period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement('electricite_fabrication_produits_mineraux_non_metalliques',period)
        electricite_production_biens_electro_intensive = etablissement('electricite_production_biens_electro_intensive',period)
        electricite_production_electricite = etablissement('electricite_production_electricite', period)
        electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques = etablissement('electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques', period)
        electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques = etablissement('electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques', period)

        if electricite_production_a_bord == True:
            taxe = 0
        elif electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0
        elif electricite_production_electricite == True:
            taxe = 0
        elif electricite_transport_guide == True: 
            taxe = etablissement("taxe_electricite_transport_guide",period)
        elif electricite_transport_collectif_personnes == True:        
            taxe = etablissement("taxe_electricite_transport_collectif_personnes",period)
        elif electricite_manutention_portuaire == True:        
            taxe = etablissement("taxe_electricite_manutention_portuaire",period)
        elif electricite_alimentation_a_quai == True:
            taxe = etablissement('taxe_electricite_alimentation_a_quai',period)
        elif electro_intensive_concurrence_internationale == True:
            taxe = etablissement("taxe_accise_electricite_electro_intensive_concurrence_internationale",period)
        elif electro_intensive_activite_industrielle == True:
            taxe = etablissement("taxe_accise_electricite_electro_intensive_activite_industrielle",period)
        elif electricite_exploitation_aerodrome == True:        
            taxe = etablissement("taxe_electricite_exploitation_aerodrome",period)
        elif electricite_centres_de_stockage_donnees == True:
            taxe = etablissement("taxe_electricite_centres_de_stockage_donnees",period)
        elif electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques == True :
            taxe = etablissement('taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques',period)
        elif electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques == True :
            taxe = etablissement('taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques',period)
        else: 
            taxe = etablissement("taxe_accise_electricite_taux_normal", period)
        
        #voici toutes les autres formes de la taxe

        summation = taxe 
        return summation
    
# class verifie_periode(Variable): 
#     value_type = float
#     entity = Etablissement
#     definition_period = YEAR
#     def formula_2025_01_01(etablissement, period, parameters):
#         taux = parameters(period).energies.electricite.ticfe.alimentation_aeronefs_stationnement_aerodromes_activites_economiques
        
#         return taux


class taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques(Variable): 
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2025_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite', period)


        taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.alimentation_aeronefs_stationnement_aerodromes_activites_economiques
        

        return taxe 
    
class taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques(Variable): 
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2025_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite', period)


        taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques
        

        return taxe 

class taxe_electricite_risque_de_fuite_de_carbone(Variable): 
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2016_01_01(etablissement, period, parameters):
        consommation_par_valeur_ajoutee = etablissement('consommation_par_valeur_ajoutee', period)
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite', period)

        if consommation_par_valeur_ajoutee >= 0.003 :
            taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.risque_de_fuite_de_carbone.taux_plus_de_3kWh_par_valeur_ajoutee
        elif consommation_par_valeur_ajoutee >= 0.0015 :
            taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.risque_de_fuite_de_carbone.taux_1_virgule_5_a_3kWh_par_valeur_ajoutee
        else:
            taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.risque_de_fuite_de_carbone.taux_moins_de_1_virgule_5kWh_par_valeur_ajoutee
        

        return taxe 


class taxe_electricite_installations_industrielles_hyper_electro_intensives(Variable): 
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2016_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite',period)
        
        taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.electro_intensive.hyperelectro_intensive
        

        return taxe 



class taxe_electricite_installations_industrielles_electro_intensives(Variable): 
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2016_01_01(etablissement, period, parameters):
        consommation_par_valeur_ajoutee = etablissement('consommation_par_valeur_ajoutee', period)
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite', period)

        if consommation_par_valeur_ajoutee >= 0.003 :
            taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.electro_intensive.taux_plus_de_3kWh_par_valeur_ajoutee
        elif consommation_par_valeur_ajoutee >= 0.0015 :
            taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.electro_intensive.taux_1_virgule_5_a_3kWh_par_valeur_ajoutee
        else:
            taxe =  assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.electro_intensive.taux_moins_de_1_virgule_5kWh_par_valeur_ajoutee
        

        return taxe 


class taxe_electricite_alimentation_a_quai(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(period).energies.electricite.ticfe.alimentation_a_quai
        taxe = assiette_taxe_electricite * taux
        return taxe


class taxe_electricite_exploitation_aerodrome(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2019_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(period).energies.electricite.ticfe.aerodromes
        taxe = assiette_taxe_electricite * taux
        return taxe


class taxe_electricite_manutention_portuaire(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(period).energies.electricite.ticfe.manutention_portuaire
        taxe = assiette_taxe_electricite * taux
        return taxe


class taxe_electricite_transport_collectif_personnes(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(period).energies.electricite.ticfe.transport_collectif_personnes
        taxe = assiette_taxe_electricite * taux
        return taxe


class taxe_electricite_transport_guide(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2016_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(period).energies.electricite.ticfe.transport_guide
        taxe = assiette_taxe_electricite * taux
        return taxe


class taxe_electricite_centres_de_stockage_donnees(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2019_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        
        if assiette_taxe_electricite > 1000 : 
            taxe = 1000 * parameters(period).energies.electricite.ticfe.taux_normal + (assiette_taxe_electricite - 1000) * parameters(period).energies.electricite.ticfe.data_center #la portion qui dépasse un gigawatt
        else : 
            taux = parameters(period).energies.electricite.ticfe.taux_normal
            taxe = assiette_taxe_electricite * taux

        return taxe

    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(period).energies.electricite.ticfe.data_center
        taxe = assiette_taxe_electricite * taux
        return taxe


class taxe_accise_electricite_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-37"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=Les%20tarifs%20normaux%20de%20l%27accise%2C%20exprim%C3%A9s%20en%20euros%20par%20m%C3%A9gawattheure%2C%20sont%2C%20en%202015%2C%20pour%20chacune%20des%20cat%C3%A9gories%20fiscales%20de%20l%27%C3%A9lectricit%C3%A9%2C%20les%20suivants%20%3A"  #

    def formula_2011_01_01(etablissement, period, parameters):
        
        """
        2011-01-01:
            value: 0.5
        2016-01-01:
            value: 22.5
        2022-01-01:
            value: 22.5
        """
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        
        taxe = assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.taux_normal

        return taxe


    def formula_2021_01_01(etablissement, period, parameters):
        """
        """
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        consommation_electricite_fournie_aux_navires = etablissement('consommation_electricite_fournie_aux_navires', period)

        taxe_electricite_fournie_aux_navires = consommation_electricite_fournie_aux_navires * parameters(period).energies.electricite.ticfe.electricite_fournie_aux_navires

        reste = assiette_taxe_electricite - taxe_electricite_fournie_aux_navires
        
        taxe = reste*parameters(period).energies.electricite.ticfe.taux_normal


        tout = taxe + taxe_electricite_fournie_aux_navires

        return tout 
    
    def formula_2022_01_01(etablissement, period, parameters):
        
        """
        """
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        amperage = etablissement("amperage", period)
        if amperage != 0 and amperage < parameters.energies.electricite.ticfe.categorie_fiscale_petite_et_moyenne_entreprise : 
            taxe = assiette_taxe_electricite*parameters(period).energies.electricite.ticfe.taux_normal_36kVA_et_moins
        elif amperage != 0 and amperage < parameters(period).energies.electricite.ticfe.categorie_fiscale_haut_puissance :
            taxe = assiette_taxe_electricite*parameters(period).energies.electricite.ticfe.taux_normal_36_a_250kVA
        else : 
            taxe = assiette_taxe_electricite*parameters(period).energies.electricite.ticfe.taux_normal #haut puissance, > 250 kVA

        return taxe

class taxe_accise_electricite_electro_intensive_activite_industrielle(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "sous L312-65"
    reference = ""  #

    def formula_2022_01_01(etablissement, period, parameters):
        """
            
        """
        electro_intensite = etablissement("electro_intensite", period)
        electro_intensive_activite_industrielle = etablissement('electro_intensive_activite_industrielle', period)
    
        assiette = etablissement("assiette_taxe_electricite", period)
        if electro_intensive_activite_industrielle == True:
            if electro_intensite != 0 and electro_intensite < 0.5: 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.activite_industrielle.electro_intensive_0_virgule_5
            elif  electro_intensite != 0 and electro_intensite < 3.375: 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.activite_industrielle.electro_intensive_3_virgule_375
            else:
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.activite_industrielle.electro_intensive_6_virgule_75
            
        
        return taxe


class taxe_accise_electricite_electro_intensive_concurrence_internationale(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-65"
    reference = ""  #

    def formula_2022_01_01(etablissement, period, parameters):
        """
        """
        electro_intensite = etablissement("electro_intensite", period)
    
        assiette = etablissement("assiette_taxe_electricite", period)
        risque_de_fuite_carbone_eta = etablissement("risque_de_fuite_carbone_eta",period)
        intensite_echanges_avec_pays_tiers = etablissement("intensite_echanges_avec_pays_tiers", period)
        electro_intensive_concurrence_internationale = etablissement('electro_intensive_concurrence_internationale',period)
        
        if electro_intensive_concurrence_internationale == True:
            
            if electro_intensite > 13.5 and risque_de_fuite_carbone_eta == True and intensite_echanges_avec_pays_tiers > 25 : 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_13_virgule_5
                                                    #energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_13_virgule_5
            elif electro_intensite > 6.75 : 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_6_virgule_75

            elif electro_intensite > 3.375 :
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_3_virgule_375

            else :
                taxe = assiette * parameters(period).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_0_virgule_5
        return taxe


class assiette_taxe_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "assiette de la Taxe Intérieure sur la Consommation Finale d'Électricité"
    reference = ""  #
    def formula_2002_01_01(etablissement, period, parameters):
        #sous CPSE
        consommation_electricite = etablissement("consommation_electricite", period)

        return consommation_electricite

    def formula_2011_01_01(etablissement, period, parameters):
        #sous TICFE, TCCFE, TDCFE
        consommation_electricite = etablissement("consommation_electricite", period)
        consommation_electricite_petite_producteur_electricite = etablissement('consommation_electricite_petite_producteur_electricite', period)
        consommation_electricite_auto_consommation = etablissement("consommation_electricite_auto_consommation",period)


        return consommation_electricite - (consommation_electricite_petite_producteur_electricite + consommation_electricite_auto_consommation)

    def formula_2017_01_01(etablissement, period, parameters):
        consommation_electricite = etablissement("consommation_electricite", period)
        consommation_electricite_petite_producteur_electricite = etablissement('consommation_electricite_petite_producteur_electricite', period)
        consommation_electricite_auto_consommation = etablissement("consommation_electricite_auto_consommation",period)
        consommation_electricite_puissance_moins_1_MW = etablissement('consommation_electricite_puissance_moins_1_MW', period)

        return consommation_electricite - (consommation_electricite_puissance_moins_1_MW + consommation_electricite_petite_producteur_electricite + consommation_electricite_auto_consommation)



    def formula_2022_01_01(etablissement, period, parameters):
        
        """https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635#:~:text=Rel%C3%A8ve%20d%27un%20tarif%20particulier%20de%20l%27accise
        """
        consommation_electricite = etablissement("consommation_electricite", period)

        consommation_electricite_energie_ou_gaz_renouvelable = etablissement("consommation_electricite_energie_ou_gaz_renouvelable",period)
        consommation_electricite_puissance_moins_1_MW = etablissement("consommation_electricite_puissance_moins_1_MW",period)
        consommation_electricite_auto_consommation = etablissement("consommation_electricite_auto_consommation",period)

        return consommation_electricite - (consommation_electricite_energie_ou_gaz_renouvelable + consommation_electricite_puissance_moins_1_MW + consommation_electricite_auto_consommation)
