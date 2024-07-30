from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_firms.entities import UniteLegale  # noqa F401


class passif_total_iv(Variable):
    cerfa_field = "EC"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Total (IV)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        dettes = UniteLegale("dettes", period)
        produits_constates_avance = UniteLegale("produits_constates_avance", period)

        passif_total_iv = (dettes + produits_constates_avance)

        return passif_total_iv


class ecart_conversion_passif(Variable):
    cerfa_field = "ED"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Ecart de conversion passif (Total IV)"
    definition_period = YEAR


class passif(Variable):
    cerfa_field = "EE"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Passif"
    definition_period = YEAR

    def formula(UniteLegale, period):
        total_i = UniteLegale("capitaux_propres", period)
        total_ii = UniteLegale("autres_fonds_propres", period)
        total_iii = UniteLegale("provisions_pour_risques_charges", period)
        total_iv = UniteLegale("passif_total_iv", period)
        total_v = UniteLegale("ecart_conversion_passif", period)

        passif = (total_i + total_ii + total_iii + total_iv + total_v)

        return passif
