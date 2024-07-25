from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class ecart_reevaluation(Variable):
    cerfa_field = "1B"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "ECart de réévaluation incorporé au capital"
    definition_period = YEAR

class reserve_speciale_reevaluation(Variable):
    cerfa_field = "1C"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserve spéciale de réévaluation (1959)"
    definition_period = YEAR

class ecart_reevaluation_libre(Variable):
    cerfa_field = "1D"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Ecart de réévaluation libre"
    definition_period = YEAR

class rerserve_reevaluation(Variable):
    cerfa_field = "1E"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserve de réévaluation (1976)"
    definition_period = YEAR

class reserve_speciale_pv_long_terme(Variable):
    cerfa_field = "EF"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserve spéciale des plus-values à long terme"
    definition_period = YEAR

class dettes_produits_constates_avance_moins_un_an(Variable):
    cerfa_field = "EG"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dettes et produits constatés d'avance à moins d'un an"
    definition_period = YEAR

class concours_bancaires_courants(Variable):
    cerfa_field = "EH"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Concours bancaires courants, et soldes créditeurs de banques et CCP"
    definition_period = YEAR
