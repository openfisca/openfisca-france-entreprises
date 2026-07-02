from openfisca_core.model_api import YEAR, Variable
from openfisca_france_entreprises.entities import Etablissement, UniteLegale

class seqe_total_emissions(Variable):
    value_type = float
    entity = Etablissement
    label = "Émissions totales de l'entreprise"
    definition_period = YEAR

class seqe_free_quotas(Variable):
    value_type = float
    entity = Etablissement
    label = "Quotas gratuits attribués à l'entreprise"
    definition_period = YEAR
