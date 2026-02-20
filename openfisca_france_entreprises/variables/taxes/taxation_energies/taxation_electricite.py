"""Variables and formulas for this module."""

from openfisca_core.model_api import YEAR, Variable, select, where

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import Etablissement
from openfisca_france_entreprises.variables.taxes.taxation_energies.formula_helpers import (
    _and,
    _or,
)


class taxe_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""

    def formula_2002_01_01(etablissement, period, parameters):
        return etablissement(
            "taxe_contribution_service_public_electricite",
            period,
        )

    def formula_2011_01_01(etablissement, period, parameters):
        taxe_interieure_sur_consommation_finale_electricite = etablissement(
            "taxe_interieure_sur_consommation_finale_electricite",
            period,
        )
        taxe_communale_consommation_finale_electricite = etablissement(
            "taxe_communale_consommation_finale_electricite",
            period,
        )
        taxe_departementale_consommation_finale_electricite = etablissement(
            "taxe_departementale_consommation_finale_electricite",
            period,
        )
        # on a pas de données pour les tdcfe et tccfe avant 2011
        taxe_contribution_service_public_electricite = etablissement(
            "taxe_contribution_service_public_electricite",
            period,
        )
        # la cspe est mis en compte pour la totale jusqu'à 2015 (inclus)

        return (
            taxe_contribution_service_public_electricite
            + taxe_interieure_sur_consommation_finale_electricite
            + taxe_communale_consommation_finale_electricite
            + taxe_departementale_consommation_finale_electricite
        )

    def formula_2016_01_01(etablissement, period, parameters):
        # la cspe n'existait plus dès cette année
        #
        # tendance
        taxe_interieure_sur_consommation_finale_electricite = etablissement(
            "taxe_interieure_sur_consommation_finale_electricite",
            period,
        )
        taxe_communale_consommation_finale_electricite = etablissement(
            "taxe_communale_consommation_finale_electricite",
            period,
        )
        taxe_departementale_consommation_finale_electricite = etablissement(
            "taxe_departementale_consommation_finale_electricite",
            period,
        )

        return (
            taxe_interieure_sur_consommation_finale_electricite
            + taxe_communale_consommation_finale_electricite
            + taxe_departementale_consommation_finale_electricite
        )

    def formula_2022_01_01(etablissement, period, parameters):
        # en 2022, la tdcfe est intégrée dans l'accise, un ans avant ça n'arrive à la tccfe
        # mais exceptionellement, on a le bouclier tarifaire qui remplace le rôle de l'accise
        # due au fait que les montants sont calculés en unité des années, on divise le grand montant par 12
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        taxe_electricite_bouclier_tarifaire = etablissement(
            "taxe_electricite_bouclier_tarifaire",
            period,
        )
        taxe_communale_consommation_finale_electricite = etablissement(
            "taxe_communale_consommation_finale_electricite",
            period,
        )
        total_positive = (
            taxe_accise_electricite / 12
            + taxe_electricite_bouclier_tarifaire * 11 / 12
            + taxe_communale_consommation_finale_electricite
        )
        return where(
            taxe_accise_electricite == 0,
            taxe_communale_consommation_finale_electricite,
            total_positive,
        )

    def formula_2023_01_01(etablissement, period, parameters):
        #
        # en
        # en 2022, la tdcfe est intégrée dans l'accise, un an avant ça n'arrive à la tccfe
        # mais exceptionellement, on a le bouclier tarifaire qui remplace le rôle de l'accise
        # due au fait que les montants sont calculés en unité des années, on divise le grand montant par 12
        taxe_electricite_bouclier_tarifaire = etablissement(
            "taxe_electricite_bouclier_tarifaire",
            period,
        )  # 2024-02-01
        taxe_communale_consommation_finale_electricite = etablissement(
            "taxe_communale_consommation_finale_electricite",
            period,
        )
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        total_zero = taxe_communale_consommation_finale_electricite / 12  # pour janvier
        total_positive = (
            taxe_electricite_bouclier_tarifaire + taxe_communale_consommation_finale_electricite / 12
        )  # pour janvier
        return where(taxe_accise_electricite == 0, total_zero, total_positive)

    def formula_2024_01_01(etablissement, period, parameters):
        #
        # -
        taxe_electricite_bouclier_tarifaire = etablissement(
            "taxe_electricite_bouclier_tarifaire",
            period,
        )
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)

        return where(taxe_accise_electricite == 0, 0, taxe_electricite_bouclier_tarifaire)

    def formula_2025_01_01(etablissement, period, parameters):
        #
        # -
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        taxe_electricite_bouclier_tarifaire = etablissement(
            "taxe_electricite_bouclier_tarifaire",
            period,
        )

        total_positive = (
            taxe_accise_electricite * 11 / 12 + taxe_electricite_bouclier_tarifaire / 12
        )  # que pour janvier
        return where(taxe_accise_electricite == 0, 0, total_positive)


class taxe_contribution_service_public_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Contribution au Servie Public de l'Électricité"
    reference = ""

    def formula_2002_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        return assiette_taxe_electricite * parameters(period).energies.electricite.cspe

    # condition d'application est pareil jusqu'à 2011


class taxe_interieure_sur_consommation_finale_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""

    def formula_2011_01_01(etablissement, period, parameters):
        """https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=1.-,Il%20est%20institu%C3%A9,-une%20taxe%20int%C3%A9rieure."""
        electricite_production_a_bord = etablissement(
            "electricite_production_a_bord",
            period,
        )
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement(
            "electricite_transport_guide",
            period,
        )
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement(
            "electricite_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        electricite_production_biens_electro_intensive = etablissement(
            "electricite_production_biens_electro_intensive",
            period,
        )
        electricite_production_electricite = etablissement(
            "electricite_production_electricite",
            period,
        )
        installation_grande_consommatrice_energie = etablissement(
            "installation_grande_consommatrice_energie",
            period,
        )

        amperage = etablissement("amperage", period)

        condition_amperage = _and(
            amperage != 0,
            amperage
            <= parameters(
                period,
            ).energies.electricite.ticfe.categorie_fiscale_haut_puissance,
        )
        condition_exoneration = _or(
            electricite_double_usage,
            electricite_fabrication_produits_mineraux_non_metalliques,
            electricite_production_biens_electro_intensive,
            electricite_production_a_bord,
            electricite_production_electricite,
            electricite_transport_guide,
            installation_grande_consommatrice_energie,
        )
        return select(
            [condition_amperage, condition_exoneration],
            [0, 0],
            default=etablissement("taxe_accise_electricite_taux_normal", period),
        )

    def formula_2016_01_01(etablissement, period, parameters):
        """https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=1.-,Il%20est%20institu%C3%A9,-une%20taxe%20int%C3%A9rieure."""
        electricite_production_a_bord = etablissement(
            "electricite_production_a_bord",
            period,
        )
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement(
            "electricite_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        electricite_production_biens_electro_intensive = etablissement(
            "electricite_production_biens_electro_intensive",
            period,
        )
        electricite_production_electricite = etablissement(
            "electricite_production_electricite",
            period,
        )
        electricite_installations_industrielles_electro_intensives = etablissement(
            "electricite_installations_industrielles_electro_intensives",
            period,
        )
        electricite_installations_industrielles_hyper_electro_intensives = etablissement(
            "electricite_installations_industrielles_hyper_electro_intensives",
            period,
        )
        electricite_transport_guide = etablissement(
            "electricite_transport_guide",
            period,
        )
        risque_de_fuite_carbone_eta = etablissement(
            "risque_de_fuite_carbone_eta",
            period,
        )

        condition_exoneration = _or(
            electricite_double_usage,
            electricite_fabrication_produits_mineraux_non_metalliques,
            electricite_production_biens_electro_intensive,
            electricite_production_a_bord,
            electricite_production_electricite,
        )
        return select(
            [
                condition_exoneration,
                electricite_installations_industrielles_hyper_electro_intensives != 0,
                electricite_installations_industrielles_electro_intensives != 0,
                electricite_transport_guide != 0,
                risque_de_fuite_carbone_eta != 0,
            ],
            [
                0,
                etablissement(
                    "taxe_electricite_installations_industrielles_hyper_electro_intensives",
                    period,
                ),
                etablissement(
                    "taxe_electricite_installations_industrielles_electro_intensives",
                    period,
                ),
                etablissement("taxe_electricite_transport_guide", period),
                etablissement("taxe_electricite_risque_de_fuite_de_carbone", period),
            ],
            default=etablissement("taxe_accise_electricite_taux_normal", period),
        )

    def formula_2019_01_01(etablissement, period, parameters):
        """https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=1.-,Il%20est%20institu%C3%A9,-une%20taxe%20int%C3%A9rieure."""
        electricite_production_a_bord = etablissement(
            "electricite_production_a_bord",
            period,
        )
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement(
            "electricite_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        electricite_production_biens_electro_intensive = etablissement(
            "electricite_production_biens_electro_intensive",
            period,
        )
        electricite_production_electricite = etablissement(
            "electricite_production_electricite",
            period,
        )
        electricite_installations_industrielles_electro_intensives = etablissement(
            "electricite_installations_industrielles_electro_intensives",
            period,
        )
        electricite_installations_industrielles_hyper_electro_intensives = etablissement(
            "electricite_installations_industrielles_hyper_electro_intensives",
            period,
        )
        electricite_transport_guide = etablissement(
            "electricite_transport_guide",
            period,
        )
        risque_de_fuite_carbone_eta = etablissement(
            "risque_de_fuite_carbone_eta",
            period,
        )
        electricite_centres_de_stockage_donnees = etablissement(
            "electricite_centres_de_stockage_donnees",
            period,
        )
        electricite_exploitation_aerodrome = etablissement(
            "electricite_exploitation_aerodrome",
            period,
        )

        condition_exoneration = _or(
            electricite_double_usage,
            electricite_fabrication_produits_mineraux_non_metalliques,
            electricite_production_biens_electro_intensive,
            electricite_production_a_bord,
            electricite_production_electricite,
        )
        return select(
            [
                condition_exoneration,
                electricite_installations_industrielles_hyper_electro_intensives != 0,
                electricite_installations_industrielles_electro_intensives != 0,
                electricite_transport_guide != 0,
                risque_de_fuite_carbone_eta != 0,
                electricite_centres_de_stockage_donnees != 0,
                electricite_exploitation_aerodrome != 0,
            ],
            [
                0,
                etablissement(
                    "taxe_electricite_installations_industrielles_hyper_electro_intensives",
                    period,
                ),
                etablissement(
                    "taxe_electricite_installations_industrielles_electro_intensives",
                    period,
                ),
                etablissement("taxe_electricite_transport_guide", period),
                etablissement("taxe_electricite_risque_de_fuite_de_carbone", period),
                etablissement("taxe_electricite_centres_de_stockage_donnees", period),
                etablissement("taxe_electricite_exploitation_aerodrome", period),
            ],
            default=etablissement("taxe_accise_electricite_taux_normal", period),
        )


# taxe_accise_electricite
#
# Public
class taxe_accise_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""

    # aussi ticfe selon la période
    def formula_2022_01_01(etablissement, period, parameters):
        """à partir de maintenant, c'est l'accise."""
        # voici les conditions à appliquer
        electro_intensive_activite_industrielle = etablissement(
            "electro_intensive_activite_industrielle",
            period,
        )
        electro_intensive_concurrence_internationale = etablissement(
            "electro_intensive_concurrence_internationale",
            period,
        )
        electricite_centres_de_stockage_donnees = etablissement(
            "electricite_centres_de_stockage_donnees",
            period,
        )
        electricite_transport_collectif_personnes = etablissement(
            "electricite_transport_collectif_personnes",
            period,
        )
        electricite_exploitation_aerodrome = etablissement(
            "electricite_exploitation_aerodrome",
            period,
        )
        electricite_production_a_bord = etablissement(
            "electricite_production_a_bord",
            period,
        )
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement(
            "electricite_transport_guide",
            period,
        )
        electricite_alimentation_a_quai = etablissement(
            "electricite_alimentation_a_quai",
            period,
        )
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement(
            "electricite_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        electricite_production_biens_electro_intensive = etablissement(
            "electricite_production_biens_electro_intensive",
            period,
        )
        electro_intensite = etablissement("electro_intensite", period)
        electricite_production_electricite = etablissement(
            "electricite_production_electricite",
            period,
        )

        condition_exoneration = _or(
            electricite_production_a_bord,
            electricite_double_usage,
            electricite_fabrication_produits_mineraux_non_metalliques,
            electricite_production_biens_electro_intensive,
            electricite_production_electricite,
        )
        condition_aerodrome = _and(
            electricite_exploitation_aerodrome,
            electro_intensite
            > parameters(
                period,
            ).energies.electricite.ticfe.aerodromes_electro_intensite,
        )
        return select(
            [
                condition_exoneration,
                electricite_transport_guide != 0,
                electricite_transport_collectif_personnes != 0,
                electricite_alimentation_a_quai != 0,
                electro_intensive_concurrence_internationale != 0,
                electro_intensive_activite_industrielle != 0,
                condition_aerodrome,
                electricite_centres_de_stockage_donnees != 0,
            ],
            [
                0,
                etablissement("taxe_electricite_transport_guide", period),
                etablissement("taxe_electricite_transport_collectif_personnes", period),
                etablissement("taxe_electricite_alimentation_a_quai", period),
                etablissement(
                    "taxe_accise_electricite_electro_intensive_concurrence_internationale",
                    period,
                ),
                etablissement(
                    "taxe_accise_electricite_electro_intensive_activite_industrielle",
                    period,
                ),
                etablissement("taxe_electricite_exploitation_aerodrome", period),
                etablissement("taxe_electricite_centres_de_stockage_donnees", period),
            ],
            default=etablissement("taxe_accise_electricite_taux_normal", period),
        )

    def formula_2023_01_01(etablissement, period, parameters):
        """Par rapport à précedement, ajouté manutention_portuaire, réf : L312-48."""
        # voici les conditions à appliquer
        electro_intensive_activite_industrielle = etablissement(
            "electro_intensive_activite_industrielle",
            period,
        )
        electro_intensive_concurrence_internationale = etablissement(
            "electro_intensive_concurrence_internationale",
            period,
        )
        electricite_centres_de_stockage_donnees = etablissement(
            "electricite_centres_de_stockage_donnees",
            period,
        )
        electricite_transport_collectif_personnes = etablissement(
            "electricite_transport_collectif_personnes",
            period,
        )
        electricite_manutention_portuaire = etablissement(
            "electricite_manutention_portuaire",
            period,
        )
        electricite_exploitation_aerodrome = etablissement(
            "electricite_exploitation_aerodrome",
            period,
        )
        electricite_production_a_bord = etablissement(
            "electricite_production_a_bord",
            period,
        )
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement(
            "electricite_transport_guide",
            period,
        )
        electricite_alimentation_a_quai = etablissement(
            "electricite_alimentation_a_quai",
            period,
        )
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement(
            "electricite_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        electricite_production_biens_electro_intensive = etablissement(
            "electricite_production_biens_electro_intensive",
            period,
        )
        electricite_production_electricite = etablissement(
            "electricite_production_electricite",
            period,
        )

        condition_exoneration = _or(
            electricite_production_a_bord,
            electricite_double_usage,
            electricite_fabrication_produits_mineraux_non_metalliques,
            electricite_production_biens_electro_intensive,
            electricite_production_electricite,
        )
        return select(
            [
                condition_exoneration,
                electricite_transport_guide != 0,
                electricite_transport_collectif_personnes != 0,
                electricite_manutention_portuaire != 0,
                electricite_alimentation_a_quai != 0,
                electro_intensive_concurrence_internationale != 0,
                electro_intensive_activite_industrielle != 0,
                electricite_exploitation_aerodrome != 0,
                electricite_centres_de_stockage_donnees != 0,
            ],
            [
                0,
                etablissement("taxe_electricite_transport_guide", period),
                etablissement("taxe_electricite_transport_collectif_personnes", period),
                etablissement("taxe_electricite_manutention_portuaire", period),
                etablissement("taxe_electricite_alimentation_a_quai", period),
                etablissement(
                    "taxe_accise_electricite_electro_intensive_concurrence_internationale",
                    period,
                ),
                etablissement(
                    "taxe_accise_electricite_electro_intensive_activite_industrielle",
                    period,
                ),
                etablissement("taxe_electricite_exploitation_aerodrome", period),
                etablissement("taxe_electricite_centres_de_stockage_donnees", period),
            ],
            default=etablissement("taxe_accise_electricite_taux_normal", period),
        )

    def formula_2025_01_01(etablissement, period, parameters):
        """Par rapport à précedement, ajouté.

        consommation_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques et
        consommation_alimentation_aeronefs_stationnement_aerodromes_activites_economiques.
        """
        # voici les conditions à appliquer
        electro_intensive_activite_industrielle = etablissement(
            "electro_intensive_activite_industrielle",
            period,
        )
        electro_intensive_concurrence_internationale = etablissement(
            "electro_intensive_concurrence_internationale",
            period,
        )
        electricite_centres_de_stockage_donnees = etablissement(
            "electricite_centres_de_stockage_donnees",
            period,
        )
        electricite_transport_collectif_personnes = etablissement(
            "electricite_transport_collectif_personnes",
            period,
        )
        electricite_manutention_portuaire = etablissement(
            "electricite_manutention_portuaire",
            period,
        )
        electricite_exploitation_aerodrome = etablissement(
            "electricite_exploitation_aerodrome",
            period,
        )
        electricite_production_a_bord = etablissement(
            "electricite_production_a_bord",
            period,
        )
        electricite_double_usage = etablissement("electricite_double_usage", period)
        electricite_transport_guide = etablissement(
            "electricite_transport_guide",
            period,
        )
        electricite_alimentation_a_quai = etablissement(
            "electricite_alimentation_a_quai",
            period,
        )
        electricite_fabrication_produits_mineraux_non_metalliques = etablissement(
            "electricite_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        electricite_production_biens_electro_intensive = etablissement(
            "electricite_production_biens_electro_intensive",
            period,
        )
        electricite_production_electricite = etablissement(
            "electricite_production_electricite",
            period,
        )
        electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques = etablissement(
            "electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques",
            period,
        )
        electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques = etablissement(
            "electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques",
            period,
        )

        condition_exoneration = _or(
            electricite_production_a_bord,
            electricite_double_usage,
            electricite_fabrication_produits_mineraux_non_metalliques,
            electricite_production_biens_electro_intensive,
            electricite_production_electricite,
        )
        return select(
            [
                condition_exoneration,
                electricite_transport_guide != 0,
                electricite_transport_collectif_personnes != 0,
                electricite_manutention_portuaire != 0,
                electricite_alimentation_a_quai != 0,
                electro_intensive_concurrence_internationale != 0,
                electro_intensive_activite_industrielle != 0,
                electricite_exploitation_aerodrome != 0,
                electricite_centres_de_stockage_donnees != 0,
                electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques != 0,
                electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques != 0,
            ],
            [
                0,
                etablissement("taxe_electricite_transport_guide", period),
                etablissement("taxe_electricite_transport_collectif_personnes", period),
                etablissement("taxe_electricite_manutention_portuaire", period),
                etablissement("taxe_electricite_alimentation_a_quai", period),
                etablissement(
                    "taxe_accise_electricite_electro_intensive_concurrence_internationale",
                    period,
                ),
                etablissement(
                    "taxe_accise_electricite_electro_intensive_activite_industrielle",
                    period,
                ),
                etablissement("taxe_electricite_exploitation_aerodrome", period),
                etablissement("taxe_electricite_centres_de_stockage_donnees", period),
                etablissement(
                    "taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques",
                    period,
                ),
                etablissement(
                    "taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques",
                    period,
                ),
            ],
            default=etablissement("taxe_accise_electricite_taux_normal", period),
        )


# class verifie_periode(Variable):
#     value_type = float
#     entity = Etablissement
#     definition_period = YEAR
#     def formula_2025_01_01(etablissement, period, parameters):
#
# parameters(period).energies.electricite.ticfe.alimentation_aeronefs_stationnement_aerodromes_activites_economiques

#         return taux


class taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques(
    Variable,
):
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2025_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        return (
            assiette_taxe_electricite
            * parameters(
                period,
            ).energies.electricite.ticfe.alimentation_aeronefs_stationnement_aerodromes_activites_economiques
        )


class taxe_electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques(
    Variable,
):
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2025_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        return (
            assiette_taxe_electricite
            * parameters(
                period,
            ).energies.electricite.ticfe.alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques
        )


class taxe_electricite_risque_de_fuite_de_carbone(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2016_01_01(etablissement, period, parameters):
        consommation_par_valeur_ajoutee = etablissement(
            "consommation_par_valeur_ajoutee",
            period,
        )
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        rfc = parameters(period).energies.electricite.ticfe.risque_de_fuite_de_carbone
        taxe_plus_3 = assiette_taxe_electricite * rfc.taux_plus_de_3kWh_par_valeur_ajoutee
        taxe_1_5_3 = assiette_taxe_electricite * rfc.taux_1_virgule_5_a_3kWh_par_valeur_ajoutee
        taxe_moins_1_5 = assiette_taxe_electricite * rfc.taux_moins_de_1_virgule_5kWh_par_valeur_ajoutee
        return select(
            [
                consommation_par_valeur_ajoutee >= rfc.seuil_3_kwh_par_va,
                consommation_par_valeur_ajoutee >= rfc.seuil_1_5_kwh_par_va,
            ],
            [taxe_plus_3, taxe_1_5_3],
            default=taxe_moins_1_5,
        )


class taxe_electricite_installations_industrielles_hyper_electro_intensives(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2016_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        return (
            assiette_taxe_electricite
            * parameters(
                period,
            ).energies.electricite.ticfe.electro_intensive.hyperelectro_intensive
        )


class taxe_electricite_installations_industrielles_electro_intensives(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2016_01_01(etablissement, period, parameters):
        consommation_par_valeur_ajoutee = etablissement(
            "consommation_par_valeur_ajoutee",
            period,
        )
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        ei = parameters(period).energies.electricite.ticfe.electro_intensive
        taxe_plus_3 = assiette_taxe_electricite * ei.taux_plus_de_3kWh_par_valeur_ajoutee
        taxe_1_5_3 = assiette_taxe_electricite * ei.taux_1_virgule_5_a_3kWh_par_valeur_ajoutee
        taxe_moins_1_5 = assiette_taxe_electricite * ei.taux_moins_de_1_virgule_5kWh_par_valeur_ajoutee
        return select(
            [
                consommation_par_valeur_ajoutee >= ei.seuil_3_kwh_par_va,
                consommation_par_valeur_ajoutee >= ei.seuil_1_5_kwh_par_va,
            ],
            [taxe_plus_3, taxe_1_5_3],
            default=taxe_moins_1_5,
        )


class taxe_electricite_alimentation_a_quai(Variable):
    # celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        taux = parameters(period).energies.electricite.ticfe.alimentation_a_quai
        return assiette_taxe_electricite * taux


class taxe_electricite_exploitation_aerodrome(Variable):
    # celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2019_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        taux = parameters(period).energies.electricite.ticfe.aerodromes
        return assiette_taxe_electricite * taux


class taxe_electricite_manutention_portuaire(Variable):
    # celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        taux = parameters(period).energies.electricite.ticfe.manutention_portuaire
        return assiette_taxe_electricite * taux


class taxe_electricite_transport_collectif_personnes(Variable):
    # celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        taux = parameters(
            period,
        ).energies.electricite.ticfe.transport_collectif_personnes
        return assiette_taxe_electricite * taux


class taxe_electricite_transport_guide(Variable):
    # celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2016_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        taux = parameters(period).energies.electricite.ticfe.transport_guide
        return assiette_taxe_electricite * taux


class taxe_electricite_centres_de_stockage_donnees(Variable):
    # celui-là est calculé dehors les autres aspects du tariff (soit niveau electricité intesif etc.)
    value_type = float
    entity = Etablissement
    definition_period = YEAR

    def formula_2019_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        ticfe = parameters(period).energies.electricite.ticfe
        plafond = ticfe.plafond_assiette_mwh
        taxe_above = (
            plafond * ticfe.taux_normal + (assiette_taxe_electricite - plafond) * ticfe.data_center
        )  # la portion qui dépasse un gigawatt
        taxe_below = assiette_taxe_electricite * ticfe.taux_normal
        return where(assiette_taxe_electricite > plafond, taxe_above, taxe_below)

    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        taux = parameters(period).energies.electricite.ticfe.data_center
        return assiette_taxe_electricite * taux


class taxe_accise_electricite_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-37"
    reference = (
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/"
        "LEGISCTA000044598327/#LEGISCTA000044603893:~:text=Les%20tarifs%20normaux%20"
        "de%20l%27accise%2C%20exprim%C3%A9s%20en%20euros%20par%20m%C3%A9gawattheure%2C%20"
        "sont%2C%20en%202015%2C%20pour%20chacune%20des%20cat%C3%A9gories%20fiscales%20"
        "de%20l%27%C3%A9lectricit%C3%A9%2C%20les%20suivants%20%3A"
    )

    def formula_2011_01_01(etablissement, period, parameters):
        """2011-01-01.

            value: 0.5
        2016-01-01:
            value: 22.5
        2022-01-01:
            value: 22.5.
        """
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)

        return assiette_taxe_electricite * parameters(period).energies.electricite.ticfe.taux_normal

    def formula_2021_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        consommation_electricite_fournie_aux_navires = etablissement(
            "consommation_electricite_fournie_aux_navires",
            period,
        )

        taxe_electricite_fournie_aux_navires = (
            consommation_electricite_fournie_aux_navires
            * parameters(
                period,
            ).energies.electricite.ticfe.electricite_fournie_aux_navires
        )

        reste = assiette_taxe_electricite - taxe_electricite_fournie_aux_navires

        taxe = reste * parameters(period).energies.electricite.ticfe.taux_normal

        return taxe + taxe_electricite_fournie_aux_navires

    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage != 0) & (amperage < ticfe.categorie_fiscale_petite_et_moyenne_entreprise)
        cond_250 = (
            (amperage != 0)
            & (amperage >= ticfe.categorie_fiscale_petite_et_moyenne_entreprise)
            & (amperage < ticfe.categorie_fiscale_haut_puissance)
        )
        taxe_36 = assiette_taxe_electricite * ticfe.taux_normal_36kVA_et_moins
        taxe_36_250 = assiette_taxe_electricite * ticfe.taux_normal_36_a_250kVA
        taxe_haut = assiette_taxe_electricite * ticfe.taux_normal  # > 250 kVA
        return select([cond_36, cond_250], [taxe_36, taxe_36_250], default=taxe_haut)


class taxe_accise_electricite_electro_intensive_activite_industrielle(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "sous L312-65"
    reference = ""

    def formula_2022_01_01(etablissement, period, parameters):
        electro_intensite = etablissement("electro_intensite", period)
        electro_intensive_activite_industrielle = etablissement(
            "electro_intensive_activite_industrielle",
            period,
        )
        seuils = parameters(period).energies.electricite.ticfe.electro_intensive.seuils

        assiette = etablissement("assiette_taxe_electricite", period)
        condition_05 = _and(
            electro_intensive_activite_industrielle,
            electro_intensite != 0,
            electro_intensite < seuils.electro_intensite_activite_industrielle_seuil_05,
        )
        condition_3375 = _and(
            electro_intensive_activite_industrielle,
            electro_intensite != 0,
            electro_intensite >= seuils.electro_intensite_activite_industrielle_seuil_05,
            electro_intensite < seuils.electro_intensite_tranche_1_max,
        )
        condition_675 = _and(
            electro_intensive_activite_industrielle,
            _or(
                electro_intensite == 0,
                electro_intensite >= seuils.electro_intensite_tranche_1_max,
            ),
        )
        return select(
            [condition_05, condition_3375, condition_675],
            [
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.activite_industrielle.electro_intensive_0_virgule_5,
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.activite_industrielle.electro_intensive_3_virgule_375,
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.activite_industrielle.electro_intensive_6_virgule_75,
            ],
            default=0,
        )


class taxe_accise_electricite_electro_intensive_concurrence_internationale(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-65"
    reference = ""

    def formula_2022_01_01(etablissement, period, parameters):
        electro_intensite = etablissement("electro_intensite", period)

        assiette = etablissement("assiette_taxe_electricite", period)
        risque_de_fuite_carbone_eta = etablissement(
            "risque_de_fuite_carbone_eta",
            period,
        )
        intensite_echanges_avec_pays_tiers = etablissement(
            "intensite_echanges_avec_pays_tiers",
            period,
        )
        electro_intensive_concurrence_internationale = etablissement(
            "electro_intensive_concurrence_internationale",
            period,
        )
        seuils = parameters(period).energies.electricite.ticfe.electro_intensive.seuils

        condition_13_5 = _and(
            electro_intensive_concurrence_internationale,
            electro_intensite > seuils.electro_intensite_tranche_3_max,
            risque_de_fuite_carbone_eta,
            intensite_echanges_avec_pays_tiers > seuils.intensite_echanges_pays_tiers_min,
        )
        condition_6_75 = _and(
            electro_intensive_concurrence_internationale,
            electro_intensite > seuils.electro_intensite_tranche_2_max,
            electro_intensite <= seuils.electro_intensite_tranche_3_max,
        )
        condition_3_375 = _and(
            electro_intensive_concurrence_internationale,
            electro_intensite > seuils.electro_intensite_tranche_1_max,
            electro_intensite <= seuils.electro_intensite_tranche_2_max,
        )
        condition_0_5 = _and(
            electro_intensive_concurrence_internationale,
            electro_intensite <= seuils.electro_intensite_tranche_1_max,
        )
        return select(
            [condition_13_5, condition_6_75, condition_3_375, condition_0_5],
            [
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_13_virgule_5,
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_6_virgule_75,
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_3_virgule_375,
                assiette
                * parameters(
                    period,
                ).energies.electricite.ticfe.electro_intensive.concurrence_internationale.electro_intensive_0_virgule_5,
            ],
            default=0,
        )


class assiette_taxe_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "assiette de la Taxe Intérieure sur la Consommation Finale d'Électricité"
    reference = ""

    def formula_2002_01_01(etablissement, period, parameters):
        # sous CPSE
        return etablissement("consommation_electricite", period)

    def formula_2011_01_01(etablissement, period, parameters):
        # sous TICFE, TCCFE, TDCFE
        consommation_electricite = etablissement("consommation_electricite", period)
        consommation_electricite_petite_producteur_electricite = etablissement(
            "consommation_electricite_petite_producteur_electricite",
            period,
        )
        consommation_electricite_auto_consommation = etablissement(
            "consommation_electricite_auto_consommation",
            period,
        )

        return consommation_electricite - (
            consommation_electricite_petite_producteur_electricite + consommation_electricite_auto_consommation
        )

    def formula_2017_01_01(etablissement, period, parameters):
        consommation_electricite = etablissement("consommation_electricite", period)
        consommation_electricite_petite_producteur_electricite = etablissement(
            "consommation_electricite_petite_producteur_electricite",
            period,
        )
        consommation_electricite_auto_consommation = etablissement(
            "consommation_electricite_auto_consommation",
            period,
        )
        consommation_electricite_puissance_moins_1_MW = etablissement(
            "consommation_electricite_puissance_moins_1_MW",
            period,
        )

        return consommation_electricite - (
            consommation_electricite_puissance_moins_1_MW
            + consommation_electricite_petite_producteur_electricite
            + consommation_electricite_auto_consommation
        )

    def formula_2022_01_01(etablissement, period, parameters):
        """https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635#:~:text=Rel%C3%A8ve%20d%27un%20tarif%20particulier%20de%20l%27accise."""
        consommation_electricite = etablissement("consommation_electricite", period)

        consommation_electricite_energie_ou_gaz_renouvelable = etablissement(
            "consommation_electricite_energie_ou_gaz_renouvelable",
            period,
        )
        consommation_electricite_puissance_moins_1_MW = etablissement(
            "consommation_electricite_puissance_moins_1_MW",
            period,
        )
        consommation_electricite_auto_consommation = etablissement(
            "consommation_electricite_auto_consommation",
            period,
        )

        return consommation_electricite - (
            consommation_electricite_energie_ou_gaz_renouvelable
            + consommation_electricite_puissance_moins_1_MW
            + consommation_electricite_auto_consommation
        )
