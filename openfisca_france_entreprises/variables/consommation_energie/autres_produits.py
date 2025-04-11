from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

#tecpe

class consommation_gaz_carburant(Variable): #renommer à consommation_gaz_carburant
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "consommation en consommation_gaz_carburant. Enlevé de taxation_produit petrolier (nom de concept) à gazoles_naturel dès 2020"
    reference = " https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168"
    definition_period = YEAR



class consommation_gazoles_transport_guide(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie du transport guidé de gazolesoles sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216676"
    

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

class consommation_gazoles_transport_collective_personnes(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

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

class consommation_gazoles_transport_taxi(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie du transport collectives de gazoles de personnes sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

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


class consommation_gazoles_transport_routier_marchandises(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie du transport routier de marchandises sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

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

class consommation_gazoles_navigation_interieure(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie de la navigation intérieure sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class gazoles_navigation_interieure(Variable):
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


class consommation_gazoles_navigation_maritime(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie de la navigation intérieure sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class gazoles_navigation_maritime(Variable):
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


class consommation_gazoles_manutention_portuaire(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie de la manutention portuaire de gazoles sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    


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


class consommation_gazoles_navigation_aerienne(Variable):
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie de la navigation aérienne de gazoles sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"
    

class gazoles_navigation_aerienne(Variable):
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


class consommation_gazoles_extraction_mineraux_industriels(Variable):	
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "la catagorie de l'extraction de mineraux industriels sous L312-64/70-1"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875772"
    

class gazoles_extraction_mineraux_industriels(Variable):	
    value_type = bool
    unit = ''
    entity = Etablissement
    label = "la catagorie de l'extraction de mineraux industriels sous L312-64/70-1"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875772"
    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        
        determinant = False
        
        if apet == type_eta._08_11Z or apet == type_eta._23_52Z or apet == type_eta._08_12Z:
            determinant = True
        return determinant
