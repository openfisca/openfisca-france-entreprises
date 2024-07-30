from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_firms.entities import UniteLegale, Etablissement  # noqa F401


class produits_participations(Variable):
    cerfa_field = "GJ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits financiers de participations"
    definition_period = YEAR


class produits_valeurs_mobilieres(Variable):
    cerfa_field = "GK"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits des autres valeurs mobilières et créances de l'actif immobilier"
    definition_period = YEAR


class autres_interets(Variable):
    cerfa_field = "GL"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres intérêts et produits assimilés"
    definition_period = YEAR


class reprises_provisions(Variable):
    cerfa_field = "GM"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Reprises sur provisions et transferts de charges"
    definition_period = YEAR


class differences_positives_change(Variable):
    cerfa_field = "GN"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Différences positives de change"
    definition_period = YEAR


class produits_nets_cessions(Variable):
    cerfa_field = "GO"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits nets sur cessions de valeurs mobilières de placement"
    definition_period = YEAR


class produits_financiers(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits nets sur cessions de valeurs mobilières de placement"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_participations = UniteLegale("produits_participations", period)
        produits_valeurs_mobilieres = UniteLegale("produits_valeurs_mobilieres", period)
        autres_interets = UniteLegale("autres_interets", period)
        reprises_provisions = UniteLegale("reprises_provisions", period)
        differences_positives_change = UniteLegale("differences_positives_change", period)
        produits_nets_cessions = UniteLegale("produits_nets_cessions", period)

        produits_financiers = (produits_participations + produits_valeurs_mobilieres + autres_interets + reprises_provisions + differences_positives_change + produits_nets_cessions)

        return produits_financiers
