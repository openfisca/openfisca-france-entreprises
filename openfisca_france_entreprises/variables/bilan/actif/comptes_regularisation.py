"""Variables and formulas for this module."""

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import UniteLegale


class charges_constatees_avance_brutes(Variable):
    cerfa_field = "CH"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Charges constatées d'avance brutes"
    definition_period = YEAR


class charges_constatees_avance_ar(Variable):
    cerfa_field = "CI"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Charges constatées d'avance : amortissements, provisions"
    definition_period = YEAR


class charges_constatees_avance_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Charges constatées d'avance nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("charges_constatees_avance_brutes", period)
        ar = UniteLegale("charges_constatees_avance_ar", period)

        return brut - ar


class actif_total_iii_brut(Variable):
    cerfa_field = "CJ"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Total (III) brut"
    definition_period = YEAR

    def formula(UniteLegale, period):
        actif_circulant = UniteLegale("actif_circulant_brut", period)
        charges_constatees_avance = UniteLegale(
            "charges_constatees_avance_brutes",
            period,
        )
        return actif_circulant + charges_constatees_avance


class actif_total_iii_ar(Variable):
    cerfa_field = "CK"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Total (III) : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        actif_circulant = UniteLegale("actif_circulant_ar", period)
        charges_constatees_avance = UniteLegale("charges_constatees_avance_ar", period)
        return actif_circulant + charges_constatees_avance


class actif_total_iii_net(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Total (III) net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("actif_total_iii_brut", period)
        ar = UniteLegale("actif_total_iii_ar", period)

        return brut - ar


class frais_emission_emprunt(Variable):
    cerfa_field = "CW"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Frais d'émission d'emprunt à étaler (IV)"
    definition_period = YEAR


class primes_remboursement_obligations(Variable):
    cerfa_field = "CM"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Primes de remboursement des obligations (V)"
    definition_period = YEAR


class ecarts_conversion_actif(Variable):
    cerfa_field = "CN"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Ecarts de conversion actif (VI)"
    definition_period = YEAR
