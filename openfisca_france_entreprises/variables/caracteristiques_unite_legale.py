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

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class apen(Enum):
    value_type = str
    max_length = 5
    entity = UniteLegale
    definition_period = MONTH
    label = "Sector of the unite_legale"
    set_input = set_input_dispatch_by_period


class postal_code_unite_legale(Variable):
    value_type = str
    max_length = 5
    entity = UniteLegale
    definition_period = MONTH
    label = "Postal code of the unite_legale"

    """
    We define the unite_legale's postal code as the unite_legale's siege_social etablissement's postal code.
    """

    def formula(unite_legale, period):
        hq = unite_legale.members(has_role ="siege_social")

        return hq("postal_code", period)


# class entreprises_risque_de_fuite_carbone(Variable):
#     #pas utilisé car on en a un au niveau établissement
#     value_type = bool
#     entity = UniteLegale
#     label = "Entreprise exposée au risque de fuite carbone"
#     definition_period = YEAR
#     reference = 'DÉCISION DÉLÉGUÉE (UE) 2019/708 DE LA COMMISSION du 15 février 2019'
#     def formula_2019_01_01(etablissement, period):
#         apet = etablissement("apet", period)
#         type_eta = apet.possible_values
#         codes_eligibles = [
#         type_eta._05_10Z, type_eta._05_20Z, type_eta._07_10Z, type_eta._07_29Z, type_eta._08_91Z,
#         type_eta._08_99Z, type_eta._10_41A, type_eta._10_41B, type_eta._10_62Z, type_eta._10_81Z,
#         type_eta._11_06Z, type_eta._13_10Z, type_eta._13_95Z, type_eta._14_11Z, type_eta._16_21Z,
#         type_eta._17_11Z, type_eta._17_12Z, type_eta._19_10Z, type_eta._19_20Z, type_eta._20_11Z,
#         type_eta._20_12Z, type_eta._20_13B, type_eta._20_14Z, type_eta._20_15Z, type_eta._20_16Z,
#         type_eta._20_17Z, type_eta._20_60Z, type_eta._23_11Z, type_eta._23_13Z, type_eta._23_14Z,
#         type_eta._23_19Z, type_eta._23_20Z, type_eta._23_31Z, type_eta._23_51Z, type_eta._23_52Z,
#         type_eta._23_99Z, type_eta._24_10Z, type_eta._24_20Z, type_eta._24_31Z, type_eta._24_42Z,
#         type_eta._24_43Z, type_eta._24_44Z, type_eta._24_45Z, type_eta._24_46Z, type_eta._24_51Z,
#         type_eta._08_93Z, type_eta._13_30Z, type_eta._21_10Z, type_eta._23_41Z, type_eta._23_42Z,
#         type_eta._23_32Z, type_eta._08_12Z, type_eta._10_31Z, type_eta._10_39A, type_eta._10_51D,
#         type_eta._10_51D, type_eta._10_51D, type_eta._10_51D, type_eta._10_51D, type_eta._10_89Z,
#         type_eta._20_30Z, type_eta._20_30Z, type_eta._25_50A
#         ]
#         determinant = False
#         if apet in codes_eligibles:
#             determinant = True
#         return determinant
#faut faire des autres listes selon la période d'utilisation

class effectif_3112_ul(Variable):
    #le nombre de personnes qui travaillent 
    value_type = float
    entity = UniteLegale
    label = "Effectifs en fin d'année, ETP, au niveau d'unité legale"
    definition_period = YEAR