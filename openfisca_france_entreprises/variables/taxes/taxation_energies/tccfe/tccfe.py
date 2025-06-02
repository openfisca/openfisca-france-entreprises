# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

class taxe_communale_consommation_finale_electricite(Variable):
    value_type = float 
    entity = Etablissement
    label = "" 
    definition_period = YEAR
    def formula(etablissement, period, parameters):
        taux_tccfe = etablissement("taux_tccfe", period)
        assiette_taxe_electricite = etablissement('assiette_taxe_electricite', period)
        #*** à vérifier que c'est la même assiette 

        taxe = assiette_taxe_electricite * taux_tccfe

        return taxe

class taux_tccfe(Variable):
    value_type = float 
    entity = Etablissement
    label = "" 
    definition_period = YEAR
    def formula_2011_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2011', period)
            # 0.75
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2011', period)
            # 0.25
        else :
            taux = 0
        return taux 
    def formula_2012_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2012', period)
            # 0.75
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2012', period)
            # 0.25
        else :
            taux = 0
        return taux
    def formula_2013_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2013', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2013', period)
        else :
            taux = 0
        return taux
    def formula_2014_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2014', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2014', period)
        else :
            taux = 0
        return taux
    def formula_2015_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2015', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2015', period)
        else :
            taux = 0
        return taux
    def formula_2016_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2016', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2016', period)
        else :
            taux = 0
        return taux
    def formula_2017_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2017', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2017', period)
        else :
            taux = 0
        return taux
    def formula_2018_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2018', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2018', period)
        else :
            taux = 0
        return taux
    def formula_2019_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2019', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2019', period)
        else :
            taux = 0
        return taux
    def formula_2020_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2020', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2020', period)
        else :
            taux = 0
        return taux
# 2016 : 0 ; 2 ; 4 ; 6 ; 8 ; 8,50.
# 2020 :  0 ; 2 ; 4 ; 6 ; 8 ; 8,50
# 2021 : 4 ; 6 ; 8 ; 8,5.
# 2022 : 6 ; 8 ; 8,5.
    def formula_2021_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2021', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2021', period)
        else :
            taux = 0
        return taux
    def formula_2022_01_01(etablissement, period, parameters):
        if etablissement('amperage', period) <= 36 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement('tccfe_coefficient_multiplicateur_normal_2022', period)
        elif etablissement('amperage', period) <= 250 and etablissement('amperage', period) != 0 : 
            taux = parameters(period).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement('tccfe_coefficient_multiplicateur_normal_2022', period)
        else :
            taux = 0
        return taux
    




