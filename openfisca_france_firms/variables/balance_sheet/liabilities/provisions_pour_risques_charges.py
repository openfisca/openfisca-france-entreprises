from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class provisions_pour_risques(Variable):
    cerfa_field = "DP"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Provisions pour risques"
    definition_period = YEAR

class provisions_pour_charges(Variable):
    cerfa_field = "DQ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Provisions pour charges"
    definition_period = YEAR

class provisions_pour_risques_charges(Variable):
    cerfa_field = "DR"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Provisions pour risques et charges (total III)"
    definition_period = YEAR

    def formula(Firm, period):
        risques = Firm("provisions_pour_risques", period)
        charges = Firm("provisions_pour_charges", period)

        provisions = (risques +
                      charges)

        return provisions
