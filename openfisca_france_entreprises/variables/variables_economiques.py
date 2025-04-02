#les valeurs qui varient avec l'ativité 
#valeur_ajouté 

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

class valeur_ajoutee_ul(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = YEAR
    label = "La valeur ajoutée d'une année donnée au niveau d'unité legale"

class valeur_ajoutee_eta(Variable):
    #la valeur ajoutée au niveau établissement
    value_type = float 
    entity = Etablissement
    definition_period = YEAR
    label = "La valeur ajoutée d'une année donnée au niveau d'établissement, en fonction du effectif."
    def formula_1986_01_01(etablissement, period, parameters):
        valeur_ajoutee_ul = etablissement.unite_legale("valeur_ajoutee_ul", period)
        effectif_3112_ul = etablissement.unite_legale("effectif_3112_ul", period)
        effectif_3112_eta = etablissement("effectif_3112_eta", period)
        valeur_ajoutee_eta = 0
        if effectif_3112_ul:
            valeur_ajoutee_eta = valeur_ajoutee_ul * (effectif_3112_eta/effectif_3112_ul)
        return valeur_ajoutee_eta
    
class consommation_par_valeur_ajoutee(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    unit = 'Wh par Euro' #'MWh' > Wh
    label = "Méasure de l'intensité de consommation d'énergie pour la valeur ajoutée."

    def formula_1960_01_01(etablissement, period, parameters):
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period)
        assiette_ticgn_mwh = etablissement("assiette_ticgn", period)
        assiette_ticgn_wh = assiette_ticgn_mwh * 1000000
        consommation__divisee_par_valeur_ajoutee = 0
        if valeur_ajoutee_eta:
            consommation__divisee_par_valeur_ajoutee = assiette_ticgn_wh/valeur_ajoutee_eta
        return consommation__divisee_par_valeur_ajoutee
    
class chiffre_affaires_ul(Variable):
    value_type = float
    entity = UniteLegale
    label = "La chiffre d'affaires pour une année donnée pour une unité legale"
    definition_period = YEAR

class chiffre_affaires_eta(Variable):
    value_type = float
    entity = Etablissement
    label = "La chiffre d'affaires pour une année donnée pour une établissement, en fonction du effectif."
    definition_period = YEAR
    def formula_1986_01_01(etablissement, period, parameters):
        chiffre_affaires_ul = etablissement.unite_legale("chiffre_affaires_ul", period)
        effectif_3112_ul = etablissement.unite_legale("effectif_3112_ul", period)
        effectif_3112_eta = etablissement("effectif_3112_eta", period)
        if effectif_3112_ul:
            chiffre_affaires_eta = chiffre_affaires_ul * (effectif_3112_eta/effectif_3112_ul)
        else :
            chiffre_affaires_eta = 0

        return chiffre_affaires_eta


class facture_energie_ul(Variable):
    value_type = float
    entity = UniteLegale
    label = "La facture energie pour une année donnée pour une unité legale"
    definition_period = YEAR

class facture_energie_eta(Variable):
    value_type = float
    entity = Etablissement
    label = "La facture energie pour une année donnée pour une établissement"
    definition_period = YEAR


class facture_energie_par_valeur_ajoutee_eta(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    unit = 'pourcentage' 
    label = "Méasure de l'intensité énergetique sur la valeur ajoutée."

    def formula_1960_01_01(etablissement, period, parameters):
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period)
        facture_energie_eta = etablissement("facture_energie_eta", period)
        facture_energie_par_valeur_ajoutee_eta = 0
        if valeur_ajoutee_eta:
            facture_energie_par_valeur_ajoutee_eta = facture_energie_eta/valeur_ajoutee_eta
        return facture_energie_par_valeur_ajoutee_eta
