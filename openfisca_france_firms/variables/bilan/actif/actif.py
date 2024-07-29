from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class actif_brut(Variable):
    #cerfa_field = "CO"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Actif brut (Total général I à VI)"
    definition_period = YEAR

    def formula(Firm, period):
        total_i = Firm("capital_souscrit_non_appele_brut", period)
        total_ii = Firm("actif_immobilise_brut", period)
        total_iii = Firm("actif_total_iii_brut", period)
        total_iv = Firm("frais_emission_emprunt", period)
        total_v = Firm("primes_remboursement_obligations", period)
        total_vi = Firm("ecarts_conversion_actif", period)
        total_general = (total_i+
                         total_ii+
                         total_iii+
                         total_iv+
                         total_v+
                         total_vi)
        return total_general

class actif_ar(Variable):
    cerfa_field = "1A"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = " : amortissements, provisions"
    definition_period = YEAR

    def formula(Firm, period):
        total_ii = Firm("actif_immobilise_ar", period)
        total_iii = Firm("actif_total_iii_ar", period)
        total_general = (total_ii+
                         total_iii)
        return total_general

class actif_net(Variable):
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Actif net"
    definition_period = YEAR

    def formula(Firm, period):
        brut = Firm("actif_brut", period)
        ar = Firm("actif_ar", period)

        return brut - ar
