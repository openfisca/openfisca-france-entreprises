from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm, Establishment  # noqa F401

class dotations_financieres_ar(Variable):
    cerfa_field = "GQ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dotations financières aux amortissements et provisions"
    definition_period = YEAR

class interets_charges(Variable):
    cerfa_field = "GR"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Intérêts et charges assimilés"
    definition_period = YEAR

class differences_negatives_change(Variable):
    cerfa_field = "GS"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Différences négatives de change"
    definition_period = YEAR

class charges_nettes_cessions(Variable):
    cerfa_field = "GT"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Charges nettes sur cessions de valeurs mobilières de placement"
    definition_period = YEAR

class charges_financieres(Variable):
    cerfa_field = ""
    value_type = int
    unit = 'currency'
    entity = Firm
    label = ""
    definition_period = YEAR

    def formula(Firm, period):
        dotations_financieres_ar = Firm("dotations_financieres_ar", period)
        interets_charges = Firm("interets_charges", period)
        differences_negatives_change = Firm("differences_negatives_change", period)
        charges_nettes_cessions = Firm("charges_nettes_cessions", period)

        charges = (
            dotations_financieres_ar +
            interets_charges +
            differences_negatives_change +
            charges_nettes_cessions
        )

        return charges
