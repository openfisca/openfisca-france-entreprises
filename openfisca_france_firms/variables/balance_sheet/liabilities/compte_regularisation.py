from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class produits_constates_avance(Variable):
    cerfa_field = "EB"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Produits constatés d'avance"
    definition_period = YEAR
