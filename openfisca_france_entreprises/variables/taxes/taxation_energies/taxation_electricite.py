from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

class taxe_interieure_consummation_finale_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Taxe Intérieure sur la Consommation Finale d'Électricité (TICFE), anciennement appelée CSPE (Contribution au Service Public de l'Électricité). "
    reference = ""  #

    def formula_2022_01_01(etablissement, period, parameters):
        """
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
        
        
        if electro_intensive_activite_industrielle == True:
            taxe = etablissement("taxe_interieure_taxation_electricite_electro_intensive_activite_industrielle",period)
        elif electro_intensive_concurrence_internationale == True:
            taxe = etablissement("taxe_interieure_taxation_electricite_electro_intensive_concurrence_internationale",period)
        elif electricite_transport_guide == True: 
            taxe = etablissement("taxe_electricite_transport_guide",period)
        elif electricite_centres_de_stockage_donnees == True:
            taxe = etablissement("taxe_electricite_centres_de_stockage_données",period)
        elif electricite_transport_collectif_personnes == True:        
            taxe = etablissement("taxe_electricite_transport_collectif_personnes",period)
        elif electricite_manutention_portuaire == True:        
            taxe = etablissement("taxe_electricite_manutention_portuaire",period)
        elif electricite_exploitation_aerodrome == True:        
            taxe = etablissement("taxe_electricite_exploitation_aerodrome",period)
        elif electricite_alimentation_a_quai == True:
            taxe = etablissement('electricite_alimentation_a_quai',period)
        elif electricite_production_a_bord == True:
        #faut lister les activités desquelles le taux est 0
            taxe = 0
        elif electricite_double_usage == True: 
            taxe = 0
        elif electricite_fabrication_produits_mineraux_non_metalliques == True: 
            taxe = 0
        elif electricite_production_biens_electro_intensive == True:
            taxe = 0
        else: 
            taxe = etablissement("taxe_interieure_taxation_electricite_taux_normal", period)
        
        #voici toutes les autres formes de la taxe

        summation = taxe 
        return summation



class taxe_electricite_production_a_bord(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.alimentation_a_quai
        taxe = assiette_ticfe * taux
        return taxe
   


class taxe_electricite_alimentation_a_quai(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.alimentation_a_quai
        taxe = assiette_ticfe * taux
        return taxe
   
class taxe_electricite_exploitation_aerodrome(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.aerodrome
        taxe = assiette_ticfe * taux
        return taxe

class taxe_electricite_manutention_portuaire(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.manutention_portuaire
        taxe = assiette_ticfe * taux
        return taxe

class taxe_electricite_transport_collectif_personnes(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.transport_collectif_personnes
        taxe = assiette_ticfe * taux
        return taxe

class taxe_electricite_transport_guide(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.transport_guide
        taxe = assiette_ticfe * taux
        return taxe

class taxe_electricite_centres_de_stockage_données(Variable): 
    #celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_ticfe = etablissement("assiette_ticfe",period)
        taux = parameters(period).energies.electricite.ticfe.data_center
        taxe = assiette_ticfe * taux
        return taxe

class taxe_interieure_taxation_electricite_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-65"
    reference = ""  #

    def formula_2020_01_01(etablissement, period, parameters):
        #faut changer la date après
        """
        """
        assiette_ticfe = etablissement("assiette_ticfe", period)
        amperage = etablissement("amperage", period)
        if amperage < 36 :
            taxe = assiette_ticfe*parameters(period).energies.electricite.ticfe.taux_normal_36kVA_et_moins
        elif amperage < 250 :
            taxe = assiette_ticfe*parameters(period).energies.electricite.ticfe.taux_normal_36_a_250kVA
        else : 
            taxe = assiette_ticfe*parameters(period).energies.electricite.ticfe.taux_normal

        return taxe


class taxe_interieure_taxation_electricite_electro_intensive_activite_industrielle(Variable):
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
    
        assiette = etablissement("assiette_ticfe", period)
        if electro_intensive_activite_industrielle == True:
            if electro_intensite < 0.5: 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.activite_industrielle.electrointensive_0_virgule_5
            elif electro_intensite < 3.375: 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.activite_industrielle.electrointensive_3_virgule_375
            else:
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.activite_industrielle.electrointensive_6_virgule_75
            
        
        return taxe




class taxe_interieure_taxation_electricite_electro_intensive_concurrence_internationale(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-65"
    reference = ""  #

    def formula_2022_01_01(etablissement, period, parameters):
        """
        """
        electro_intensite = etablissement("electro_intensite", period)
    
        assiette = etablissement("assiette_ticfe", period)
        risque_de_fuite_carbone_eta = etablissement("risque_de_fuite_carbone_eta",period)
        intensite_echanges_avec_pays_tiers = etablissement("intensite_echanges_avec_pays_tiers", period)
        electro_intensive_concurrence_internationale = etablissement('electro_intensive_concurrence_internationale',period)
        
        if electro_intensive_concurrence_internationale == True:
            
            if electro_intensite > 13.5 and risque_de_fuite_carbone_eta == True and intensite_echanges_avec_pays_tiers > 25 : 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.concurrence_internationale.electrointensive_13_virgule_5
                                                    #energies.electricite.ticfe.electrointensive.concurrence_internationale.electrointensive_13_virgule_5
            elif electro_intensite > 6.75 : 
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.concurrence_internationale.electrointensive_6_virgule_75

            elif electro_intensite > 3.375 :
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.concurrence_internationale.electrointensive_3_virgule_375

            else :
                taxe = assiette * parameters(period).energies.electricite.ticfe.electrointensive.concurrence_internationale.electrointensive_0_virgule_5
        #Il y a pas une pre-caution contre la situation où la taxe ne s'applique à ce qui est saisi
        return taxe
    



class assiette_ticfe(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "assiette de la Taxe Intérieure sur la Consommation Finale d'Électricité"
    reference = ""  #
#faut avoir une formule avant 2024
    def formula_2022_01_01(etablissement, period, parameters):
        """Selon L312-64
        """
        consommation_electricite = etablissement("consommation_electricite", period)

        consommation_electricite_energie_ou_gaz_renouvelable = etablissement("consommation_electricite_energie_ou_gaz_renouvelable",period)
        consommation_electricite_puissance_moins_1_MW = etablissement("consommation_electricite_puissance_moins_1_MW",period)
        consommation_electricite_auto_consommation = etablissement("consommation_electricite_auto_consommation",period)

        return consommation_electricite - (consommation_electricite_energie_ou_gaz_renouvelable+ consommation_electricite_puissance_moins_1_MW + consommation_electricite_auto_consommation)
