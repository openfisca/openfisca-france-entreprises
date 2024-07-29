from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class passif_total_iv(Variable):
    cerfa_field = "EC"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Total (IV)"
    definition_period = YEAR

    def formula(Firm, period):
        dettes = Firm("dettes", period)
        produits_constates_avance = Firm("produits_constates_avance", period)

        passif_total_iv = (dettes+
                           produits_constates_avance)

        return passif_total_iv

class ecart_conversion_passif(Variable):
    cerfa_field = "ED"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Ecart de conversion passif (Total IV)"
    definition_period = YEAR

class passif(Variable):
    cerfa_field = "EE"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Passif"
    definition_period = YEAR

    def formula(Firm, period):
        total_i = Firm("capitaux_propres", period)
        total_ii = Firm("autres_fonds_propres", period)
        total_iii = Firm("provisions_pour_risques_charges", period)
        total_iv = Firm("passif_total_iv", period)
        total_v = Firm("ecart_conversion_passif", period)

        passif = (total_i +
                  total_ii +
                  total_iii +
                  total_iv +
                  total_v)        

        return passif
