from openfisca_core.model_api import *
from openfisca_france_firms.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class consommation_charbon(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Coal consumption of the etablissement"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

    def formula(etablissement, period):
        conso_non_combustible = etablissement("consommation_charbon_non_combustible", period)
        conso_double_usage = etablissement("consommation_charbon_double_usage", period)
        conso_di26 = etablissement("consommation_charbon_di26", period)
        conso_combustible = etablissement("consommation_charbon_combustible", period)

        return (conso_non_combustible +
                conso_double_usage +
                conso_di26 +
                conso_combustible)

class consommation_charbon_non_combustible(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé autrement que comme combustible"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

    def formula(etablissement, period):
      conso_carburant = etablissement("consommation_charbon_carburant", period)
      conso_non_combustible_non_carburant = etablissement("consommation_charbon_non_combustible_non_carburant", period)
      
      return conso_carburant + conso_non_combustible_non_carburant

class consommation_charbon_non_combustible_non_carburant(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé autrement que carburant ou combustible"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 

class consommation_charbon_carburant(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme carburant"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 

class consommation_charbon_double_usage(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé à double usage"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

    def formula_2007_01_01(etablissement, period):
        conso_double = etablissement("consommation_charbon_double_usage_reductionchimique", period)
        return conso_double

    def formula_2009_01_01(etablissement, period):
        conso_double = etablissement("consommation_charbon_double_usage_265C", period)
        return conso_double

class consommation_charbon_double_usage_reductionchimique(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé à double usage, [...] notamment [...] [utilisé] dans des procédés métallurgiques ou de réduction chimique."
    definition_period = YEAR

class consommation_charbon_double_usage_265C(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé à double usage au sens du 2° du I de l'article 265 C"
    definition_period = YEAR

class consommation_charbon_di26(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé dans un procédé de fabrication de produits minéraux non métalliques classé dans la nomenclature statistique des activités économiques dans la Communauté européenne (NACE), telle qu'elle résulte du règlement (CEE) n° 3037/90 du Conseil, du 9 octobre 1990, sous la rubrique DI 26"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class consommation_charbon_combustible(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

    def formula(etablissement, period):
        conso_combustible_interne = etablissement("consommation_charbon_combustible_interne", period)
        conso_combustible_prodelec = etablissement("consommation_charbon_combustible_electricite", period)
        conso_combustible_extraction = etablissement("consommation_charbon_combustible_extraction", period)
        conso_combustible_particuliers = etablissement("consommation_charbon_combustible_particuliers", period)
        conso_combustible_biomasse = etablissement("consommation_charbon_combustible_biomasse", period)
        conso_combustible_other = etablissement("consommation_charbon_combustible_other", period)

        return (conso_combustible_interne + 
                conso_combustible_prodelec +
                conso_combustible_extraction + 
                conso_combustible_particuliers + 
                conso_combustible_biomasse +
                conso_combustible_other)

class consommation_charbon_combustible_interne(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé par établissements de production de produits pétroliers ou assimilés [...] lorsque cette consommation est effectuée pour la production de ces produits énergétiques ou pour la production de tout ou partie de l'énergie nécessaire à leur fabrication"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class consommation_charbon_combustible_electricite(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé pour la production d'électricité"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

    def formula(etablissement, period):
        conso_266qA = etablissement("consommation_charbon_combustible_electricite_266qA", period)
        conso_petitprod = etablissement("consommation_charbon_combustible_electricite_petits_producteurs", period)
        conso_other = etablissement("consommation_charbon_combustible_electricite_other", period)

        return conso_266qA + conso_petitprod + conso_other

class consommation_charbon_combustible_electricite_266qA(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé pour la production d'électricité par une installation mentionnée à l'article 266 quinquies A du CDD."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class contrat_achat_electricite_314(Variable):
    value_type = bool
    entity = Etablissement
    label = "bénéficient d'un contrat d'achat d'électricité conclu en application de l'article L. 314-1 du code de l'énergie ou mentionné à l'article L. 121-27 du même code "
    definition_period = YEAR

class consommation_charbon_combustible_electricite_petits_producteurs(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé pour leurs besoins par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class consommation_charbon_combustible_electricite_other(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé pour la production d'électricité, autre."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 


class consommation_charbon_combustible_extraction(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible dans le processus de sa fabrication et de son extraction."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class consommation_charbon_combustible_particuliers(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible pour les particuliers."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class consommation_charbon_combustible_biomasse(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé par les entreprises de valorisation de la biomasse, sous réserve qu'elles soient soumises au régime des quotas d'émission de gaz à effet de serre prévu aux articles L. 229-5 à L. 229-19 du code de l'environnement ou qu'elles appliquent des accords volontaires de réduction de gaz à effet de serre permettant d'atteindre des objectifs environnementaux équivalents ou d'accroître leur rendement énergétique."
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 

class consommation_charbon_combustible_other(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consommation de charbon de l'établissement, utilisé comme combustible, non exonérée"
    definition_period = YEAR
    # houilles, lignites et cokes repris aux codes NC 2701, 2702 et 2704 et destinés à être utilisés comme combustible 
