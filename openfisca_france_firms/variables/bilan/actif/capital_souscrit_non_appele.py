from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class capital_souscrit_non_appele_brut(Variable):
    cerfa_field = "AA"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Capital souscrit non appelé"
    definition_period = YEAR
