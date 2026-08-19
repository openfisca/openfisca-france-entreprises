"""Variables and formulas for this module."""

from openfisca_core.model_api import ADD, YEAR, Variable, select

from openfisca_france_entreprises.entities import Etablissement
from openfisca_france_entreprises.variables.taxes.formula_helpers import (
    departement_commune,
)


class taxe_communale_consommation_finale_electricite(Variable):
    value_type = float
    entity = Etablissement
    label = ""
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        taux_tccfe = etablissement("taux_tccfe", period)
        # L'assiette est mensuelle depuis la bascule ; taux_tccfe reste annuel (coefficient
        # communal), la TCCFE garde donc son traitement annuel. Passer le taux au mois est un
        # chantier distinct — la TCCFE disparaît de toute façon dans l'accise au 2023-01-01.
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period, options=[ADD])
        # *** à vérifier que c'est la même assiette

        return assiette_taxe_electricite * taux_tccfe


class taux_tccfe(Variable):
    value_type = float
    entity = Etablissement
    label = ""
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        tcfe = parameters(period).energies.electricite.tcfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        key = departement_commune(etablissement, period)
        coeff = tcfe.tccfe.coefficient[key]
        val_36 = tcfe.tarif_professionnel_36kVA_et_moins * coeff
        val_250 = tcfe.tarif_professionnel_36_a_250kVA * coeff
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2023_01_01(etablissement, period, parameters):
        """La TCCFE est incorporée à l'accise sur l'électricité au 1er janvier 2023.

        Elle cesse d'être prélevée séparément : son produit est repris dans les tarifs normaux
        de l'accise, différenciés par catégorie fiscale de puissance. Le taux propre est donc nul.
        """
        return etablissement("assiette_taxe_electricite", period, options=[ADD]) * 0
