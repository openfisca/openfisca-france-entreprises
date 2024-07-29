from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class charges_constatees_avance_brutes(Variable):
    cerfa_field = "CH"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges constatées d'avance brutes"
    definition_period = YEAR

class charges_constatees_avance_ar(Variable):
    cerfa_field = "CI"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges constatées d'avance : amortissements, provisions"
    definition_period = YEAR

class charges_constatees_avance_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges constatées d'avance nettes"
    definition_period = YEAR

    def formula(Firm, period):
        brut = Firm("charges_constatees_avance_brutes", period)
        ar = Firm("charges_constatees_avance_ar", period)

        return brut - ar

class actif_total_iii_brut(Variable):
    cerfa_field = "CJ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Total (III) brut"
    definition_period = YEAR

    def formula(Firm, period):

        actif_circulant = Firm("actif_circulant_brut", period)
        charges_constatees_avance = Firm("charges_constatees_avance_brutes", period)
        total = actif_circulant + charges_constatees_avance

        return total

class actif_total_iii_ar(Variable):
    cerfa_field = "CK"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Total (III) : amortissements, provisions"
    definition_period = YEAR

    def formula(Firm, period):
        actif_circulant = Firm("actif_circulant_ar", period)
        charges_constatees_avance = Firm("charges_constatees_avance_ar", period)
        total = actif_circulant + charges_constatees_avance

        return total

class actif_total_iii_net(Variable):
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Total (III) net"
    definition_period = YEAR

    def formula(Firm, period):
        brut = Firm("actif_total_iii_brut", period)
        ar = Firm("actif_total_iii_ar", period)

        return brut - ar

class frais_emission_emprunt(Variable):
    cerfa_field = "CW"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Frais d'émission d'emprunt à étaler (IV)"
    definition_period = YEAR

class primes_remboursement_obligations(Variable):
    cerfa_field = "CM"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Primes de remboursement des obligations (V)"
    definition_period = YEAR

class ecarts_conversion_actif(Variable):
    cerfa_field = "CN"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Ecarts de conversion actif (VI)"
    definition_period = YEAR
