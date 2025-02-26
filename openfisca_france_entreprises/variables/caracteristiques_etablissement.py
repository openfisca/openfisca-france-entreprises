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
    default_value = naf.pas_donnes



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
