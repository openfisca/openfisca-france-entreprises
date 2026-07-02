from openfisca_core.model_api import Variable, YEAR
from openfisca_france_entreprises.entities import Etablissement, UniteLegale

class seqe_price_paid(Variable):
    value_type = float
    entity = Etablissement
    label = "Montant payé par l'entreprise en quotas via le SEQE"
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        total_emissions = etablissement("seqe_total_emissions", period)
        free_quotas = etablissement("seqe_free_quotas", period)
        price_quota = parameters(period).taxation_emissions.seqe.price_quotas

        chargeable_emissions = total_emissions - free_quotas  # On s'intéressse seulement au résultat net, sous l'hypothèse que les entreprises vendent leurs quotas gratuits et engrengent une plus value.
        return chargeable_emissions * price_quota
