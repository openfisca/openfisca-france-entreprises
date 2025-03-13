from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable



class consommation_electricite(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Coal consumption of the etablissement"
    definition_period = YEAR
    reference = ""


class amperage(Variable):
    value_type = float
    unit = 'kVA'
    entity = Etablissement
    label = "Amperage de la consummation de l'establissement. Ça determine la catégorie fiscale au sein du Article L312-24."
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603823"


class electro_intensite(Variable):
    value_type = float
    unit = 'pourcentage'
    entity = Etablissement
    label = "niveau d'electro-intensité, lié au L312-65"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603709"


class electricite_double_usage(Variable):
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
# _20_13B, _20_59Z
#_25_50A
#pour la quatrème catagorie, 4° Pour les produits taxables en tant que combustible et consommés pour les besoins d'un processus déterminé, la génération d'une substance indispensable à la réalisation de ce processus et ne pouvant être générée qu'à partir de ces produits.
#j'ai aucune idée comment le faire. 


class electricite_production_a_bord(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport guidé d'élétricité sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._03_11Z, type_eta._03_12Z, type_eta._03_21Z, type_eta._03_22Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant


class electricite_transport_guide(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport guidé d'élétricité sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._33_17Z, type_eta._49_10Z, type_eta._49_20Z, type_eta._49_31Z,
        type_eta._49_39C, type_eta._52_21Z, type_eta._52_29A, type_eta._52_29B,
        type_eta._53_10Z, type_eta._53_20Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant
#_33_17Z, _49_10Z, _49_20Z, _49_31Z, _49_39C, _52_21Z, _52_29A, _52_29B, _53_10Z, _53_20Z


class electricite_transport_collectif_personnes(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie du transport collectif d'éléctricité de personnes sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._49_39A:
            determinant = True
        return determinant
#_49_39A


class electricite_alimentation_a_quai(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie d'alimentation à quai"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._52_22Z: 
            determinant = True
        return determinant


class electricite_manutention_portuaire(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de la manutention portuaire d'électricité"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._52_24A:
            determinant = True
        return determinant


class electricite_exploitation_aerodrome(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie des exploitation des aérodromes ouverts à la circulation aérienne publique	"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._52_23Z:
            determinant = True
        return determinant


class electricite_fabrication_produits_mineraux_non_metalliques(Variable):
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
#_23_11Z, _23_12Z, _23_13Z, _23_14Z, _23_19Z, 
#_23_31Z, _23_41Z, _23_42Z, _23_43Z, _23_44Z, _23_49Z, _23_32Z, _23_20Z
#_23_51Z, _23_65Z, _23_69Z, _23_61Z, _23_62Z, _23_63Z, _23_64Z, _23_69Z, _23_52Z
#_23_70Z, _08_11Z
#_23_91Z, _23_99Z, 


class electricite_production_biens_electro_intensive(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "conditions du L312-64/68"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603703/2025-03-05"
#si l’électricité représente plus de la moitié du coût total de production d’un bien, l’entreprise peut bénéficier d’un allègement fiscal


class electricite_centres_de_stockage_donnees(Variable):
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "qualification du L314-70"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200586"
    def formula_2022_01_01(etablissement, period) : 
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        determinant = False
        
        if apet == type_eta._63_11Z:
            determinant = True
        return determinant


class electro_intensive_activite_industrielle(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = "sous L312-64/65/71"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603709"  #
    def formula_2022_01_01(etablissement, period, parameters):
        """
        """
        apet = etablissement("apet", period)
        type_eta = apet.possible_values

        status = False
        if apet == type_eta._08_12Z or apet == type_eta._08_99Z or apet == type_eta._09_90Z or apet == type_eta._28_92Z :
            status = True
        
        
        return status


class electro_intensive_concurrence_internationale(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = "concurrence internationale sous L312-65/72"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603709"  #
    def formula_2022_01_01(etablissement, period, parameters):
        """
        """
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles =  [
        type_eta._07_10Z, type_eta._08_91Z, type_eta._09_90Z,
    
        type_eta._24_42Z, type_eta._24_43Z, type_eta._24_44Z, type_eta._24_45Z, type_eta._22_21Z,
        type_eta._24_20Z, type_eta._22_21Z, type_eta._24_31Z,
    
        type_eta._20_13B, type_eta._20_14Z, type_eta._07_21Z, type_eta._11_01Z,
    
        type_eta._20_15Z, type_eta._38_21Z,
    
        type_eta._20_60Z, type_eta._14_11Z,
    
        type_eta._17_11Z, type_eta._17_12Z
        ]
        determinant = False
        
        if apet in codes_eligibles:
            determinant = True
        return determinant


class consommation_electricite_energie_ou_gaz_renouvelable(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "partie une du L312-87"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635"


class consommation_electricite_puissance_moins_1_MW(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "partie deux du L312-87"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635"


class consommation_electricite_auto_consommation(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "partie trois du L312-87"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635"






