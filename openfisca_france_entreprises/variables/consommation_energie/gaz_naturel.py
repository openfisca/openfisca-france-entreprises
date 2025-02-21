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
    definition_period = YEAR

class consommation_gaz_huiles_minerales(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en huiles minerales de l'etablissement"
    definition_period = YEAR

class consommation_gaz_chauffage_habitation(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en chauffage d'habitation de l'etablissement"
    definition_period = YEAR

class consommation_gaz_production_electricite(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel en production d'électricité de l'etablissement"
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
    definition_period = YEAR     
    
class consummation_gaz_sur_place(Variable):
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
    label = "La consommation de gaz naturel  autrement que comme combustible"
    definition_period = YEAR

class consommation_gaz_double_usage(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel à un double usage"
    definition_period = YEAR

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
    definition_period = YEAR

class consommation_gaz_extraction_production(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel pour les besoins de l'extraction et de la production de gaz naturel"
    definition_period = YEAR

class consommation_gaz_particuliers(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel par des particuliers"
    definition_period = YEAR

class consommation_gaz_autorites_regionales(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "La consommation de gaz naturel par les autorités régionales"
    definition_period = YEAR

# class consommation_gaz_particuliers(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "La consommation de gaz naturel en carburant de l'etablissement"
#     definition_period = YEAR

# class consommation_gaz_particuliers(Variable):
#     value_type = float
#     unit = 'MWh'
#     entity = Etablissement
#     label = "La consommation de gaz naturel en carburant de l'etablissement"
#     definition_period = YEAR