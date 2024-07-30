from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_entreprises.entities import UniteLegale, Etablissement  # noqa F401


class dotations_financieres_ar(Variable):
    cerfa_field = "GQ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Dotations financières aux amortissements et provisions"
    definition_period = YEAR


class interets_charges(Variable):
    cerfa_field = "GR"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Intérêts et charges assimilés"
    definition_period = YEAR


class differences_negatives_change(Variable):
    cerfa_field = "GS"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Différences négatives de change"
    definition_period = YEAR


class charges_nettes_cessions(Variable):
    cerfa_field = "GT"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Charges nettes sur cessions de valeurs mobilières de placement"
    definition_period = YEAR


class charges_financieres(Variable):
    cerfa_field = ""
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = ""
    definition_period = YEAR

    def formula(UniteLegale, period):
        dotations_financieres_ar = UniteLegale("dotations_financieres_ar", period)
        interets_charges = UniteLegale("interets_charges", period)
        differences_negatives_change = UniteLegale("differences_negatives_change", period)
        charges_nettes_cessions = UniteLegale("charges_nettes_cessions", period)

        charges = (dotations_financieres_ar + interets_charges + differences_negatives_change + charges_nettes_cessions)

        return charges
