from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm, Establishment  # noqa F401

class charges_ex_operations_gestion(Variable):
    cerfa_field = "HE"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges exceptionnelles sur opérations de gestion"
    definition_period = YEAR

class charges_ex_operations_capital(Variable):
    cerfa_field = "HF"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges exceptionnelles sur opérations en capital"
    definition_period = YEAR

class charges_ex_reprises_ar(Variable):
    cerfa_field = "HG"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dotations exceptionnelles aux amortissements et provisions"
    definition_period = YEAR

class charges_exceptionnelles(Variable):
    cerfa_field = "HH"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges exceptionnelles"
    definition_period = YEAR

    def formula(Firm, period):
        charges_ex_operations_capital = Firm("charges_ex_operations_capital", period)
        charges_ex_operations_gestion = Firm("charges_ex_operations_gestion", period)
        charges_ex_reprises_ar = Firm("charges_ex_reprises_ar", period)

        charges_ex = (
            charges_ex_operations_capital +
            charges_ex_operations_gestion +
            charges_ex_reprises_ar
        )

        return charges_ex
