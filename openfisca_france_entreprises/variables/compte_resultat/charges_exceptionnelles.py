from openfisca_core.model_api import *
from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import (  # noqa F401
    Etablissement,
    UniteLegale,
)


class charges_ex_operations_gestion(Variable):
    cerfa_field = "HE"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Charges exceptionnelles sur opérations de gestion"
    definition_period = YEAR


class charges_ex_operations_capital(Variable):
    cerfa_field = "HF"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Charges exceptionnelles sur opérations en capital"
    definition_period = YEAR


class charges_ex_reprises_ar(Variable):
    cerfa_field = "HG"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Dotations exceptionnelles aux amortissements et provisions"
    definition_period = YEAR


class charges_exceptionnelles(Variable):
    cerfa_field = "HH"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Charges exceptionnelles"
    definition_period = YEAR

    def formula(UniteLegale, period):
        charges_ex_operations_capital = UniteLegale(
            "charges_ex_operations_capital", period
        )
        charges_ex_operations_gestion = UniteLegale(
            "charges_ex_operations_gestion", period
        )
        charges_ex_reprises_ar = UniteLegale("charges_ex_reprises_ar", period)

        charges_ex = (
            charges_ex_operations_capital
            + charges_ex_operations_gestion
            + charges_ex_reprises_ar
        )

        return charges_ex
