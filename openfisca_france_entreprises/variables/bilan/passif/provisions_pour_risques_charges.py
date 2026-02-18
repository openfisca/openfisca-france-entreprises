from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_entreprises.entities import UniteLegale  # noqa F401


class provisions_pour_risques(Variable):
    cerfa_field = "DP"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Provisions pour risques"
    definition_period = YEAR


class provisions_pour_charges(Variable):
    cerfa_field = "DQ"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Provisions pour charges"
    definition_period = YEAR


class provisions_pour_risques_charges(Variable):
    cerfa_field = "DR"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Provisions pour risques et charges (total III)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        risques = UniteLegale("provisions_pour_risques", period)
        charges = UniteLegale("provisions_pour_charges", period)

        provisions = risques + charges

        return provisions
