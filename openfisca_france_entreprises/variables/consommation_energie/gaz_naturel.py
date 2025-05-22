from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class consommation_gaz_naturel(Variable):
    #dès 1986, seules les usages comme combustible sont soumis à la TICGN. 
    #dès 2020, les usages comme carbrant y sont somis aussi. '
    #dès 2022, le gaz naturel combustible et le gaz naturel carburant ont des taux differents
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Natural gas consumption of the etablissement"
    definition_period = YEAR
    def formula_1986_01_01(etablissement, period) : 
        
        totale = etablissement('consommation_gaz_combustible', period)

        return totale
    def formula_2020_01_01(etablissement, period) : 
        #la division entre les deux s'apparaître en cette année
        
        totale = etablissement('consommation_gaz_combustible', period) + etablissement('consommation_gaz_carburant', period)

        return totale

class consommation_gaz_combustible(Variable):
    #dès 1986, seules les usages comme combustible sont soumis à la TICGN. 
    #dès 2020, les usages comme carbrant y sont somis aussi. 
    #dès 2022, le gaz naturel combustible et le gaz naturel carburant ont des taux differents

    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Usages du gaz naturel comme combustible"
    definition_period = YEAR


class consommation_gaz_carburant(Variable): 
    #ça fait partie de la formule de consommation_gaz_naturel dès 2020
    #dès 2022, le gaz naturel combustible et le gaz naturel carburant ont des taux differents

    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "consommation en consommation_gaz_carburant. Enlevé de taxation_produit petrolier (nom de concept) à gazoles_naturel dès 2020"
    reference = " https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168"
    definition_period = YEAR



class gaz_matiere_premiere(Variable):
    #exonéré dès 1993 (dec 1992) jusqu'à 2008
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel en matière première de l'etablissement"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/'
    definition_period = YEAR
    def formula_1992_01_01(etablissement, period, parameters): 
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        #voici une liste que j'ai fait. C'est fortement possible que j'ai raté quelques activités.
        codes_eligibles = [
        type_eta._19_20Z, type_eta._20_11Z, type_eta._20_13B, type_eta._20_14Z, 
        type_eta._20_15Z, type_eta._20_16Z, type_eta._20_17Z, type_eta._20_60Z,
        type_eta._23_52Z, type_eta._23_51Z, type_eta._24_10Z, type_eta._24_41Z,
        type_eta._24_42Z, type_eta._24_43Z, type_eta._24_44Z, type_eta._24_45Z, 
        type_eta._24_46Z
        ]
        determinant = False   
        if apet in codes_eligibles:
            determinant = True
        return determinant
#_19_20Z, _20_11Z, _20_13B, _20_14Z , _20_15Z , _20_16Z , _20_17Z , _20_60Z 
#_23_52Z , _23_51Z , _24_10Z , _24_41Z 
#_24_42Z , _24_43Z , _24_44Z , _24_45Z , _24_46Z 
#
#



class gaz_huiles_minerales(Variable):
    #exonéré dès 1993 (dec 1992) jusquà 2008
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel en huiles minerales de l'etablissement"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"
    definition_period = YEAR
    def formula_1992_01_01(etablissement, period, parameters): 
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        #voici une liste que j'ai fait. C'est fortement possible que j'ai raté quelques activités.
        codes_eligibles = [
        type_eta._19_20Z, type_eta._05_10Z, type_eta._05_20Z, type_eta._06_10Z, type_eta._06_20Z,
        type_eta._07_10Z, type_eta._07_21Z, type_eta._07_29Z, type_eta._08_11Z,
        type_eta._08_12Z, type_eta._08_91Z, type_eta._08_92Z
        ]
        determinant = False   
        if apet in codes_eligibles:
            determinant = True
        return determinant

 


class consommation_gaz_chauffage_habitation(Variable):
    #exonéré dès 1993 à 2014 (avril 2014)
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en chauffage d'habitation de l'etablissement"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"
    definition_period = YEAR

class consommation_gaz_production_electricite(Variable):
    #exonerée dès 2006 avec des exceptions
    #soustraire de l'assiette 
    #NB : soustraire de l'assiette -> consommation, condition de taxe -> valeur booleanne
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en production d'électricité de l'etablissement"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615172/2006-12-31/"
    definition_period = YEAR


# # class consommation_gaz_beneficier_tarif_achat_2000_108(Variable):
#     #dès 2007 à 2020, cogéneration +  contrat d'achat  = pas exonéré en cadre de production d'électricité
#     #soustraire de l'assiette 
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = ""
#     reference = "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000023181905"
#     definition_period = YEAR 
# #trop compliqué :(


class consommation_gaz_electricite_petits_producteurs(Variable):
    #exclu d'exonération en tant que la production d'électricité dès 2011
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000023216090/2011-01-01/"
    definition_period = YEAR 


class consommation_gaz_fabrication_soi(Variable):
    #Article 265 C, exonéré dès 2008 à 2022
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ''
    reference = "La consommation de gaz naturel dans l'enceinte des établissements de production de produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/2008-01-01/?anchor=LEGIARTI000018036100#LEGIARTI000018036100:~:text=III.%2DLa%20consommation,%C3%A0%20leur%20fabrication."
    definition_period = YEAR

#remplacé par la logique que les formes de gaz naturel pas utilisé sont automatiquement prises en compte comme non combustible.
# class consommation_gaz_usage_non_combustible(Variable):
#     #exonéré dès 2008 
#     #combiner gaz_matiere_premiere et gaz_huiles_minerales
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "La consommation de gaz naturel autrement que comme combustible"
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
#     definition_period = YEAR
#     def formula_2008_01_01(etablissement, period):
#         status = False
#         if etablissement("gaz_matiere_premiere", period) == True or etablissement("gaz_huiles_minerales", period) == True:
#             status = True
#         return status

#penser à ajouter des autres usages 

class gaz_double_usage(Variable):
    #exonéré dès 2008
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification au L312-66"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603707"
    def formula_2008_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._20_13B, type_eta._20_59Z, type_eta._25_50A
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant

class gaz_production_mineraux_non_metalliques(Variable):
    #exonéré dès 2008
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel dans un procédé de fabrication de produits minéraux non métalliques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/#:~:text=3%C2%B0%20Dans%20un%20proc%C3%A9d%C3%A9%20de%20fabrication%20de%20produits%20min%C3%A9raux%20non%20m%C3%A9talliques%20mentionn%C3%A9%20au%203%C2%B0%20du%20I%20de%20l%27article%20265%20C."
    definition_period = YEAR
    def formula_2008_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._23_11Z, type_eta._23_12Z, type_eta._23_13Z, type_eta._23_14Z,
        type_eta._23_19Z, type_eta._23_20Z, type_eta._23_31Z, type_eta._23_32Z,
        type_eta._23_41Z, type_eta._23_42Z, type_eta._23_43Z, type_eta._23_44Z,
        type_eta._23_49Z, type_eta._23_51Z, type_eta._23_52Z, type_eta._23_61Z,
        type_eta._23_62Z, type_eta._23_63Z, type_eta._23_64Z, type_eta._23_65Z,
        type_eta._23_69Z, type_eta._23_70Z, type_eta._23_91Z, type_eta._23_99Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant
#"3° Lorsqu'ils sont utilisés dans un procédé de fabrication de produits minéraux non métalliques, classé dans la nomenclature statistique des activités économiques dans la Communauté européenne, telle qu'elle résulte du règlement (CEE) n° 3037 / 90 du 9 octobre 1990 du Conseil, sous la rubrique " DI 26 "."


class gaz_extraction_production(Variable):
    #exonéré dès 2008
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel pour les besoins de l'extraction et de la production de gaz naturel"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
    definition_period = YEAR
    def formula_2008_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._06_20Z 
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant

class consommation_gaz_particuliers(Variable):
    #exonéré dès 2008
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel par des particuliers"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/" 
    definition_period = YEAR

# class consommation_gaz_autorites_regionales(Variable):
#     #exonéré dès 2008 jusqu'à 2009
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "La consommation de gaz naturel par les autorités régionales"
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/" 
#     definition_period = YEAR
# #je l'ai suprimmé car c'est pas pertinant 


class gaz_dehydration_legumes_et_plantes_aromatiques(Variable):
    #exonéré dès 2019
    #condition basé sur la consommation divisée par la valeur ajouté jusqu'à 2022
    #condition basé sur le niveau d'intisité énergetique divisée par la valeur ajouté dès 2022
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification au L312-60/62"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200591"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        status = 0
        if apet == type_eta._10_39A: 
            status = 1
        return status
    
class gaz_travaux_agricoles_et_forestiers(Variable):
    #exonéré dès 2020
    #TODO : pas d'exonération dans l'accise, c'est un tariff diffrent
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
    
class consommation_gaz_cogeneration(Variable):
    #liée avec la vériable date_installation_cogeneration dans carateristique_etablissement
    #dès 2000, mais seulement pendant les 5 ans après l'installation
    # installations mises en service, au plus tard, le 31 décembre 2007
    #jusqu'à la loi de la version 2006 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "qualification à l'Article 266 quinquies A"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615174/1999-12-31"



class consommation_gaz_nc_4401_4402(Variable):
    #exonerées dès 2008 à 2022
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "exonerées selon l'Article 265 C"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/#LEGISCTA000006122062:~:text=%C2%B0%20Lorsqu%27il%20s%27agit%20de%20produits%20repris%20aux%20codes%20NC%204401%20et%204402%20de%20la%20nomenclature%20douani%C3%A8re%20%3B"
#I.-Les produits énergétiques mentionnés à l'article 265 ne sont pas soumis aux taxes intérieures de consommation :
#1° Lorsqu'il s'agit de produits repris aux codes NC 4401 et 4402 de la nomenclature douanière ;
#4401 	Bois de chauffage en rondins, bûches, ramilles, fagots ou sous formes similaires; bois en plaquettes ou en particules; sciures, déchets et débris de bois, même agglomérés sous forme de bûches, briquettes, granulés ou sous formes similaires 
#4402	Charbon de bois (y compris le charbon de coques ou de noix), même aggloméré


class consommation_gaz_nc_2705(Variable):
    #exonerées de 2008 à 2021
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "exonerées selon l'Article 266 qq"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/, https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615107/2006-12-27"
#NC 2705
#2705-50, Mélanges à forte teneur en hydrocarbures aromatiques distillant 65 % ou plus de leur volume à 250° C d'après la méthode ASTM D 86, destinés à être utilisés comme carburants ou combustibles : indice 2, hectolitre ou 100 kg net, taxe intérieure selon le type de produit.
#Sont également exonérés de la taxe intérieure de consommation mentionnée au 1 les gaz repris au code NC 2705

class consommation_gaz_nc_2711_29(Variable):
    #exonerées dès 2014
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "exonerées selon l'Article 266 qq"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/, https://www.edouane.com/wp-content/uploads/2019/07/7312.pdf"
#ensemble des hydrocarbures à l’état gazeux, autres que le gaz naturel, notamment le biogaz
#Sont également exonérés de la taxe intérieure de consommation mentionnée au 1 les gaz repris au code NC 2705, ainsi que le biogaz repris au code NC 2711-29, lorsqu'il n'est pas mélangé au gaz naturel.



