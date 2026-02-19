from openfisca_core.model_api import *
from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import (  # noqa F401
    Etablissement,
    UniteLegale,
)


class produits_ex_operations_gestion(Variable):
    cerfa_field = "HA"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits exceptionnels sur opérations de gestion"
    definition_period = YEAR


class produits_ex_operations_capital(Variable):
    cerfa_field = "HB"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits exceptionnels sur opérations en capital"
    definition_period = YEAR


class produits_ex_reprises_provisions(Variable):
    cerfa_field = "HC"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Reprises sur provisions et transferts de charges (produits exceptionnels)"
    definition_period = YEAR


class produits_exceptionnels(Variable):
    cerfa_field = "HD"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits exceptionnels"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_ex_operations_capital = UniteLegale(
            "produits_ex_operations_capital", period
        )
        produits_ex_operations_gestion = UniteLegale(
            "produits_ex_operations_gestion", period
        )
        produits_ex_reprises_provisions = UniteLegale(
            "produits_ex_reprises_provisions", period
        )

        produits_ex = (
            produits_ex_operations_capital
            + produits_ex_operations_gestion
            + produits_ex_reprises_provisions
        )

        return produits_ex
