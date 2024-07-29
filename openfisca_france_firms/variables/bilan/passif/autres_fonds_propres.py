from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class produit_emissions_titres_participatifs(Variable):
    cerfa_field = "DM"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Produit des émissions de titres participatifs"
    definition_period = YEAR

class avances_conditionnees(Variable):
    cerfa_field = "DN"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Avances conditionnees"
    definition_period = YEAR

class autres_fonds_propres(Variable):
    cerfa_field = "DO"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Autres fonds propres (total II)"
    definition_period = YEAR

    def formula(Firm, period):
        produit_emissions_titres_participatifs = Firm("produit_emissions_titres_participatifs", period)
        avances_conditionnees = Firm("avances_conditionnees", period)

        autres_fonds_propres = (produit_emissions_titres_participatifs+
                                avances_conditionnees)

        return autres_fonds_propres
