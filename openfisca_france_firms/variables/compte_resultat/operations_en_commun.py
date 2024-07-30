from openfisca_core.model_api import *
from openfisca_france_firms.entities import UniteLegale, Etablissement  # noqa F401

class benefice_attribue(Variable):
    cerfa_field = "GH"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Bénéfice attribuée ou perte transférée"
    definition_period = YEAR

class perte_supportee(Variable):
    cerfa_field = "GI"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Perte supportée ou bénéfice transféré"
    definition_period = YEAR

class operations_en_commun(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Opérations en commun"
    definition_period = YEAR

    def formula(UniteLegale, period):
        benefice_attribue = UniteLegale("benefice_attribue", period)
        perte_supportee = UniteLegale("perte_supportee", period)

        operations = benefice_attribue - perte_supportee

        return operations
