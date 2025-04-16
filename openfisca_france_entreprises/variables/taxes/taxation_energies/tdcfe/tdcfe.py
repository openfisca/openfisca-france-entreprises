# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

class taxe_departementale_consommation_finale_electricite(Variable):
    value_type = float 
    entity = Etablissement
    label = "" 
    definition_period = YEAR
    def formula(etablissement, period, parameters):
        taux_tdcfe = etablissement("taux_tdcfe", period)
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite', period)
        #*** à vérifier que c'est la même assiette 

        taxe = assiette_taxe_electricite * taux_tdcfe

        return taxe

class taux_tdcfe(Variable):
    value_type = float 
    entity = Etablissement
    label = "" 
    definition_period = YEAR
    def formula_2012_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2012', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2012', period)
        else :
            taux = 0
        return taux
    def formula_2013_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2013', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2013', period)
        else :
            taux = 0
        return taux
    def formula_2014_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2014', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2014', period)
        else :
            taux = 0
        return taux
    def formula_2015_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2015', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2015', period)
        else :
            taux = 0
        return taux
    def formula_2016_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2016', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2016', period)
        else :
            taux = 0
        return taux
    def formula_2017_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2017', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2017', period)
        else :
            taux = 0
        return taux
    def formula_2018_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2018', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2018', period)
        else :
            taux = 0
        return taux
    def formula_2019_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2019', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2019', period)
        else :
            taux = 0
        return taux
def formula_2020_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2020', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2020', period)
        else :
            taux = 0
        return taux
def formula_2021_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tdcfe_coefficient_multiplicateur_normal_2021', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tdcfe_coefficient_multiplicateur_normal_2021', period)
        else :
            taux = 0
        return taux
