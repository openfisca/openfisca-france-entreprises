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


class taxe_interieure_consommation_sur_produits_energetiques(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"  #
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
    #NB : pour cette variable, j'ai commencé avec l'année 2021, puis j'ai traveilé en inverse. Donc, les changements sont par rapport à l'année suivante, pas precedante. 
    
    #les changements décrits en dessous sont remarqués par rapport aux années suivantes ; ils s'appliquent aux années précédents
    #2000
    #rien de changements
    #2001
    #rien de changements 
    #2002
    #beaucoup de changements à vérfier 
    #fioul autre, 27 n'exist que pour 2002, exemption
    #Fiouls lourds 28, 28 bis taxable > vérifie rélation à 24 pour 2003
    #
    #2003 
    #pas de changements
    #2004
    #les majorations regionales n'existent pas, tandis que les autres majorations par l'état 
    #2006
    #“2. Une réfaction peut être effectuée sur les taux de taxe intérieure de consommation applicable 
    # au supercarburant repris aux indices d'identification 11 et 11 ter et au gazole repris à 
    # l'indice d'identification 22. A compter du 1er janvier 2006, le montant de cette réfaction 
    # est de 1,77 euro par hectolitre pour le supercarburant et de 1,15 euro par hectolitre pour le gazole.”
    # *** TODO: mais où peut-on trouver qui est concerné par cette majoration ? ^
    
    #consommation_supercarburant_e85 
    #^exempté
    def formula_2000_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            # + etablissement('consommation_supercarburant_e10', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            # + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL (combiner en une variable de consommation)
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            # + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre


            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            # + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            + etablissement('consommation_carbureacteurs_essence_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    #2007
    #(par rapport à précédement) majoration régionale pour consommation_gazole et consommation_supercarburant_e5, en plus de la réfaction
    #NB : quelquels changements dans les indices
    #par rapport aux années suivantes; ces changements s'appliquent aux années précédents :
    #1° Huiles légères, indice 4 bis, hectolitre, taxe intérieure applicable au fioul domestique visé à l'indice 20.
    #parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
    #
    #exempté :
    #parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
    # 
    #remarques peu importantes : 
    #---huiles lubrifiantes et autres, exemption
    #Ex 2715-00, Bitumes fluxés ("cut-backs"), émulsions de bitume de pétrole et similaires : indice 47, exemption.
    #3403-11, Préparations pour le traitement des matières textiles, du cuir, des pelleteries ou d'autres matières, contenant moins de 70 % en poids d'huiles de pétrole ou de minéraux bitumineux : indice 48, exemption.
    #Ex 3403-19, Préparations lubrifiantes contenant moins de 70 % en poids d'huiles de pétrole ou de minéraux bitumineux : indice 49, exemption.
    #3811 21-00, Additifs pour huiles lubrifiantes, contenant des huiles de pétrole ou de minéraux bitumineux : indice 51, exemption.
    #
    #il a pas de tariff explicite après 2008, non plus
    #
    #
    def formula_2007_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            # + etablissement('consommation_supercarburant_e10', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL 
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

            
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            # + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            
            + etablissement('consommation_carbureacteurs_essence_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total


    #2008
    #par rapport aux années suivantes; ces changements s'appliquent aux années précédents :
    #  consommation_supercarburant_e10 exempté 
    def formula_2008_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

            
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            
            + etablissement('consommation_carbureacteurs_essence_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    

    #*** TODO : vérifie quand e10 s'est apparu 2011 pas 2012 ? 
    #2012
    #par rapport à précédement, 
    #la majoration régionale inclus désormais 11 ter, consommation_supercarburant_e10
    #par rapport aux années suivantes; ces changements s'appliquent aux années précédents :
    #ajouté 
    #parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
    #parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
    def formula_2012_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period))
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

            
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            
            + etablissement('consommation_carbureacteurs_essence_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_sous_conditions_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    #2014
    #pas de changement par rapport à 2015
    #2015: 
    #pas de changement par rapport à 2016
    #2016:
    #consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole
    #^exempté en 2016 et celles d'avant 
    def formula_2014_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period))
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

            
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total
    #2017: 
    #parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
    #^est exempté, également pendant les années précédantes 
    #parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
    #^également pour ça 
    #consommation_carburant_constitue_100_estars_methyliques_acides_gras
    #parameters\energies\autres_produits_energetiques\ticpe\gazole\gazole_b_10_hectolitre.yaml
    #^également 
    def formula_2017_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period))
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

            
            + etablissement('consommation_gazole_b_10_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole_b_10_hectolitre
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total        

    #2018: pareil que 2019
    #2019 : par rapport à 2020,
    #parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole_b_10_hectolitre
    #parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
    #parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
    def formula_2018_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period))
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            

            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

            
            + etablissement('consommation_gazole_b_10_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole_b_10_hectolitre
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement('consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total

    #2020 : par rapport à 2021, 
    # carburants_sous_conditions_hectolitre,
    #sous_conditions_100kg_nets (propane)
    #parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
    #
    #parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
    #
    #parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
    #(en dessous est un nouveau catagorie)
    #parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
    #
    #parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
    def formula_2020_01_01(etablissement, period, parameters):
        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period))
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            #additions, en plus de 2021
            + etablissement('consommation_propane_carburants_sous_conditions_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement('consommation_butanes_liquefies_sous_condition_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement('consommation_emulsion_eau_gazoles_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement('consommation_emulsion_eau_gazoles_autres_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre

        ]
        return total
        

    def formula_2021_01_01(etablissement, period, parameters):
        

        total = [
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('consommation_huiles_legeres_preparation_essence_aviation', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_supercarburant_e5', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e5 + etablissement("ticpe_majoration_regionale_supercarburant_95_98", period))
            + etablissement('consommation_super_ars', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_supercarburant_e10', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10 + etablissement("ticpe_majoration_regionale_supercarburant_e10", period))
            + etablissement('consommation_carbureacteurs_essence_carburants_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement('consommation_carbureacteurs_essence_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres_combustible_carburant_ou_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carbureacteurs_petrole_lampant_autres_hL', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes_autres', period) * parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_gazoles_carburants_sous_conditions_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazoles', period) * (parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole + etablissement("ticpe_majoration_regionale_gazole", period))
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_supercarburant_e85', period) * parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).

        ]
        return total
    
    def formula_2022_01_01(etablissement, period, parameters):
        #à noter que l'accise est mise en effet dès cette année. beaucoup des categories sont éliminées 
        #les majorations régionales sont manquants.
        #menutention portuaire existe en tant qu'une catégorie dès 2023

        # if etablissement('departement', period) == '02A' or etablissement('departement', period) == '02B':
        #     beneficie_corse = 1
        # else : 
        #     beneficie_corse = 0
        #Article L312-41, minoration pour l'essence pour la Corse

        #les carburants
        #ça determine quel taux à appliquer aux gazoles 
        if etablissement('gazoles_transport_guide', period) == True : 
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_guide
        elif etablissement('gazoles_engins_travaux_statiques', period) == True:
            taux_gazoles = parameters.energies.autres_produits_energetiques.accise.carburants.gazoles_engins_travaux_statiques 
        elif etablissement('gazoles_transport_collective_personnes', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_collectif_routier_de_personnes
        elif etablissement('gazoles_transport_taxi', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_de_personnes_par_taxi
        elif etablissement('gazoles_transport_routier_marchandises', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_routier_de_marchandises
        elif etablissement('gazoles_manutention_portuaire', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_manutention_portuaire
            #la formule de manutention portuaire existe qu'après 2023
        elif etablissement('autres_produits_travaux_agricoles_et_forestiers', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_travaux_agricoles
        elif etablissement('gazoles_extraction_mineraux_industriels', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_extraction_de_mineraux_industriels
            #dès 2024
        elif etablissement('gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux
        elif etablissement('autres_produits_intervention_vehicules_services_incendie_secours', period) == True:
            taux_gazoles = 0
        else :
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.carburants.gazoles
        
        #essence
        if etablissement('essence_transport_taxi', period) == True :
            taux_essence = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.essences_transport_de_personnes_par_taxi
        if etablissement('autres_produits_intervention_vehicules_services_incendie_secours', period) == True :
            taux_essence = 0
        else :    
            taux_essence = parameters(period).energies.autres_produits_energetiques.accise.carburants.essences

        #gaz de pétrole liquifié
        if etablissement('autres_produits_travaux_agricoles_et_forestiers', period) == True :
            taux_gaz_de_petrole_liquefies_combustible = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gaz_de_petrole_liquefies_combustible_travaux_agricoles
        else :    
            taux_gaz_de_petrole_liquefies_combustible = parameters(period).energies.autres_produits_energetiques.accise.combustibles.gaz_de_petrole_liquefies_combustibles

        #les combustibles
        installation_seqe = etablissement("installation_seqe", period)
        risque_de_fuite_carbone_eta = etablissement('risque_de_fuite_carbone_eta', period)
        intensite_energetique_valeur_production = etablissement('intensite_energetique_valeur_production', period)
        intensite_energetique_valeur_ajoutee = etablissement('intensite_energetique_valeur_ajoutee', period)


        #ça determine quel taux à appliquer aux fiouls lourds 
        if etablissement('autres_produits_travaux_agricoles_et_forestiers', period) == True :
            taux_fiouls_lourds = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.fiouls_lourds_travaux_agricoles
        elif (installation_seqe == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taux_fiouls_lourds = parameters.energies.autres_produits_energetiques.accise.taux_selon_activite.fiouls_lourds_seqe
            #***faut faire un test pour 
        elif (installation_seqe == False and risque_de_fuite_carbone_eta == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == False and risque_de_fuite_carbone_eta == True and  intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taux_fiouls_lourds = parameters.energies.autres_produits_energetiques.accise.taux_selon_activite.fiouls_lourds_concurrence_internationale
        else :    
            taux_fiouls_lourds = parameters(period).energies.autres_produits_energetiques.accise.combustibles.fiouls_lourds

        #pour les fiouls domestiques
        
        if (installation_seqe == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taux_fiouls_domestiques = parameters.energies.autres_produits_energetiques.accise.taux_selon_activite.fiouls_domestiques_seqe
            #***faut faire un test pour 
        elif (installation_seqe == False and risque_de_fuite_carbone_eta == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == False and risque_de_fuite_carbone_eta == True and  intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taux_fiouls_domestiques = parameters.energies.autres_produits_energetiques.accise.taux_selon_activite.fiouls_domestiques_concurrence_internationale
        else :    
            taux_fiouls_domestiques = parameters(period).energies.autres_produits_energetiques.accise.combustibles.fiouls_domestiques

        #pétrole lampant
        if (installation_seqe == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == True and intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taux_petrole_lampant = parameters.energies.autres_produits_energetiques.accise.taux_selon_activite.petroles_lampants_seqe
            #***faut faire un test pour 
        elif (installation_seqe == False and risque_de_fuite_carbone_eta == True and intensite_energetique_valeur_production >= 0.03) or (installation_seqe == False and risque_de_fuite_carbone_eta == True and  intensite_energetique_valeur_ajoutee >= 0.005 ) :
            taux_petrole_lampant = parameters.energies.autres_produits_energetiques.accise.taux_selon_activite.petroles_lampants_concurrence_internationale
        else :    
            taux_petrole_lampant = parameters(period).energies.autres_produits_energetiques.accise.combustibles.petroles_lampants




        #trois cas d'exoneration pour toute la consommation
        if etablissement('autres_produits_navigation_interieure', period) == True:
                total = 0
        elif etablissement('autres_produits_navigation_maritime', period) == True:
                total = 0
        elif etablissement('autres_produits_navigation_aerienne', period) == True:
                total = 0
        elif etablissement('autres_produits_double_usage', period) == True:
                total = 0
        elif etablissement('autre_produits_fabrication_produits_mineraux_non_metalliques', period) == True:
                total = 0
        elif etablissement('autres_produits_secteurs_aeronautique_et_naval', period) == True:
                total = 0
        else :
            total = [
                #ces produits sont de carburants (L312-35)
                
                etablissement('consommation_gazoles_mwh', period) * (taux_gazoles + etablissement('ticpe_majoration_regionale_gazole', period))
                + etablissement('consommation_carbureactuers_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.carburants.carbureacteurs
                + etablissement('consommation_essences_mwh', period) * (taux_essence + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)) #+ beneficie_corse * parameters(period).energies.autres_produits_energetiques.accise.minoration_corse 
                #^*** besoin des taux de majoration régionale pour l'essence 
                + etablissement('consommation_gaz_de_petrole_liquefies_carburant_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.carburants.gaz_de_petrole_liquefies_carburant
                
                #ces produits sont de combustibles (L312-36)
                + etablissement('consommation_fiouls_lourds_mwh', period) * taux_fiouls_lourds
                + etablissement('consommation_fiouls_domestiques_mwh', period) * taux_fiouls_domestiques
                + etablissement('consommation_petroles_lampants_mwh', period) * taux_petrole_lampant
                + etablissement('consommation_gaz_de_petrole_liquefies_combustible_mwh', period) * taux_gaz_de_petrole_liquefies_combustible

                #ces produits sont des produits particuliers (L312-79)
                + etablissement('consommation_ethanol_diesel_ed95_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.ethanol_diesel_ed95
                + etablissement('consommation_gazole_b100_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.gazole_b100
                + etablissement('consommation_essence_aviation_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.essence_aviation
                + etablissement('consommation_essence_sp95_e10_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.essence_sp95_e10
                + etablissement('consommation_superethanol_e85_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.superethanol_e85
                + etablissement('consommation_grisou_et_gaz_assimiles_combustible_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.grisou_et_gaz_assimiles_combustible
                + etablissement('consommation_biogaz_combustible_non_injecte_dans_le_reseau_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.biogaz_combustible_non_injecte_dans_le_reseau
            ]
        return total

    
    
    def formula_2024_01_01(etablissement, period, parameters):
        #par rapport à précédement, suprimmé consommation_essence_aviation_mwh et quelques tariffs visé à le seqe et concurrence internationale

        # if etablissement('departement', period) == '02A' or etablissement('departement', period) == '02B':
        #     beneficie_corse = 1
        # else : 
        #     beneficie_corse = 0
        #Article L312-41, minoration pour l'essence pour la Corse


        #les carburants
        #ça determine quel taux à appliquer aux gazoles 
        if etablissement('gazoles_transport_guide', period) == True : 
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_guide
        elif etablissement('gazoles_engins_travaux_statiques', period) == True:
            taux_gazoles = parameters.energies.autres_produits_energetiques.accise.carburants.gazoles_engins_travaux_statiques 
        elif etablissement('gazoles_transport_collective_personnes', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_collectif_routier_de_personnes
        elif etablissement('gazoles_transport_taxi', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_de_personnes_par_taxi
        elif etablissement('gazoles_transport_routier_marchandises', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_transport_routier_de_marchandises
        elif etablissement('gazoles_manutention_portuaire', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_manutention_portuaire
            #la formule de manutention portuaire existe qu'après 2023
        elif etablissement('autres_produits_travaux_agricoles_et_forestiers', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_travaux_agricoles
        elif etablissement('gazoles_extraction_mineraux_industriels', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_extraction_de_mineraux_industriels
            #dès 2024
        elif etablissement('gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux', period) == True:
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux
        elif etablissement('autres_produits_intervention_vehicules_services_incendie_secours', period) == True:
            taux_gazoles = 0
        else :
            taux_gazoles = parameters(period).energies.autres_produits_energetiques.accise.carburants.gazoles
        
        #essence
        if etablissement('essence_transport_taxi', period) == True :
            taux_essence = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.essences_transport_de_personnes_par_taxi
        if etablissement('autres_produits_intervention_vehicules_services_incendie_secours', period) == True :
            taux_essence = 0
        else :    
            taux_essence = parameters(period).energies.autres_produits_energetiques.accise.carburants.essences

        #gaz de pétrole liquifié
        if etablissement('autres_produits_travaux_agricoles_et_forestiers', period) == True :
            taux_gaz_de_petrole_liquefies_combustible = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.gaz_de_petrole_liquefies_combustible_travaux_agricoles
        else :    
            taux_gaz_de_petrole_liquefies_combustible = parameters(period).energies.autres_produits_energetiques.accise.combustibles.gaz_de_petrole_liquefies_combustibles

        #les combustibles


        #ça determine quel taux à appliquer aux fiouls lourds 
        if etablissement('autres_produits_travaux_agricoles_et_forestiers', period) == True :
            taux_fiouls_lourds = parameters(period).energies.autres_produits_energetiques.accise.taux_selon_activite.fiouls_lourds_travaux_agricoles
        else :    
            taux_fiouls_lourds = parameters(period).energies.autres_produits_energetiques.accise.combustibles.fiouls_lourds

        #pour les fiouls domestiques
        
        taux_fiouls_domestiques = parameters(period).energies.autres_produits_energetiques.accise.combustibles.fiouls_domestiques

        #pétrole lampant
        taux_petrole_lampant = parameters(period).energies.autres_produits_energetiques.accise.combustibles.petroles_lampants




        #trois cas d'exoneration pour toute la consommation
        if etablissement('autres_produits_navigation_interieure', period) == True:
                total = 0
        elif etablissement('autres_produits_navigation_maritime', period) == True:
                total = 0
        elif etablissement('autres_produits_navigation_aerienne', period) == True:
                total = 0
        elif etablissement('autres_produits_double_usage', period) == True:
                total = 0
        elif etablissement('autre_produits_fabrication_produits_mineraux_non_metalliques', period) == True:
                total = 0
        elif etablissement('autres_produits_secteurs_aeronautique_et_naval', period) == True:
                total = 0
        else :
            total = [
                #ces produits sont de carburants (L312-35)
                
                etablissement('consommation_gazoles_mwh', period) * (taux_gazoles + etablissement('ticpe_majoration_regionale_gazole', period))
                + etablissement('consommation_carbureactuers_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.carburants.carbureacteurs
                + etablissement('consommation_essences_mwh', period) * (taux_essence + etablissement("ticpe_majoration_regionale_supercarburant_e10", period) ) #+ beneficie_corse * parameters(period).energies.autres_produits_energetiques.accise.minoration_corse
                #^*** besoin des taux de majoration régionale pour l'essence 
                + etablissement('consommation_gaz_de_petrole_liquefies_carburant_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.carburants.gaz_de_petrole_liquefies_carburant
                
                #ces produits sont de combustibles (L312-36)
                + etablissement('consommation_fiouls_lourds_mwh', period) * taux_fiouls_lourds
                + etablissement('consommation_fiouls_domestiques_mwh', period) * taux_fiouls_domestiques
                + etablissement('consommation_petroles_lampants_mwh', period) * taux_petrole_lampant
                + etablissement('consommation_gaz_de_petrole_liquefies_combustible_mwh', period) * taux_gaz_de_petrole_liquefies_combustible

                #ces produits sont des produits particuliers (L312-79)
                + etablissement('consommation_ethanol_diesel_ed95_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.ethanol_diesel_ed95
                + etablissement('consommation_gazole_b100_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.gazole_b100
                + etablissement('consommation_essence_sp95_e10_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.essence_sp95_e10
                + etablissement('consommation_superethanol_e85_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.superethanol_e85
                + etablissement('consommation_grisou_et_gaz_assimiles_combustible_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.grisou_et_gaz_assimiles_combustible
                + etablissement('consommation_biogaz_combustible_non_injecte_dans_le_reseau_mwh', period) * parameters(period).energies.autres_produits_energetiques.accise.tariffs_particuliers.biogaz_combustible_non_injecte_dans_le_reseau
            ]
        return total
    




#2007 e5, gazole

#2012 e10

class ticpe_majoration_regionale_gazole(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"  #
    def formula_2007_01_01(etablissement, period, parameters):
        
        departement = etablissement('departement', period)


        if departement in ['67', '68']:
            #region = 'Alsace'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.alsace
        
        elif departement in ['24', '33', '40', '47', '64']:
            #region = 'Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.aquitaine

        elif departement in ['3', '15', '43', '63']:
            #region = 'Auvergne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.auvergne

        elif departement in ['14', '50', '61']:
            #region = 'Basse-Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.basse_normandie

        elif departement in ['21', '58', '71', '89']:
            #region = 'Bourgogne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.bourgogne

        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.bretagne

        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.centre

        elif departement in ['8', '10', '51', '52']:
            #region = 'Champagne-Ardenne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.champagne_ardennes

        elif departement in ['02A', '02B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.corse

        elif departement in ['25', '39', '70', '90']:
            #region = 'Franche-Comté'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.franche_comte

        elif departement in ['27', '76']:
            #region = 'Haute-Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.haute_normandie

        elif departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Île-de-France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.ils_france

        elif departement in ['11', '30', '34', '48', '66']:
            #region = 'Languedoc-Roussillon'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.languedoc_roussillon

        elif departement in ['19', '23', '87']:
            #region = 'Limousin'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.limousin

        elif departement in ['54', '55', '57', '88']:
            #region = 'Lorraine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.lorraine

        elif departement in ['9', '12', '31', '32', '46', '65', '81', '82']:
            #region = 'Midi-Pyrénées'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.midi_pyrenees

        elif departement in ['59', '62']:
            #region = 'Nord-Pas-de-Calais'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.nord_pas_calais

        elif departement in ['4', '5', '6', '13', '83', '84']:
            #region = 'PACA'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.paca

        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays de la Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.pays_loire

        elif departement in ['2', '60', '80']:
            #region = 'Picardie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.picardie

        elif departement in ['16', '17', '79', '86']:
            #region = 'Poitou-Charentes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.poitou_charentes

        elif departement in ['1', '7', '26', '38', '42', '69', '73', '74']:
            #region = 'Rhône-Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.rhone_alpes
        else:
            #region = 'Inconnu'
            majoration = 0
      
        return majoration 
    def formula_2017_01_01(etablissement, period, parameters):
        #suivant la reforme des régions en 2014, on les a changées
        departement = etablissement('departement', period)


        if departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Ils De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.ils_france
        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre Val De Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.centre_val_loire
        elif departement in ['21', '25', '39', '58', '70', '71', '89', '90']:
            #region = 'Bourgogne Franche Comte'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.bourgogne_franche_comte
        elif departement in ['14', '27', '50', '61', '76']:
            #region = 'Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.normandie
        elif departement in ['02', '59', '60', '62', '80']:
            #region = 'Hauts De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.hauts_france
        elif departement in ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88']:
            #region = 'Grand Est'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.grand_est
        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays De La Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.pays_la_loire
        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.bretagne
        elif departement in ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']:
            #region = 'Nouvelle Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.nouvelle_aquitaine
        elif departement in ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82']:
            #region = 'Occitanie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.occitanie
        elif departement in ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74']:
            #region = 'Auvergne Rhone Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.auvergne_rhone_alpes
        elif departement in ['04', '05', '06', '13', '83', '84']:
            #region = 'Paca'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.paca
        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017.corse
        else:
            #region = 'Inconnu'
            majoration = 0

        return majoration 
    def formula_2022_01_01(etablissement, period, parameters):
        #suivant la reforme des régions en 2014, on les a changées
        #la raison pour avoir une autre ensemble des variables c'est parce que l'unité change à MWh
        departement = etablissement('departement', period)


        if departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Ils De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.ils_france
        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre Val De Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.centre_val_loire
        elif departement in ['21', '25', '39', '58', '70', '71', '89', '90']:
            #region = 'Bourgogne Franche Comte'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.bourgogne_franche_comte
        elif departement in ['14', '27', '50', '61', '76']:
            #region = 'Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.normandie
        elif departement in ['02', '59', '60', '62', '80']:
            #region = 'Hauts De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.hauts_france
        elif departement in ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88']:
            #region = 'Grand Est'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.grand_est
        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays De La Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.pays_la_loire
        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.bretagne
        elif departement in ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']:
            #region = 'Nouvelle Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.nouvelle_aquitaine
        elif departement in ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82']:
            #region = 'Occitanie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.occitanie
        elif departement in ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74']:
            #region = 'Auvergne Rhone Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.auvergne_rhone_alpes
        elif departement in ['04', '05', '06', '13', '83', '84']:
            #region = 'Paca'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.paca
        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022.corse
        else:
            #region = 'Inconnu'
            majoration = 0

        return majoration

    


class ticpe_majoration_regionale_supercarburant_e10(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"  #
    def formula_2007_01_01(etablissement, period, parameters):
        
        departement = etablissement('departement', period)


        if departement in ['67', '68']:
            #region = 'Alsace'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.alsace
        
        elif departement in ['24', '33', '40', '47', '64']:
            #region = 'Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.aquitaine

        elif departement in ['3', '15', '43', '63']:
            #region = 'Auvergne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.auvergne

        elif departement in ['14', '50', '61']:
            #region = 'Basse-Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.basse_normandie

        elif departement in ['21', '58', '71', '89']:
            #region = 'Bourgogne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.bourgogne

        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.bretagne

        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.centre

        elif departement in ['8', '10', '51', '52']:
            #region = 'Champagne-Ardenne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.champagne_ardennes

        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.corse

        elif departement in ['25', '39', '70', '90']:
            #region = 'Franche-Comté'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.franche_comte

        elif departement in ['27', '76']:
            #region = 'Haute-Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.haute_normandie

        elif departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Île-de-France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.ils_france

        elif departement in ['11', '30', '34', '48', '66']:
            #region = 'Languedoc-Roussillon'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.languedoc_roussillon

        elif departement in ['19', '23', '87']:
            #region = 'Limousin'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.limousin

        elif departement in ['54', '55', '57', '88']:
            #region = 'Lorraine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.lorraine

        elif departement in ['9', '12', '31', '32', '46', '65', '81', '82']:
            #region = 'Midi-Pyrénées'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.midi_pyrenees

        elif departement in ['59', '62']:
            #region = 'Nord-Pas-de-Calais'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.nord_pas_calais

        elif departement in ['4', '5', '6', '13', '83', '84']:
            #region = 'PACA'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.paca

        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays de la Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.pays_loire

        elif departement in ['2', '60', '80']:
            #region = 'Picardie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.picardie

        elif departement in ['16', '17', '79', '86']:
            #region = 'Poitou-Charentes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.poitou_charentes

        elif departement in ['1', '7', '26', '38', '42', '69', '73', '74']:
            #region = 'Rhône-Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.rhone_alpes
        else:
            #region = 'Inconnu'
            majoration = 0
      
        return majoration 
    def formula_2017_01_01(etablissement, period, parameters):
        #suivant la reforme des régions en 2014, on les a changées
        departement = etablissement('departement', period)


        if departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Ils De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.ils_france
        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre Val De Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.centre_val_loire
        elif departement in ['21', '25', '39', '58', '70', '71', '89', '90']:
            #region = 'Bourgogne Franche Comte'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.bourgogne_franche_comte
        elif departement in ['14', '27', '50', '61', '76']:
            #region = 'Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.normandie
        elif departement in ['02', '59', '60', '62', '80']:
            #region = 'Hauts De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.hauts_france
        elif departement in ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88']:
            #region = 'Grand Est'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.grand_est
        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays De La Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.pays_la_loire
        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.bretagne
        elif departement in ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']:
            #region = 'Nouvelle Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.nouvelle_aquitaine
        elif departement in ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82']:
            #region = 'Occitanie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.occitanie
        elif departement in ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74']:
            #region = 'Auvergne Rhone Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.auvergne_rhone_alpes
        elif departement in ['04', '05', '06', '13', '83', '84']:
            #region = 'Paca'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.paca
        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017.corse
        else:
            #region = 'Inconnu'
            majoration = 0

        return majoration
    def formula_2022_01_01(etablissement, period, parameters):
        #la raison pour avoir une autre ensemble des variables c'est parce que l'unité change à MWh
        #suivant la reforme des régions en 2014, on les a changées
        departement = etablissement('departement', period)


        if departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Ils De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.ils_france
        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre Val De Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.centre_val_loire
        elif departement in ['21', '25', '39', '58', '70', '71', '89', '90']:
            #region = 'Bourgogne Franche Comte'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.bourgogne_franche_comte
        elif departement in ['14', '27', '50', '61', '76']:
            #region = 'Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.normandie
        elif departement in ['02', '59', '60', '62', '80']:
            #region = 'Hauts De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.hauts_france
        elif departement in ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88']:
            #region = 'Grand Est'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.grand_est
        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays De La Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.pays_la_loire
        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.bretagne
        elif departement in ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']:
            #region = 'Nouvelle Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.nouvelle_aquitaine
        elif departement in ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82']:
            #region = 'Occitanie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.occitanie
        elif departement in ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74']:
            #region = 'Auvergne Rhone Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.auvergne_rhone_alpes
        elif departement in ['04', '05', '06', '13', '83', '84']:
            #region = 'Paca'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.paca
        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022.corse
        else:
            #region = 'Inconnu'
            majoration = 0

        return majoration

class ticpe_majoration_regionale_supercarburant_95_98(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"  #
    def formula_2007_01_01(etablissement, period, parameters):
        
        departement = etablissement('departement', period)


        if departement in ['67', '68']:
            #region = 'Alsace'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.alsace
        
        elif departement in ['24', '33', '40', '47', '64']:
            #region = 'Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.aquitaine

        elif departement in ['3', '15', '43', '63']:
            #region = 'Auvergne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.auvergne

        elif departement in ['14', '50', '61']:
            #region = 'Basse-Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.basse_normandie

        elif departement in ['21', '58', '71', '89']:
            #region = 'Bourgogne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.bourgogne

        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.bretagne

        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.centre

        elif departement in ['8', '10', '51', '52']:
            #region = 'Champagne-Ardenne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.champagne_ardennes

        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.corse

        elif departement in ['25', '39', '70', '90']:
            #region = 'Franche-Comté'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.franche_comte

        elif departement in ['27', '76']:
            #region = 'Haute-Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.haute_normandie

        elif departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Île-de-France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.ils_france

        elif departement in ['11', '30', '34', '48', '66']:
            #region = 'Languedoc-Roussillon'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.languedoc_roussillon

        elif departement in ['19', '23', '87']:
            #region = 'Limousin'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.limousin

        elif departement in ['54', '55', '57', '88']:
            #region = 'Lorraine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.lorraine

        elif departement in ['9', '12', '31', '32', '46', '65', '81', '82']:
            #region = 'Midi-Pyrénées'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.midi_pyrenees

        elif departement in ['59', '62']:
            #region = 'Nord-Pas-de-Calais'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.nord_pas_calais

        elif departement in ['4', '5', '6', '13', '83', '84']:
            #region = 'PACA'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.paca

        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays de la Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.pays_loire

        elif departement in ['2', '60', '80']:
            #region = 'Picardie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.picardie

        elif departement in ['16', '17', '79', '86']:
            #region = 'Poitou-Charentes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.poitou_charentes

        elif departement in ['1', '7', '26', '38', '42', '69', '73', '74']:
            #region = 'Rhône-Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.rhone_alpes
        else:
            #region = 'Inconnu'
            majoration = 0
      
        return majoration 
    def formula_2017_01_01(etablissement, period, parameters):
        #suivant la reforme des régions en 2014, on les a changées
        departement = etablissement('departement', period)


        if departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Ils De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.ils_france
        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre Val De Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.centre_val_loire
        elif departement in ['21', '25', '39', '58', '70', '71', '89', '90']:
            #region = 'Bourgogne Franche Comte'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.bourgogne_franche_comte
        elif departement in ['14', '27', '50', '61', '76']:
            #region = 'Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.normandie
        elif departement in ['02', '59', '60', '62', '80']:
            #region = 'Hauts De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.hauts_france
        elif departement in ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88']:
            #region = 'Grand Est'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.grand_est
        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays De La Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.pays_la_loire
        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.bretagne
        elif departement in ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']:
            #region = 'Nouvelle Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.nouvelle_aquitaine
        elif departement in ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82']:
            #region = 'Occitanie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.occitanie
        elif departement in ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74']:
            #region = 'Auvergne Rhone Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.auvergne_rhone_alpes
        elif departement in ['04', '05', '06', '13', '83', '84']:
            #region = 'Paca'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.paca
        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017.corse
        else:
            #region = 'Inconnu'
            majoration = 0

        return majoration
    def formula_2017_01_01(etablissement, period, parameters):
        #la raison pour avoir une autre ensemble des variables c'est parce que l'unité change à MWh
        #suivant la reforme des régions en 2014, on les a changées
        departement = etablissement('departement', period)


        if departement in ['75', '77', '78', '91', '92', '93', '94', '95']:
            #region = 'Ils De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.ils_france
        elif departement in ['18', '28', '36', '37', '41', '45']:
            #region = 'Centre Val De Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.centre_val_loire
        elif departement in ['21', '25', '39', '58', '70', '71', '89', '90']:
            #region = 'Bourgogne Franche Comte'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.bourgogne_franche_comte
        elif departement in ['14', '27', '50', '61', '76']:
            #region = 'Normandie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.normandie
        elif departement in ['02', '59', '60', '62', '80']:
            #region = 'Hauts De France'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.hauts_france
        elif departement in ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88']:
            #region = 'Grand Est'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.grand_est
        elif departement in ['44', '49', '53', '72', '85']:
            #region = 'Pays De La Loire'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.pays_la_loire
        elif departement in ['22', '29', '35', '56']:
            #region = 'Bretagne'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.bretagne
        elif departement in ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87']:
            #region = 'Nouvelle Aquitaine'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.nouvelle_aquitaine
        elif departement in ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82']:
            #region = 'Occitanie'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.occitanie
        elif departement in ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74']:
            #region = 'Auvergne Rhone Alpes'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.auvergne_rhone_alpes
        elif departement in ['04', '05', '06', '13', '83', '84']:
            #region = 'Paca'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.paca
        elif departement in ['2A', '2B']:
            #region = 'Corse'
            majoration = parameters(period).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022.corse
        else:
            #region = 'Inconnu'
            majoration = 0

        return majoration