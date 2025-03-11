from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class consommation_gaz_naturel(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Natural gas consumption of the etablissement"
    definition_period = YEAR

class consommation_gaz_matiere_premiere(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en matière première de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/" 
    definition_period = YEAR

class gaz_matiere_premiere(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel en matière première de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/" 
    definition_period = YEAR

class consommation_gaz_huiles_minerales(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en huiles minerales de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"
    definition_period = YEAR

class gaz_huiles_minerales(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel en huiles minerales de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"
    definition_period = YEAR

class consommation_gaz_chauffage_habitation(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en chauffage d'habitation de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"
    definition_period = YEAR

class gaz_chauffage_habitation(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel en chauffage d'habitation de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"
    definition_period = YEAR

class consommation_gaz_production_electricite(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en production d'électricité de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615172/2006-12-31/"
    definition_period = YEAR

class gaz_production_electricite(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel en production d'électricité de l'etablissement"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615172/2006-12-31/"
    definition_period = YEAR

class consommation_gaz_production_electricite_non_exonere(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = """
            en version de 2008 : La consommation de gaz naturel en production d'électricité de l'etablissement 
                * sauf pour les installations visées à l'article 266 quinquies A
                    ++ sauf quand celles-ci ne bénéficient pas d'un tarif d'achat d'électricité dans le cadre l'article 10 de la loi n° 2000-108 du 10 février 2000
            en version de 2011 : Ça va comprendre la consommation du gaz utilisé pour la production d'électricité par les petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2 du code général des collectivités territoriales.
            """
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
    definition_period = YEAR     
    def formula_2008_01_01(etablissement, period):
        conso_installation_266qA = etablissement("consommation_gaz_combustible_electricite_266qA", period)
        conso_gaz_non_beneficier_tarif_achat_2000_108 = etablissement("consommation_gaz_non_beneficier_tarif_achat_2000_108", period)
        return (conso_installation_266qA - conso_gaz_non_beneficier_tarif_achat_2000_108)
    def formula_2011_01_01(etablissement, period):
        conso_installation_266qA = etablissement("consommation_gaz_combustible_electricite_266qA", period)
        conso_gaz_non_beneficier_tarif_achat_2000_108 = etablissement("consommation_gaz_non_beneficier_tarif_achat_2000_108", period)
        conso_petitprod = etablissement("consommation_gaz_electricite_petits_producteurs", period)
        return (conso_installation_266qA - conso_gaz_non_beneficier_tarif_achat_2000_108 + conso_petitprod)

class consommation_gaz_combustible_electricite_266qA(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "c"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
    definition_period = YEAR 

class consommation_gaz_non_beneficier_tarif_achat_2000_108(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = ""
    reference : "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000023181905"
    definition_period = YEAR 

class gaz_non_beneficier_tarif_achat_2000_108(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = ""
    reference : "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000023181905"
    definition_period = YEAR 

class consommation_gaz_electricite_petits_producteurs(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000023216090/2011-01-01/"
    definition_period = YEAR 

class gaz_electricite_petits_producteurs(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000023216090/2011-01-01/"
    definition_period = YEAR 

class consummation_gaz_sur_place(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel dans l'enceinte des établissements de production de produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/2008-01-01/?anchor=LEGIARTI000018036100#LEGIARTI000018036100:~:text=III.%2DLa%20consommation,%C3%A0%20leur%20fabrication."
    definition_period = YEAR

class gaz_sur_place(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel dans l'enceinte des établissements de production de produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/2008-01-01/?anchor=LEGIARTI000018036100#LEGIARTI000018036100:~:text=III.%2DLa%20consommation,%C3%A0%20leur%20fabrication."
    definition_period = YEAR

class consommation_gaz_usage_non_combustible(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel autrement que comme combustible"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
    definition_period = YEAR

class gaz_usage_non_combustible(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "La consommation de gaz naturel autrement que comme combustible"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
    definition_period = YEAR

class consommation_gaz_double_usage(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel à un double usage"
    reference : """https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/ 
                et https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000028447925/2025-02-21 """
    definition_period = YEAR

class gaz_double_usage(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification au L312-66"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603707"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        double_usage = 0
        if apet == type_eta._20_13B or apet == type_eta._20_59Z or apet == type_eta._25_50A: 
            double_usage = 1
        return double_usage

# class consommation_gaz_production_electricite # v2?(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "La consommation de gaz naturel pour la production d'électricité"
# #                 * sauf pour les installations visées à l'article 266 quinquies A
# #                     ++ sauf quand celles-ci ne bénéficient pas d'un tarif d'achat d'électricité dans le cadre l'article 10 de la loi n° 2000-108 du 10 février 2000  
#     definition_period = YEAR

class consommation_gaz_production_mineraux_non_metalliques(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel dans un procédé de fabrication de produits minéraux non métalliques"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/#:~:text=3%C2%B0%20Dans%20un%20proc%C3%A9d%C3%A9%20de%20fabrication%20de%20produits%20min%C3%A9raux%20non%20m%C3%A9talliques%20mentionn%C3%A9%20au%203%C2%B0%20du%20I%20de%20l%27article%20265%20C."
    definition_period = YEAR

class consommation_gaz_extraction_production(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel pour les besoins de l'extraction et de la production de gaz naturel"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/"
    definition_period = YEAR

class consommation_gaz_particuliers(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel par des particuliers"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/" 
    definition_period = YEAR

class consommation_gaz_autorites_regionales(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel par les autorités régionales"
    reference : "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018036078/2008-04-01/" 
    definition_period = YEAR






