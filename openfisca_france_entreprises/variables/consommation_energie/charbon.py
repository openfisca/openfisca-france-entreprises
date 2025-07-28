from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable


class consommation_charbon(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Coal consumption of the etablissement"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible
    #dès 2007, seules les usages comme combustible sont soumis à la TICGN. 
    #dès 2020, les usages comme carbrant y sont somis aussi. 
    def formula_2007_01_01(etablissement, period) : 
        
        totale = etablissement('consommation_charbon_combustible', period)

        return totale
    def formula_2020_01_01(etablissement, period) : 
        
        
        totale = etablissement('consommation_charbon_combustible', period) + etablissement('consommation_charbon_carburant', period)

        return totale
    def formula_2022_01_01(etablissement, period) : 
        #selon L312-22, le charbon utilisé comme carburant est pas soumis à l'accise
        
        totale = etablissement('consommation_charbon_combustible', period)

        return totale

class consommation_charbon_carburant(Variable):
    #inclus dans le ticc à partir de 2020
    #ça fait partie de la formule de consommation_charbon
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme carburant"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704

class consommation_charbon_combustible(Variable):
    #inclus dans le ticc à partir de 2020
    #ça fait partie de la formule de consommation_charbon
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704



# class consommation_charbon_ni_combustible_ni_carburant(Variable):
#     # 
#     # non combustible ou non carburant sont exclus de la taxe à partir de 2020
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "Consommation de charbon de l'établissement, utilisé autrement que carburant ou combustible"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"
    
#     def formula_2020_01_01(etablissement, period):
#         consommation_charbon_non_combustible = etablissement("consommation_charbon_non_combustible", period)

#         return consommation_charbon_non_combustible 
#     # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704

# class consommation_charbon_non_combustible(Variable):
#     # changer à consommation_charbon_ni_combustible_ni_carburant en 2020
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "Consommation de charbon de l'établissement, utilisé autrement que comme combustible"
#     definition_period = YEAR
#     reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"
#     # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible


class charbon_double_usage(Variable):
    #à exlure dès 2022
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification au L312-66"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603707"
    def formula_2007_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        double_usage = 0
        if apet == type_eta._20_13B or apet == type_eta._20_59Z or apet == type_eta._25_50A: 
            double_usage = 1
        return double_usage

class consommation_charbon_di26(Variable):
    #ça existait de 2007 à 2008, soumise à la rubrique DI 26
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé dans un procédé de fabrication de produits minéraux non métalliques classé dans la nomenclature statistique des activités économiques dans la Communauté européenne (NACE), telle qu'elle résulte du règlement (CEE) n° 3037/90 du Conseil, du 9 octobre 1990, sous la rubrique DI 26"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"

    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible


class consommation_charbon_combustible_interne(Variable):
    #toujours à exclure 
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé par établissements de production de produits pétroliers ou assimilés [...] lorsque cette consommation est effectuée pour la production de ces produits énergétiques ou pour la production de tout ou partie de l'énergie nécessaire à leur fabrication"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"

    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible


class consommation_charbon_combustible_electricite(Variable):
    #à exclure dès 2007
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "à exclure. Consommation de charbon de l'établissement."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"


class consommation_charbon_combustible_electricite_petits_producteurs(Variable):
    #à exclure de consommation_charbon_combustible_electricite dès 2011
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "à exclure. Consommation de charbon de l'établissement, utilisé pour leurs besoins par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"


class consommation_charbon_combustible_extraction(Variable):
    #Toujours exonerée
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible dans le processus de sa fabrication et de son extraction."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041469051/2020-01-01/"


class consommation_charbon_combustible_particuliers(Variable):
    #Exonerée dès 2007 jusqu'à 2016
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible pour les particuliers."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000028447819/2014-01-01/"


class charbon_biomasse(Variable):
    #Exonerée dès 2008 et sous une autre ensemble de conditions dès 2009
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la valorisation de la biomass sous L312-75/78"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048833579"
    def formula_2008_01_01(etablissement, period):
        #vérifie que les activités inclus sont pareils en les anées précedents 
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._01_11Z, type_eta._01_12Z, type_eta._01_13Z, type_eta._01_14Z, type_eta._01_15Z,
        type_eta._01_16Z, type_eta._01_19Z, type_eta._01_21Z, type_eta._01_22Z, type_eta._01_23Z,
        type_eta._01_24Z, type_eta._01_25Z, type_eta._01_26Z, type_eta._01_27Z, type_eta._01_28Z,
        type_eta._01_29Z, type_eta._01_30Z, type_eta._01_41Z, type_eta._01_42Z, type_eta._01_43Z,
        type_eta._01_44Z, type_eta._01_45Z, type_eta._01_46Z, type_eta._01_47Z, type_eta._01_49Z,
        type_eta._01_50Z, type_eta._01_61Z, type_eta._01_62Z, type_eta._01_63Z, type_eta._01_64Z,
        type_eta._01_70Z, type_eta._02_10Z, type_eta._02_20Z, type_eta._02_30Z, type_eta._02_40Z,
        type_eta._03_11Z, type_eta._03_12Z, type_eta._03_21Z, type_eta._03_22Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant



class charbon_navigation_interieure(Variable):
    #Exonerée dès 2022
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la navigation intérieure de charbon sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._50_30Z or apet == type_eta._50_40Z:
            determinant = True
        return determinant


class charbon_navigation_maritime(Variable):
    #Exonerée dès 2022
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la navigation intérieure de charbon sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._50_10Z or apet == type_eta._50_20Z:
            determinant = True
        return determinant
    

class charbon_navigation_aerienne(Variable):
    #Exonerée dès 2022
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la navigation aérienne de charbon sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._51_10Z or apet == type_eta._51_21Z:
            determinant = True
        return determinant


class charbon_fabrication_produits_mineraux_non_metalliques(Variable):
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
    

class charbon_secteurs_aeronautique_et_naval(Variable):
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
    

##############################################
#usage pas claire 
####
class contrat_achat_electricite_314(Variable):
    value_type = bool
    entity = Etablissement
    label = "bénéficient d'un contrat d'achat d'électricité conclu en application de l'article L. 314-1 du code de l'énergie ou mentionné à l'article L. 121-27 du même code "
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032969945"
