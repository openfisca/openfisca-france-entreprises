"""This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import YEAR, Variable, select
from openfisca_core.periods import Instant

from openfisca_france_entreprises.entities import Etablissement
from openfisca_france_entreprises.variables.taxes.taxation_energies.formula_helpers import (
    _and,
    _not,
    _or,
)


class taxe_interieure_consommation_charbon(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Taxe intérieure de consommation sur les houilles, lignites et cokes - TICC"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"

    def formula_2007_01_01(etablissement, period, parameters):
        """Taxe sur la consommation de houilles, lignites, et cokes."""
        assiette_ticc = etablissement("assiette_ticc", period)
        return assiette_ticc * parameters(period).energies.charbon.ticc

    def formula_2008_01_01(etablissement, period, parameters):
        # (2008) Par rapport à precedement: ajout conso_combustible_biomasse, seqe
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        # les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)
        seqe = etablissement("installation_seqe", period)

        condition_exoneration = _and(seqe, charbon_biomasse)
        return select(
            [condition_exoneration],
            [0],
            default=etablissement(
                "taxe_interieure_taxation_consommation_charbon_taux_normal",
                period,
            ),
        )

    def formula_2009_01_01(etablissement, period, parameters):
        # (2009) par rapport à précedement, ajout condition_facture
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        # les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)

        installation_grande_consommatrice_energie = etablissement(
            "installation_grande_consommatrice_energie",
            period,
        )  # grandes consommatrices d'énergie soumises à quota CO₂

        condition_exoneration = _and(
            installation_grande_consommatrice_energie,
            charbon_biomasse,
        )
        return select(
            [condition_exoneration],
            [0],
            default=etablissement(
                "taxe_interieure_taxation_consommation_charbon_taux_normal",
                period,
            ),
        )

    def formula_2022_01_01(etablissement, period, parameters):
        #
        # charbon_navigation_aerienne,
        # de

        # les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)
        installation_seqe = etablissement("installation_seqe", period)
        risque_de_fuite_carbone_eta = etablissement(
            "risque_de_fuite_carbone_eta",
            period,
        )
        intensite_energetique_valeur_production = etablissement(
            "intensite_energetique_valeur_production",
            period,
        )
        intensite_energetique_valeur_ajoutee = etablissement(
            "intensite_energetique_valeur_ajoutee",
            period,
        )

        # les suivant permettent une excemption de la taxe
        charbon_navigation_interieure = etablissement(
            "charbon_navigation_interieure",
            period,
        )
        charbon_navigation_maritime = etablissement(
            "charbon_navigation_maritime",
            period,
        )
        charbon_navigation_aerienne = etablissement(
            "charbon_navigation_aerienne",
            period,
        )
        charbon_fabrication_produits_mineraux_non_metalliques = etablissement(
            "charbon_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        charbon_secteurs_aeronautique_et_naval = etablissement(
            "charbon_secteurs_aeronautique_et_naval",
            period,
        )
        charbon_double_usage = etablissement("charbon_double_usage", period)

        # Exonération : seqe + biomasse + seuil production, ou l'une des navigations / double usage
        seuils = parameters(period).energies.seuils_seqe
        condition_exoneration = _or(
            _and(
                installation_seqe,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
                charbon_biomasse,
            ),
            charbon_navigation_interieure,
            charbon_navigation_maritime,
            charbon_navigation_aerienne,
            charbon_fabrication_produits_mineraux_non_metalliques,
            charbon_secteurs_aeronautique_et_naval,
            charbon_double_usage,
        )
        # Taux SEGE
        condition_seqe = _or(
            _and(
                installation_seqe,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
            ),
            _and(
                installation_seqe,
                intensite_energetique_valeur_ajoutee >= seuils.intensite_valeur_ajoutee_min,
            ),
        )
        # Concurrence internationale (ça n'existe plus dès 2024)
        condition_concurrence = _or(
            _and(
                _not(installation_seqe),
                risque_de_fuite_carbone_eta,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
            ),
            _and(
                _not(installation_seqe),
                risque_de_fuite_carbone_eta,
                intensite_energetique_valeur_ajoutee >= seuils.intensite_valeur_ajoutee_min,
            ),
        )

        return select(
            [condition_exoneration, condition_seqe, condition_concurrence],
            [
                0,
                etablissement(
                    "taxe_interieure_taxation_consommation_charbon_seqe",
                    period,
                ),
                etablissement(
                    "taxe_interieure_taxation_consommation_charbon_concurrence_internationale",
                    period,
                ),
            ],
            default=etablissement(
                "taxe_interieure_taxation_consommation_charbon_taux_normal",
                period,
            ),
        )

    def formula_2024_01_01(etablissement, period, parameters):
        seuils = parameters(period).energies.seuils_seqe
        # les suivants sont liés à charbon_biomasse comme conditions d'application
        charbon_biomasse = etablissement("charbon_biomasse", period)
        installation_seqe = etablissement("installation_seqe", period)

        intensite_energetique_valeur_production = etablissement(
            "intensite_energetique_valeur_production",
            period,
        )
        intensite_energetique_valeur_ajoutee = etablissement(
            "intensite_energetique_valeur_ajoutee",
            period,
        )

        # les suivant permettent une excemption de la taxe
        charbon_navigation_interieure = etablissement(
            "charbon_navigation_interieure",
            period,
        )
        charbon_navigation_maritime = etablissement(
            "charbon_navigation_maritime",
            period,
        )
        charbon_navigation_aerienne = etablissement(
            "charbon_navigation_aerienne",
            period,
        )
        charbon_fabrication_produits_mineraux_non_metalliques = etablissement(
            "charbon_fabrication_produits_mineraux_non_metalliques",
            period,
        )
        charbon_secteurs_aeronautique_et_naval = etablissement(
            "charbon_secteurs_aeronautique_et_naval",
            period,
        )
        charbon_double_usage = etablissement("charbon_double_usage", period)

        condition_exoneration = _or(
            _and(
                installation_seqe,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
                charbon_biomasse,
            ),
            charbon_navigation_interieure,
            charbon_navigation_maritime,
            charbon_navigation_aerienne,
            charbon_fabrication_produits_mineraux_non_metalliques,
            charbon_secteurs_aeronautique_et_naval,
            charbon_double_usage,
        )
        condition_seqe = _or(
            _and(
                installation_seqe,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
            ),
            _and(
                installation_seqe,
                intensite_energetique_valeur_ajoutee >= seuils.intensite_valeur_ajoutee_min,
            ),
        )

        return select(
            [condition_exoneration, condition_seqe],
            [
                0,
                etablissement(
                    "taxe_interieure_taxation_consommation_charbon_seqe",
                    period,
                ),
            ],
            default=etablissement(
                "taxe_interieure_taxation_consommation_charbon_taux_normal",
                period,
            ),
        )


class taxe_interieure_taxation_consommation_charbon_concurrence_internationale(
    Variable,
):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75"
    reference = ""

    def formula_2007_01_01(etablissement, period, parameters):
        # faut changer la date après
        assiette_ticc = etablissement("assiette_ticc", period)
        return assiette_ticc * parameters(period).energies.charbon.taux_reduit_concurrence_internationale


class taxe_interieure_taxation_consommation_charbon_seqe(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75"
    reference = ""

    def formula_2007_01_01(etablissement, period, parameters):
        # faut changer la date après
        assiette_ticc = etablissement("assiette_ticc", period)
        return assiette_ticc * parameters(period).energies.charbon.taux_reduit_seqe


class taxe_interieure_taxation_consommation_charbon_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-65"
    reference = ""

    def formula_2007_01_01(etablissement, period, parameters):
        # faut changer la date après
        assiette_ticc = etablissement("assiette_ticc", period)
        return assiette_ticc * parameters(period).energies.charbon.ticc


class assiette_ticc(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Coal consumption taxable according to TICC"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"

    def formula_2007_01_01(etablissement, period, parameters):
        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement(
            "consommation_autres_produits_energetique_ticc",
            period,
        )

        # ces cinq sont à exclure de l'assiette
        consommation_charbon_combustible_interne = etablissement(
            "consommation_charbon_combustible_interne",
            period,
        )
        consommation_charbon_combustible_extraction = etablissement(
            "consommation_charbon_combustible_extraction",
            period,
        )
        consommation_charbon_combustible_particuliers = etablissement(
            "consommation_charbon_combustible_particuliers",
            period,
        )
        consommation_charbon_combustible_electricite = etablissement(
            "consommation_charbon_combustible_electricite",
            period,
        )

        return (
            consommation_charbon
            + consommation_autres_produits_energetique_ticc
            - (
                consommation_charbon_combustible_interne
                + consommation_charbon_combustible_electricite
                + consommation_charbon_combustible_extraction
                + consommation_charbon_combustible_particuliers
            )
        )

    def formula_2011_01_01(etablissement, period, parameters):
        # par rapport à précedement, ajout consommation_charbon_combustible_electricite_petits_producteurs

        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement(
            "consommation_autres_produits_energetique_ticc",
            period,
        )

        # les quatres sont à exclure de l'assiette, également pour consommation_charbon_combustible_electricite
        consommation_charbon_combustible_interne = etablissement(
            "consommation_charbon_combustible_interne",
            period,
        )
        consommation_charbon_combustible_extraction = etablissement(
            "consommation_charbon_combustible_extraction",
            period,
        )
        consommation_charbon_combustible_particuliers = etablissement(
            "consommation_charbon_combustible_particuliers",
            period,
        )

        # la dernière est exclus de consommation_charbon_combustible_electricite
        consommation_charbon_combustible_electricite = etablissement(
            "consommation_charbon_combustible_electricite",
            period,
        )
        consommation_charbon_combustible_electricite_petits_producteurs = etablissement(
            "consommation_charbon_combustible_electricite_petits_producteurs",
            period,
        )

        return (
            consommation_charbon
            + consommation_autres_produits_energetique_ticc
            - (
                consommation_charbon_combustible_interne
                + (
                    consommation_charbon_combustible_electricite
                    - consommation_charbon_combustible_electricite_petits_producteurs
                )
                + consommation_charbon_combustible_extraction
                + consommation_charbon_combustible_particuliers
            )
        )

    def formula_2016_01_01(etablissement, period, parameters):
        # par rapport à précedement, supprimer consommation_charbon_combustible_particuliers
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement(
            "consommation_autres_produits_energetique_ticc",
            period,
        )

        # ces trois  sont à exclure de l'assiette, également pour consommation_charbon_combustible_electricite
        consommation_charbon_combustible_interne = etablissement(
            "consommation_charbon_combustible_interne",
            period,
        )
        consommation_charbon_combustible_extraction = etablissement(
            "consommation_charbon_combustible_extraction",
            period,
        )

        # consommation_charbon_combustible_electricite_petits_producteurs est exclus de l'éxoneration
        consommation_charbon_combustible_electricite = etablissement(
            "consommation_charbon_combustible_electricite",
            period,
        )
        consommation_charbon_combustible_electricite_petits_producteurs = etablissement(
            "consommation_charbon_combustible_electricite_petits_producteurs",
            period,
        )

        return (
            consommation_charbon
            + consommation_autres_produits_energetique_ticc
            - (
                consommation_charbon_combustible_interne
                + (
                    consommation_charbon_combustible_electricite
                    - consommation_charbon_combustible_electricite_petits_producteurs
                )
                + consommation_charbon_combustible_extraction
            )
        )

    def formula_2020_01_01(etablissement, period, parameters):
        # à partir de 2020, charbon utilisé comme carburant est prise en compte

        consommation_charbon = etablissement("consommation_charbon", period)
        consommation_autres_produits_energetique_ticc = etablissement(
            "consommation_autres_produits_energetique_ticc",
            period,
        )

        #
        # consommation_charbon_combustible_electricite
        consommation_charbon_combustible_interne = etablissement(
            "consommation_charbon_combustible_interne",
            period,
        )
        consommation_charbon_combustible_extraction = etablissement(
            "consommation_charbon_combustible_extraction",
            period,
        )

        #
        # consommation_charbon_combustible_electricite
        consommation_charbon_combustible_electricite = etablissement(
            "consommation_charbon_combustible_electricite",
            period,
        )
        consommation_charbon_combustible_electricite_petits_producteurs = etablissement(
            "consommation_charbon_combustible_electricite_petits_producteurs",
            period,
        )
        # NB : la définition des petits producteurs d'énergie change au 1er avril 2017

        return (
            consommation_charbon
            + consommation_autres_produits_energetique_ticc
            - (
                consommation_charbon_combustible_interne
                + (
                    consommation_charbon_combustible_electricite
                    - consommation_charbon_combustible_electricite_petits_producteurs
                )
                + consommation_charbon_combustible_extraction
            )
        )
        #
        # contrat_achat_electricite_314,

        #
        # consommation_charbon_combustible_interne
        # également pour le charbon
        # NB -34, chaleur >= carburant
        # ajouter un engin_non_routier (-35) ?


class instant_electrite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Coal consumption taxable according to TICC"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615177/2007-07-01/"

    def formula_2007_01_01(etablissement, period, parameters):
        return parameters(
            Instant((2023, 2, 1)),
        ).energies.bouclier_tarifaire.majoration_tccfe_maximum


# parameters(Instant((YYYY, MM, DD)))
