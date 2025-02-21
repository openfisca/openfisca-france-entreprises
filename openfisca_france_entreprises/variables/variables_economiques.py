#les valeurs qui varient avec l'ativité 
#valeur_ajoute 

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

class valeur_ajoutee(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "La valeur ajoutée d'une année donnée"


class consummation_par_valeur_ajoutee(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Méasure de l'intensité de consommation d'énergie pour la valeur ajoutée."

    def formula_1960_01_01(etablissement, period, parameters):
        valeur_ajoutee = etablissement("valeur_ajoutee", period)
        conso = etablissement("consommation_gaz_naturel", period)
        consummation__divisee_par_valeur_ajoutee = conso/valeur_ajoutee
        return consummation__divisee_par_valeur_ajoutee