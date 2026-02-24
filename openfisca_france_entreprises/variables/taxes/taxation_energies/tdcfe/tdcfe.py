"""Variables and formulas for this module."""

from openfisca_core.model_api import YEAR, Variable, select

from openfisca_france_entreprises.entities import Etablissement


class taxe_departementale_consommation_finale_electricite(Variable):
    value_type = float
    entity = Etablissement
    label = ""
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        taux_tdcfe = etablissement("taux_tdcfe", period)
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        return assiette_taxe_electricite * taux_tdcfe


class taux_tdcfe(Variable):
    value_type = float
    entity = Etablissement
    label = ""
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        tcfe = parameters(period).energies.electricite.tcfe
        departement = etablissement("departement", period).astype(str)
        coeff = tcfe.tdcfe.coefficient[departement]
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = tcfe.taux_professionnel_36kVA_et_moins * coeff
        val_250 = tcfe.taux_professionnel_36_a_250kVA * coeff
        return select([cond_36, cond_250], [val_36, val_250], default=0)
