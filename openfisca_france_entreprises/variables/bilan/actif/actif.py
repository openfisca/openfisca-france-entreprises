"""Variables and formulas for this module."""

from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import UniteLegale


class actif_brut(Variable):
    value_type = int
    # cerfa_field = "CO"
    unit = "currency"
    entity = UniteLegale
    label = "Actif brut (Total général I à VI)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        total_i = UniteLegale("capital_souscrit_non_appele_brut", period)
        total_ii = UniteLegale("actif_immobilise_brut", period)
        total_iii = UniteLegale("actif_total_iii_brut", period)
        total_iv = UniteLegale("frais_emission_emprunt", period)
        total_v = UniteLegale("primes_remboursement_obligations", period)
        total_vi = UniteLegale("ecarts_conversion_actif", period)
        return total_i + total_ii + total_iii + total_iv + total_v + total_vi


class actif_ar(Variable):
    cerfa_field = "1A"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = " : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        total_ii = UniteLegale("actif_immobilise_ar", period)
        total_iii = UniteLegale("actif_total_iii_ar", period)
        return total_ii + total_iii


class actif_net(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("actif_brut", period)
        ar = UniteLegale("actif_ar", period)

        return brut - ar
