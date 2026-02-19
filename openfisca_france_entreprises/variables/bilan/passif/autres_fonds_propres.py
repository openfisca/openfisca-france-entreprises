from openfisca_core.model_api import *
from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import UniteLegale  # noqa F401


class produit_emissions_titres_participatifs(Variable):
    cerfa_field = "DM"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produit des émissions de titres participatifs"
    definition_period = YEAR


class avances_conditionnees(Variable):
    cerfa_field = "DN"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Avances conditionnees"
    definition_period = YEAR


class autres_fonds_propres(Variable):
    cerfa_field = "DO"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Autres fonds propres (total II)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produit_emissions_titres_participatifs = UniteLegale(
            "produit_emissions_titres_participatifs", period
        )
        avances_conditionnees = UniteLegale("avances_conditionnees", period)

        autres_fonds_propres = (
            produit_emissions_titres_participatifs + avances_conditionnees
        )

        return autres_fonds_propres
