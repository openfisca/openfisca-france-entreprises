from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable




class consommation_goudrons_utilises_comme_combustibles(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carburant_constitue_100_estars_methyliques_acides_gras(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole(Variable): 
    #s'appelle éthanol-diesel ED95 dans l'accisse
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_essence_normale(Variable): 
    #dans l'accise, s'appelle essence SP95-E10
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_essences_speciales_utilisees_comme_carburants_combustibles(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_white_spirit_utilise_comme_combustible(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_supercarburant_e5(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = '''-----supercarburant d'une teneur en plomb n'excédant pas 0,005 g/ litre, autre que le supercarburant correspondant à l'indice d'identification n° 11 bis, contenant jusqu'à 5 % volume/ volume d'éthanol, 22 % volume/ volume d'éthers contenant 5 atomes de carbone ou plus, par molécule et d'une teneur en oxygène maximale de 2,7 % en masse d'oxygène ;	'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_supercarburant_e10(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = '''-----supercarburant d'une teneur en plomb n'excédant pas 0,005 g/ litre, autre que les supercarburants correspondant aux indices d'identification 11 et 11 bis, et contenant jusqu'à 10 % volume/ volume d'éthanol, 22 % volume/ volume d'éthers contenant 5 atomes de carbone, ou plus, par molécule et d'une teneur en oxygène maximale de 3,7 % en masse/ masse d'oxygène ;'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_supercarburant_e85(Variable): 
    #dans l'accise, s'appelle supercarburant E85
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_super_ars(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = "-----supercarburant d'une teneur en plomb n'excédant pas 0,005 g/litre, contenant un additif spécifique améliorant les caractéristiques antirécession de soupape (ARS), à base de potassium, ou tout autre additif reconnu de qualité équivalente dans un autre Etat membre de la Communauté européenne ou dans un autre Etat membre de l'Espace économique européen."
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_propane_carburants_autres_100kg_nets(Variable): 
    value_type = float
    unit = '100kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_propane_carburants_sous_conditions_100kg_nets(Variable): 
    value_type = float
    unit = '100kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets(Variable): 
    value_type = float
    unit = '100kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR


class consommation_petrole_lampant_autre_hectolitre(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_petrole_lampant_utilise_comme_combustible_hectolitre(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_huiles_legeres_preparation_essence_aviation(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_huiles_legeres_combustible_carburant_ou_autres(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR


class consommation_huiles_moyennes_autres(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_gazoles_carburants_sous_conditions_hectolitre(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_galzole_fioul_domestique_hectolitre(Variable): 
    #dans l'accise, s'appelle fioul domestique
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_gazole_b_10_hectolitre(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_gazoles(Variable): 
    #dans l'accise, s'appelle gazole B100
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = '''indice 22; ----autres, à l'exception du gazole coloré et tracé en apllication du a du 1 de l'article 265 B ;'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_fioul_lourd_100kg_net(Variable): 
    #dans l'accise, s'appelle fioul lourd
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_fioul_lourd_bts_100kg(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_fioul_lourd_hts_100kg(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_point_eclair_inferieur_120deg_c_hectolitre(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_emulsion_eau_gazoles_autres_hectolitre(Variable): 
    #dans l'accise, s'appelle grisou et gaz assimilés combustible
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_emulsion_eau_gazoles_sous_conditions_hectolitre(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carbureacteurs_essence_autres_hL(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR


class consommation_carbureacteurs_essence_carburants_avion_hL(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carbureacteurs_essence_sous_conditions_hL(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carbureacteurs_petrole_lampant_autres_hL(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_carbureacteurs_petrole_lampant_sous_conditions_hL(Variable): 
    value_type = float
    unit = 'Hectolitre'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_butanes_liquefies_autres_100kg_nets(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_butanes_liquefies_sous_condition_100kg_nets(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg(Variable): 
    #gaz de pétrole liquéfié combustible
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg(Variable): 
    value_type = float
    unit = '100 kg nets'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

# pour en cas où 
# class consommation_(Variable): 
#     value_type = float
#     unit = ''
#     entity = Etablissement
#     label = ''
#     reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
#     definition_period = YEAR

class consommation_autres_produits_energetique_ticc(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''Les produits energetique dans l'article 265 soumis à l'article 265 quinques B.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR
    def formula_2007_01_01(etablissement, period, parameters):
        totale =  etablissement('consommation_huiles_lubrifiantes_et_autres', period) + etablissement('consommation_vaseline', period) + etablissement('consommation_paraffine_moins_75_pourcent_huile', period) + etablissement('consommation_paraffine_cires_de_petrole_residus_paraffineux', period) + etablissement('consommation_bitumes_de_petrole', period) + etablissement('consommation_autres_residus_huiles_petrole_ou_mineraux_bitumineux', period) + etablissement('consommation_melanges_bitumeux', period) + etablissement('consommation_preparations_traitement_matiere_textiles', period) + etablissement('consommation_preparations_lubrifiantes', period) + etablissement('consommation_additifs_huiles_lubrifiantes', period)

        return totale
    
    def formula_2012_01_01(etablissement, period, parameters):
        #par rapport à précédement, ajouté consommation_melanges_hydrocarbures_aromatiques
        totale = etablissement('consommation_melanges_hydrocarbures_aromatiques', period) + etablissement('consommation_huiles_lubrifiantes_et_autres', period) + etablissement('consommation_vaseline', period) + etablissement('consommation_paraffine_moins_75_pourcent_huile', period) + etablissement('consommation_paraffine_cires_de_petrole_residus_paraffineux', period) + etablissement('consommation_bitumes_de_petrole', period) + etablissement('consommation_autres_residus_huiles_petrole_ou_mineraux_bitumineux', period) + etablissement('consommation_melanges_bitumeux', period) + etablissement('consommation_preparations_traitement_matiere_textiles', period) + etablissement('consommation_preparations_lubrifiantes', period) + etablissement('consommation_additifs_huiles_lubrifiantes', period)
        etablissement('', period)

        return totale

class consommation_autres_produits_energetique_ticgn(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''Les produits energetique dans l'article 265 soumis à l'article 265 quinques.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR
    def formula_2007_01_01(etablissement, period, parameters):
        totale = etablissement('consommation_ethylene_propylene_butylene_butadiene', period) 

        return totale

class consommation_melanges_hydrocarbures_aromatiques(Variable): 
    #dans l'accise, s'appelle biogaz combustible non injecté dans le réseau
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''Ex 2707-50 Mélanges à forte teneur en hydrocarbures aromatiques distillant 65 % ou plus de leur volume (y compris les pertes) à 250° C d'après la méthode ASTM D 86, destinés à être utilisés comme carburants ou combustibles.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR
    #avant 2012 : Taxe intérieure applicable aux huiles légères ou moyennes du 2710, suivant les caractéristiques du produit.

class consommation_huiles_lubrifiantes_et_autres(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '2710---huiles lubrifiantes et autres.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_ethylene_propylene_butylene_butadiene(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '2711-14 Éthylène, propylène, butylène et butadiène.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_vaseline(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '2712-10 Vaseline.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_paraffine_moins_75_pourcent_huile(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''2712-20  Paraffine contenant en poids moins de 0,75 % d'huile.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_paraffine_cires_de_petrole_residus_paraffineux(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = 'Ex 2712-90 Paraffine (autre que celle mentionnée au 2712-20), cires de pétrole et résidus paraffineux, même colorés.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_bitumes_de_petrole(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '2713-20 Bitumes de pétrole.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_autres_residus_huiles_petrole_ou_mineraux_bitumineux(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '2713-90 Autres résidus des huiles de pétrole ou de minéraux bitumineux.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_melanges_bitumeux(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''2715-00 Mélanges bitumeux à base d'asphalte ou de bitume naturel, de bitume de pétrole, de goudrons minéraux ou de brai de goudron minéral.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_preparations_traitement_matiere_textiles(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''3403-11 Préparations pour le traitement des matières textiles, du cuir, des pelleteries ou d'autres matières, contenant moins de 70 % en poids d'huiles de pétrole ou de minéraux bitumeux.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_preparations_lubrifiantes(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '''Ex 3403-19 Préparations lubrifiantes contenant moins de 70 % en poids d'huiles de pétrole ou de minéraux bitumeux.'''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR

class consommation_additifs_huiles_lubrifiantes(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = '3811-21 Additifs pour huiles lubrifiantes contenant des huiles de pétrole ou de minéraux bitumeux.'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
    definition_period = YEAR


##########################
#les catégories en dessous sont de l'accise
##########################

# class consommation_(Variable): 
#     value_type = float
#     unit = ''
#     entity = Etablissement
#     label = ''
#     reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16'
#     definition_period = YEAR


class consommation_gazoles_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046196825'
    definition_period = YEAR

class consommation_carbureactuers_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046196825'
    definition_period = YEAR

class consommation_essences_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046196825'
    definition_period = YEAR

class consommation_gaz_de_petrole_liquefies_carburant_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046196825'
    definition_period = YEAR

class consommation_fiouls_lourds_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603825'
    definition_period = YEAR

class consommation_fiouls_domestiques_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603825'
    definition_period = YEAR

class consommation_petroles_lampants_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603825'
    definition_period = YEAR

class consommation_gaz_de_petrole_liquefies_combustible_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603825'
    definition_period = YEAR

class consommation_ethanol_diesel_ed95_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class consommation_gazole_b100_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class consommation_essence_aviation_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class consommation_essence_sp95_e10_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class consommation_superethanol_e85_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class consommation_grisou_et_gaz_assimiles_combustible_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class consommation_biogaz_combustible_non_injecte_dans_le_reseau_mwh(Variable): 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051242692'
    definition_period = YEAR

class gazoles_engins_travaux_statiques(Variable): 
    value_type = float
    unit = ''
    entity = Etablissement
    label = ''
    reference = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=Toutefois%2C%20le%20tarif,la%20propulsion%20d%27engins.'
    definition_period = YEAR



# class consommation_gazoles_transport_guide(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie du transport guidé de gazolesoles sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216676"
    

class gazoles_transport_guide(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport guidé de gazolesoles sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216676"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._49_10Z, type_eta._49_20Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant
#_49_10Z, _49_20Z

# class consommation_gazoles_transport_collective_personnes(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class gazoles_transport_collective_personnes(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._49_39A:
            determinant = True
        return determinant

# class consommation_gazoles_transport_taxi(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class gazoles_transport_taxi(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._49_32Z:
            determinant = True
        return determinant


# class consommation_gazoles_transport_routier_marchandises(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie du transport routier de marchandises sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class gazoles_transport_routier_marchandises(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport routier de marchandises sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._49_41A or apet == type_eta._49_41B:
            determinant = True
        return determinant

# class consommation_gazoles_navigation_interieure(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie de la navigation intérieure sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class autres_produits_navigation_interieure(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la navigation intérieure sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._50_30Z or apet == type_eta._50_40Z:
            determinant = True
        return determinant


# class consommation_gazoles_navigation_maritime(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie de la navigation intérieure sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class autres_produits_navigation_maritime(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la navigation intérieure sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._50_10Z or apet == type_eta._50_20Z:
            determinant = True
        return determinant


# class consommation_gazoles_manutention_portuaire(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie de la manutention portuaire de gazoles sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    


class gazoles_manutention_portuaire(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la manutention portuaire de gazoles sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._52_24A:
            determinant = True
        return determinant


# class consommation_gazoles_navigation_aerienne(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie de la navigation aérienne de gazoles sous L312-48"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class autres_produits_navigation_aerienne(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la navigation aérienne de gazoles sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._51_10Z or apet == type_eta._51_21Z:
            determinant = True
        return determinant


# class consommation_gazoles_extraction_mineraux_industriels(Variable):	
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "la catagorie de l'extraction de mineraux industriels sous L312-64/70-1"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875772"
    

class gazoles_extraction_mineraux_industriels(Variable):	
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de l'extraction de mineraux industriels sous L312-64/70-1"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875772"
    def formula_2024_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._08_11Z or apet == type_eta._23_52Z or apet == type_eta._08_12Z:
            determinant = True
        return determinant
    

class essence_transport_taxi(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._49_32Z:
            determinant = True
        return determinant


class autres_produits_travaux_agricoles_et_forestiers(Variable):
    #exonéré dès 2020
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification au L312-60/63"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603707"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        status = 0
        if apet == type_eta._10_39A: 
            status = 1
        return status
    

class gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = ""
    definition_period = YEAR
    reference = ""
    # def formula_2022_01_01(etablissement, period):
    #     apet = etablissement("apet", period)
    #     type_eta = apet.possible_values
    #     status = 0
    #     if apet == type_eta._42_11Z:  #_42_11Z	=	"	Construction de routes et autoroutes. corresponde pas exactement
    #         status = 1
    #     return status
#Relèvent d'un tarif réduit de l'accise les gazoles consommés dans les massifs mentionnés à l'article 5 de la loi n° 85-30 du 9 janvier 1985 relative au développement et à la protection de la montagne pour les besoins des activités suivantes :
#1° Aménagement et préparation des parcours sur neige en extérieur réservés à la pratique des activités de glisse autorisées par des engins spécialement conçus à cet effet ;
#2° Déneigement des voies ouvertes à la circulation publique par des engins équipés d'outils spécifiques destinés à lutter contre le verglas ou la neige.

class autres_produits_double_usage(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification au L312-66"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603707"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._20_13B, type_eta._20_59Z, type_eta._25_50A
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant


class autre_produits_fabrication_produits_mineraux_non_metalliques(Variable):
    #Exonerée dès 2022
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "coonditions du L314-64"
    definition_period = YEAR
    reference = ""
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._23_11Z, type_eta._23_12Z, type_eta._23_13Z, type_eta._23_14Z, type_eta._23_19Z,
        type_eta._23_31Z, type_eta._23_41Z, type_eta._23_42Z, type_eta._23_43Z, type_eta._23_44Z,
        type_eta._23_49Z, type_eta._23_32Z, type_eta._23_20Z, type_eta._23_51Z, type_eta._23_65Z,
        type_eta._23_69Z, type_eta._23_61Z, type_eta._23_62Z, type_eta._23_63Z, type_eta._23_64Z,
        type_eta._23_69Z, type_eta._23_52Z, type_eta._23_70Z, type_eta._08_11Z,
        type_eta._23_91Z, type_eta._23_99Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant
    

class autres_produits_secteurs_aeronautique_et_naval(Variable):
    #Exonerée dès 2022
    #À partir de 2022, il est exclus de la taxe d'énergie en toutes les formes sauf l'électricité 
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "coonditions du L314-64"
    definition_period = YEAR
    reference = ""
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._30_30Z, type_eta._33_16Z, type_eta._30_12Z, 
        type_eta._33_15Z, type_eta._30_11Z, type_eta._28_11Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant
    

class autres_produits_intervention_vehicules_services_incendie_secours(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = ""
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047807623"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        status = 0
        if apet == type_eta._84_25Z:  #_84_25Z	=	"	Services du feu et de secours	"
            status = 1
        return status
