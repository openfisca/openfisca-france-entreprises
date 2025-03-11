"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
from openfisca_france_entreprises.variables.naf import naf

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class apet(Variable):
    value_type = Enum #voir dans openfisca_france comment le faire
    entity = Etablissement
    label = "Secteur NAF de l'établissement" #nomencultures des activités françaises
    #mettre tous les valeurs NAF, les deux colomnes
    definition_period = YEAR
    possible_values = naf
    default_value = naf.manquant 



class postal_code(Variable):
    value_type = str
    max_length = 5
    entity = Etablissement
    definition_period = MONTH
    label = "Postal code of the etablissement"


class effectif_3112_eta(Variable):
    #le nombre de personnes qui travaillent 
    value_type = float
    entity = Etablissement
    label = "Effectifs en fin d'année, ETP"
    definition_period = YEAR


class installation_cogeneration(Variable):
    value_type = bool
    entity = Etablissement
    label = "Installation de cogénération pour la production combinée de chaleur et d'électricité"
    definition_period = YEAR


class installation_euets(Variable):
    #remplacer par _seqe, et on a déjà l'information sur ça. 
    value_type = bool
    entity = Etablissement
    label = "Installation soumise au système européen de quotas carbone"
    definition_period = YEAR


# class installation_electrointensive(Variable):
#     value_type = bool
#     entity = Etablissement
#     label = "Installation électrointensive"
#     definition_period = YEAR
    

#     def formula_2014_01_01(etablissement, period):

#         return True

#     def formula_2021_01_01(etablissement, period):

#         return True


class installation_grande_consommatrice(Variable):
    value_type = bool
    entity = Etablissement
    label = "Installation grande consommatrice d'énergie"
    definition_period = YEAR

    # def formula_2014_01_01(etablissement, period):

    #     return True

    # def formula_2021_01_01(etablissement, period):

    #     return True


class risque_de_fuite_carbone_eta(Variable):
    value_type = bool
    entity = Etablissement
    label = "Entreprise exposée au risque de fuite carbone"
    definition_period = YEAR
    reference = 'DÉCISION DÉLÉGUÉE (UE) 2019/708 DE LA COMMISSION du 15 février 2019'
    def formula_2019_01_01(etablissement, period):
        apet = etablissement("apet", period)
        type_eta = apet.possible_values
        codes_eligibles = [
        type_eta._05_10Z, type_eta._05_20Z, type_eta._07_10Z, type_eta._07_29Z, type_eta._08_91Z,
        type_eta._08_99Z, type_eta._10_41A, type_eta._10_41B, type_eta._10_62Z, type_eta._10_81Z,
        type_eta._11_06Z, type_eta._13_10Z, type_eta._13_95Z, type_eta._14_11Z, type_eta._16_21Z,
        type_eta._17_11Z, type_eta._17_12Z, type_eta._19_10Z, type_eta._19_20Z, type_eta._20_11Z,
        type_eta._20_12Z, type_eta._20_13B, type_eta._20_14Z, type_eta._20_15Z, type_eta._20_16Z,
        type_eta._20_17Z, type_eta._20_60Z, type_eta._23_11Z, type_eta._23_13Z, type_eta._23_14Z,
        type_eta._23_19Z, type_eta._23_20Z, type_eta._23_31Z, type_eta._23_51Z, type_eta._23_52Z,
        type_eta._23_99Z, type_eta._24_10Z, type_eta._24_20Z, type_eta._24_31Z, type_eta._24_42Z,
        type_eta._24_43Z, type_eta._24_44Z, type_eta._24_45Z, type_eta._24_46Z, type_eta._24_51Z,
        type_eta._08_93Z, type_eta._13_30Z, type_eta._21_10Z, type_eta._23_41Z, type_eta._23_42Z,
        type_eta._23_32Z, type_eta._08_12Z, type_eta._10_31Z, type_eta._10_39A, type_eta._10_51D,
        type_eta._10_51D, type_eta._10_51D, type_eta._10_51D, type_eta._10_51D, type_eta._10_89Z,
        type_eta._20_30Z, type_eta._20_30Z, type_eta._25_50A
        ]
        determinant = False
        if apet in codes_eligibles:
            determinant = True
        return determinant
#faut changer à l'établissement
#faut faire des autres listes selon la période d'utilisation



class intensite_echanges_avec_pays_tiers(Variable):
    value_type = float
    unit = "pourcentage"
    entity = Etablissement
    label = "L'intensité des échanges avec les pays tiers, appliqué au sein de L312-65, -73"
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046196784'
    