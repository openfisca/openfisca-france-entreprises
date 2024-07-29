from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm, Establishment  # noqa F401

class produits_ex_operations_gestion(Variable):
    cerfa_field = "HA"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Produits exceptionnels sur opérations de gestion"
    definition_period = YEAR

class produits_ex_operations_capital(Variable):
    cerfa_field = "HB"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Produits exceptionnels sur opérations en capital"
    definition_period = YEAR

class produits_ex_reprises_provisions(Variable):
    cerfa_field = "HC"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Reprises sur provisions et transferts de charges (produits exceptionnels)"
    definition_period = YEAR

class produits_exceptionnels(Variable):
    cerfa_field = "HD"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Produits exceptionnels"
    definition_period = YEAR

    def formula(Firm, period):
        produits_ex_operations_capital = Firm("produits_ex_operations_capital", period)
        produits_ex_operations_gestion = Firm("produits_ex_operations_gestion", period)
        produits_ex_reprises_provisions = Firm("produits_ex_reprises_provisions", period)

        produits_ex = (
            produits_ex_operations_capital +
            produits_ex_operations_gestion +
            produits_ex_reprises_provisions
        )

        return produits_ex
