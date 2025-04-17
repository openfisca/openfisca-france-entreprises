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

    #2002
    #beaucoup de changements à voir 

    #2003 
    #pas de changements

    #2004
    #les majorations regionales n'existaient pas, tandis que les majorations par l'état 

    #2006
    #consommation_super_e85 
    #^exempté

    #2007
    #NB : quelquels changements dans les indices
    #Grandes changements 
    #1° Huiles légères, indice 4 bis, hectolitre, taxe intérieure applicable au fioul domestique visé à l'indice 20.
    #parameters\energies\autres_produits_energetiques\ticpe\carburateurs\essence\autres_hL.yaml
    #
    #parameters\energies\autres_produits_energetiques\ticpe\gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires.yaml
    #^exempté 
    #remarque pas importante : 
    #---huiles lubrifiantes et autres, excemption
    #Ex 2715-00, Bitumes fluxés ("cut-backs"), émulsions de bitume de pétrole et similaires : indice 47, exemption.
    #3403-11, Préparations pour le traitement des matières textiles, du cuir, des pelleteries ou d'autres matières, contenant moins de 70 % en poids d'huiles de pétrole ou de minéraux bitumineux : indice 48, exemption.
    #Ex 3403-19, Préparations lubrifiantes contenant moins de 70 % en poids d'huiles de pétrole ou de minéraux bitumineux : indice 49, exemption.
    #3811 21-00, Additifs pour huiles lubrifiantes, contenant des huiles de pétrole ou de minéraux bitumineux : indice 51, exemption.
    #
    #il a pas de tariff explicite après 2008 non plus
    #
    #



    #2008
    #consommation_super_e10 exempté 


    #2012
    #ajoute
    #parameters\energies\autres_produits_energetiques\ticpe\carburateurs\essence\sous_conditions_hL.yaml
    #parameters\energies\autres_produits_energetiques\ticpe\carburateurs\petrole_lampant\sous_conditions_hL.yaml

    #2014
    #pas de changement par rapport à 2015

    #2015: 
    #pas de changement par rapport à 2016


    #2016:
    #consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole
    #^exempté en 2016 et les années avant 

    #2017: 
    #parameters\energies\autres_produits_energetiques\ticpe\propane_carburants\usages_autres_que_comme_carburant_100kg_nets.yaml
    #^est exempté, également pendant les années précédantes 
    #parameters\energies\autres_produits_energetiques\ticpe\butanes_liquefies\usages_autres_que_comme_carburant_100kg_nets.yaml
    #^également pour ça 
    #consommation_carburant_constitue_100_estars_methyliques_acides_gras
    #^également 

    #2018: pareil que 2019


    #2019 : par rapport à 2020,
    #parameters\energies\autres_produits_energetiques\ticpe\gazole\gazol_b_10_hectolitre.yaml
    #parameters\energies\autres_produits_energetiques\ticpe\gaz_naturel_etat_gazeux_utilises_comme_carburants.yaml
    #parameters\energies\autres_produits_energetiques\ticpe\gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires.yaml
    #
    #


    #2020 : par rapport à 2021, 
    # carburants_sous_conditions_hectolitre,
    # parameters\energies\autres_produits_energetiques\ticpe\gazole\carburants_sous_conditions_hectolitre.yaml
    #sous_conditions_100kg_nets (propane)
    #parameters\energies\autres_produits_energetiques\ticpe\propane_carburants\sous_conditions_100kg_nets.yaml
    #
    #parameters\energies\autres_produits_energetiques\ticpe\butanes_liquefies\sous_condition_100kg_nets.yaml
    #
    #parameters\energies\autres_produits_energetiques\ticpe\autres_gaz_petrole_liquefies_utilises_comme_carburants\sous_conditions_100kg.yaml
    #(en dessous est un nouveau catagorie)
    #parameters\energies\autres_produits_energetiques\ticpe\emulsion_eau_gazole\sous_conditions_hectolitre.yaml
    #
    #parameters\energies\autres_produits_energetiques\ticpe\emulsion_eau_gazole\autres_hectolitre.yaml

    def formula_2021_01_01(etablissement, period, parameters):
        
        total = {
            #chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement('consommation_goudrons_utilises_comme_combustibles', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement('consommation_white_spirit_utilise_comme_combustible', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement('consommation_essences_speciales_utilisees_comme_carburants_combustibles', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement('huiles_legeres_preparation_essence_aviation', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement('consommation_super_e5', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.super.super_e5
            + etablissement('consommation_super_plombe', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement('consommation_super_e10', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.super.super_e10
            + etablissement('consommation_carburateurs_essence_carburants_avion_hL', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.carburateurs.essence.carburants_avion_hL
            + etablissement('consommation_carburateurs_essence_autres_hL', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.carburateurs.essence.autres_hL
            + etablissement('consommation_huiles_legeres', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement('consommation_petrole_lampant_utilise_comme_combustible_hectolitre', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement('consommation_petrole_lampant_autre_hectolitre', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement('consommation_carburateurs_petrole_lampant_carburant_moteurs_avion_hL', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.carburateurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement('consommation_carburateurs_petrole_lampant_autres_hL', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.carburateurs.petrole_lampant.autres_hL
            + etablissement('consommation_huiles_moyennes', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement('consommation_galzole_fioul_domestique_hectolitre', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement('consommation_gazole', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.gazole.gazole
            + etablissement('consommation_fioul_lourd_100kg_net', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement('consommation_propane_carburants_autres_100kg_nets', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_butanes_liquefies_autres_100kg_nets', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement('consommation_autres_gaz_petrole_liquefies_utilises_comme_carburants_autres_100kg', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement('consommation_super_e85', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) * parameters(period).parameters.energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            
            
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).

        }
        

        

        return total