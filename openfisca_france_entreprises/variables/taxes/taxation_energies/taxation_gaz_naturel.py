"""This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html

Les commentaires avec *** indiquent qu'il y a des problèmes
"""

from openfisca_core.model_api import ADD, MONTH, YEAR, Variable, select, set_input_divide_by_period

from openfisca_france_entreprises.entities import Etablissement
from openfisca_france_entreprises.variables.taxes.formula_helpers import (
    _and,
    _not,
    _or,
    accise_annuelle,
    majoration_zni,
    tarif_avec_repli,
    tarif_moyen_annuel,
)


class taxe_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        return etablissement("taxe_interieure_consommation_gaz_naturel", period)

    def formula_2022_01_01(etablissement, period, parameters):
        return etablissement("taxe_accise_gaz_naturel", period)


class taxe_interieure_consommation_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        return etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)

    def formula_1993_01_01(etablissement, period, parameters):
        # ajouté gaz_matiere_premiere

        gaz_matiere_premiere = etablissement("gaz_matiere_premiere", period)
        return select(
            [gaz_matiere_premiere],
            [0],
            default=etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period),
        )

    def formula_2003_01_01(etablissement, period, parameters):
        # ajouté gaz_huiles_minerales

        gaz_huiles_minerales = etablissement("gaz_huiles_minerales", period)
        gaz_matiere_premiere = etablissement("gaz_matiere_premiere", period)
        condition_exoneration = _or(gaz_matiere_premiere, gaz_huiles_minerales)
        return select(
            [condition_exoneration],
            [0],
            default=etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period),
        )

    def formula_2008_01_01(etablissement, period, parameters):
        """ajouté.

            -gaz_production_mineraux_non_metalliques
            -gaz_extraction_production
            -gaz_double_usage.

        combiné
            -gaz_huiles_minerales
            -gaz_matiere_premiere
        en les transformant en
            -consommation_gaz_usage_non_combustible
            > supprimé
        pour conformant plus à la langage de la loi
        """
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)
        gaz_double_usage = etablissement("gaz_double_usage", period)

        condition_exoneration = _or(
            gaz_production_mineraux_non_metalliques,
            gaz_double_usage,
            gaz_extraction_production,
        )
        return select(
            [condition_exoneration],
            [0],
            default=etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period),
        )

    def formula_2014_01_01(etablissement, period, parameters):
        """ajouté.

        -installation_grande_consommatrice, qui est lié à une modification de taux, voir les paramètres pour plus d'info
        -les conditions qui elle sont liées.
        """
        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        taxe_interieure_consommation_gaz_naturel_taux_normal = etablissement(
            "taxe_interieure_consommation_gaz_naturel_taux_normal",
            period,
        )
        taxe_interieure_consommation_gaz_naturel_grande_consommatrice = etablissement(
            "taxe_interieure_consommation_gaz_naturel_grande_consommatrice",
            period,
        )

        gaz_double_usage = etablissement("gaz_double_usage", period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)

        condition_exoneration = _or(
            gaz_production_mineraux_non_metalliques,
            gaz_double_usage,
            gaz_extraction_production,
        )
        condition_grande_consommatrice = _and(seqe, grande_consommatrice)
        return select(
            [condition_exoneration, condition_grande_consommatrice],
            [0, taxe_interieure_consommation_gaz_naturel_grande_consommatrice],
            default=taxe_interieure_consommation_gaz_naturel_taux_normal,
        )

    def formula_2019_01_01(etablissement, period, parameters):
        """ajouté.

        -Le tarif de la taxe applicable au produit consommé pour déshydrater les légumes
        et plantes aromatiques, autres que les pommes de terres, les champignons et les
        truffes, par les entreprises pour lesquelles cette consommation est supérieure à
        800 wattheures par euro de valeur ajoutée, est fixé à 1,6 € par mégawattheure.
            calculer, creer une variable value_ajouté, et ensuit appelle la variable ici, si ça depasse le seuil.

        """
        gaz_double_usage = etablissement("gaz_double_usage", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)

        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        taxe_interieure_consommation_gaz_naturel_taux_normal = etablissement(
            "taxe_interieure_consommation_gaz_naturel_taux_normal",
            period,
        )
        taxe_interieure_consommation_gaz_naturel_grande_consommatrice = etablissement(
            "taxe_interieure_consommation_gaz_naturel_grande_consommatrice",
            period,
        )

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement(
            "gaz_dehydration_legumes_et_plantes_aromatiques",
            period,
        )

        consommation_par_valeur_ajoutee = etablissement("consommation_par_valeur_ajoutee", period)

        condition_exoneration = _or(
            gaz_double_usage,
            gaz_production_mineraux_non_metalliques,
            gaz_extraction_production,
        )
        condition_legumes = _and(
            gaz_dehydration_legumes_et_plantes_aromatiques,
            consommation_par_valeur_ajoutee >= parameters(period).energies.gaz_naturel.ticgn.seuil_conso_par_va_legumes,
        )  # 0,0008 MWh par Euro
        condition_grande_consommatrice = _and(seqe, grande_consommatrice)
        return select(
            [
                condition_exoneration,
                condition_legumes,
                condition_grande_consommatrice,
            ],
            [
                0,
                etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period),
                taxe_interieure_consommation_gaz_naturel_grande_consommatrice,
            ],
            default=taxe_interieure_consommation_gaz_naturel_taux_normal,
        )

    def formula_2020_01_01(etablissement, period, parameters):
        """ajouté.

        -gaz_travaux_agricoles_et_forestiers.
        """
        gaz_double_usage = etablissement("gaz_double_usage", period)
        gaz_travaux_agricoles_et_forestiers = etablissement("gaz_travaux_agricoles_et_forestiers", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)

        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        ticgn_normal = etablissement("taxe_interieure_consommation_gaz_naturel_taux_normal", period)
        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement(
            "gaz_dehydration_legumes_et_plantes_aromatiques",
            period,
        )
        consommation_par_valeur_ajoutee = etablissement("consommation_par_valeur_ajoutee", period)

        condition_exoneration = _or(
            gaz_double_usage,
            gaz_extraction_production,
            gaz_production_mineraux_non_metalliques,
            gaz_travaux_agricoles_et_forestiers,
        )
        condition_legumes = _and(
            gaz_dehydration_legumes_et_plantes_aromatiques,
            consommation_par_valeur_ajoutee >= parameters(period).energies.gaz_naturel.ticgn.seuil_conso_par_va_legumes,
        )  # 0.0008 MWh par Euro
        condition_grande_consommatrice = _and(seqe, grande_consommatrice)
        return select(
            [
                condition_exoneration,
                condition_legumes,
                condition_grande_consommatrice,
            ],
            [
                0,
                etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period),
                ticgn_grande_conso,
            ],
            default=ticgn_normal,
        )


class taxe_accise_gaz_naturel(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Pour combiner les gaz naturels combustible et carburant"
    reference = ""

    def formula_2022_01_01(etablissement, period, parameters):
        # faut changer la date après
        return etablissement("taxe_accise_gaz_naturel_combustible", period) + etablissement(
            "taxe_accise_gaz_naturel_carburant",
            period,
        )


class taxe_accise_gaz_naturel_combustible(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Pour combiner les gaz naturels combustible et carburant"
    reference = ""

    def formula_2022_01_01(etablissement, period, parameters):
        # faut changer la date après
        gaz_double_usage = etablissement("gaz_double_usage", period)
        gaz_travaux_agricoles_et_forestiers = etablissement("gaz_travaux_agricoles_et_forestiers", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        # consommation_gaz_usage_non_combustible n'existe pas : la classe est commentée dans
        # consommation_energie/gaz_naturel.py. On rétablit ici l'intention documentée en tête de
        # ce fichier — cette variable « combinait gaz_matiere_premiere et gaz_huiles_minerales »
        # (le gaz consommé autrement que comme combustible, exonéré).
        gaz_usage_non_combustible = _or(
            etablissement("gaz_matiere_premiere", period),
            etablissement("gaz_huiles_minerales", period),
        )

        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)
        risque_de_fuite_carbone_eta = etablissement("risque_de_fuite_carbone_eta", period)
        intensite_energetique_valeur_production = etablissement("intensite_energetique_valeur_production", period)
        intensite_energetique_valeur_ajoutee = etablissement("intensite_energetique_valeur_ajoutee", period)

        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement(
            "gaz_dehydration_legumes_et_plantes_aromatiques",
            period,
        )
        # « intensite_energetique » (sans suffixe) n'existe pas dans le modèle, et le seuil
        # qui lui était comparé (seuil_facture_energie_par_va = 0.6744) n'a aucune source.
        # On aligne donc la condition déshydratation sur celle des formules 2019 et 2020,
        # qui applique le critère légal : consommation supérieure à 800 Wh par euro de valeur
        # ajoutée (LF 2019, art. 67), soit 0.0008 MWh/€.
        consommation_par_valeur_ajoutee = etablissement("consommation_par_valeur_ajoutee", period)

        def accise_combustible(choisir):
            """Accise de l'année sur le gaz combustible au tarif désigné, mois par mois."""
            return accise_annuelle(
                period,
                lambda mois: etablissement("consommation_gaz_combustible", mois),
                lambda mois: choisir(parameters(mois).energies.gaz_naturel.accise.combustibles),
            )

        condition_double_usage = gaz_double_usage
        taxe_travaux_agricoles = accise_combustible(lambda c: c.tarifs_reduits.travaux_agricoles_forestiers)
        condition_travaux_agricoles = gaz_travaux_agricoles_et_forestiers
        # La fabrication de produits minéraux relève d'un tarif réduit propre, porté par un
        # paramètre. Les deux autres cas ne sont pas des tarifs réduits mais des exclusions
        # du champ de l'accise : ils restent à zéro, sans paramètre au barème.
        condition_fabrication_mineraux = gaz_production_mineraux_non_metalliques
        condition_exoneration_autres = _or(
            gaz_extraction_production,
            gaz_usage_non_combustible,
        )
        condition_legumes = _and(
            gaz_dehydration_legumes_et_plantes_aromatiques,
            consommation_par_valeur_ajoutee >= parameters(period).energies.gaz_naturel.ticgn.seuil_conso_par_va_legumes,
        )  # 0,0008 MWh par Euro
        seuils = parameters(period).energies.seuils_seqe
        condition_seqe = _or(
            _and(
                seqe,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
            ),
            _and(
                seqe,
                intensite_energetique_valeur_ajoutee >= seuils.intensite_valeur_ajoutee_min,
            ),
        )
        condition_concurrence = _or(
            _and(
                _not(seqe),
                risque_de_fuite_carbone_eta,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
            ),
            _and(
                _not(seqe),
                risque_de_fuite_carbone_eta,
                intensite_energetique_valeur_ajoutee >= seuils.intensite_valeur_ajoutee_min,
            ),
        )
        condition_grande_consommatrice = _and(seqe, grande_consommatrice)
        # Le tarif normal supporte la majoration au titre des zones non interconnectées
        # (L312-37-1), depuis le 1er août 2025 et nulle avant. Les tarifs réduits ne sont pas
        # majorés, et le gaz carburant ne relève pas des catégories fiscales des combustibles.
        taxe_normal_combustible = accise_annuelle(
            period,
            lambda mois: etablissement("consommation_gaz_combustible", mois),
            lambda mois: (
                parameters(mois).energies.gaz_naturel.accise.combustibles.tarif_normal
                + majoration_zni(parameters, mois)
            ),
        )

        return select(
            [
                condition_double_usage,
                condition_travaux_agricoles,
                condition_fabrication_mineraux,
                condition_exoneration_autres,
                condition_legumes,
                condition_seqe,
                condition_concurrence,
                condition_grande_consommatrice,
            ],
            [
                accise_combustible(lambda c: c.tarifs_reduits.doubles_usages),
                taxe_travaux_agricoles,
                accise_combustible(lambda c: c.tarifs_reduits.fabrication_mineraux),
                0,
                etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period),
                etablissement(
                    "taxe_interieure_taxation_consommation_gaz_naturel_seqe",
                    period,
                ),
                etablissement(
                    "taxe_interieure_taxation_consommation_gaz_naturel_concurrence_internationale",
                    period,
                ),
                ticgn_grande_conso,
            ],
            default=taxe_normal_combustible,
        )

    def formula_2024_01_01(etablissement, period, parameters):
        """Suppression du tarif réduit « concurrence internationale ».

        Le tarif applicable aux installations exposées à un risque de fuite de carbone non
        soumises au SEQE est abrogé au 1er janvier 2024 par l'article 94 II K 2° de la loi
        n° 2023-1322 du 29 décembre 2023 de finances pour 2024. Ces installations relèvent
        désormais du tarif normal. Le reste de la formule est inchangé.
        """
        gaz_double_usage = etablissement("gaz_double_usage", period)
        gaz_travaux_agricoles_et_forestiers = etablissement("gaz_travaux_agricoles_et_forestiers", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)
        gaz_usage_non_combustible = _or(
            etablissement("gaz_matiere_premiere", period),
            etablissement("gaz_huiles_minerales", period),
        )

        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)
        intensite_energetique_valeur_production = etablissement("intensite_energetique_valeur_production", period)
        intensite_energetique_valeur_ajoutee = etablissement("intensite_energetique_valeur_ajoutee", period)

        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        gaz_dehydration_legumes_et_plantes_aromatiques = etablissement(
            "gaz_dehydration_legumes_et_plantes_aromatiques",
            period,
        )
        consommation_par_valeur_ajoutee = etablissement("consommation_par_valeur_ajoutee", period)

        def accise_combustible(choisir):
            """Accise de l'année sur le gaz combustible au tarif désigné, mois par mois."""
            return accise_annuelle(
                period,
                lambda mois: etablissement("consommation_gaz_combustible", mois),
                lambda mois: choisir(parameters(mois).energies.gaz_naturel.accise.combustibles),
            )

        condition_double_usage = gaz_double_usage
        taxe_travaux_agricoles = accise_combustible(lambda c: c.tarifs_reduits.travaux_agricoles_forestiers)
        condition_travaux_agricoles = gaz_travaux_agricoles_et_forestiers
        # La fabrication de produits minéraux relève d'un tarif réduit propre, porté par un
        # paramètre. Les deux autres cas ne sont pas des tarifs réduits mais des exclusions
        # du champ de l'accise : ils restent à zéro, sans paramètre au barème.
        condition_fabrication_mineraux = gaz_production_mineraux_non_metalliques
        condition_exoneration_autres = _or(
            gaz_extraction_production,
            gaz_usage_non_combustible,
        )
        condition_legumes = _and(
            gaz_dehydration_legumes_et_plantes_aromatiques,
            consommation_par_valeur_ajoutee >= parameters(period).energies.gaz_naturel.ticgn.seuil_conso_par_va_legumes,
        )  # 0,0008 MWh par Euro
        seuils = parameters(period).energies.seuils_seqe
        condition_seqe = _or(
            _and(
                seqe,
                intensite_energetique_valeur_production >= seuils.intensite_production_min,
            ),
            _and(
                seqe,
                intensite_energetique_valeur_ajoutee >= seuils.intensite_valeur_ajoutee_min,
            ),
        )
        condition_grande_consommatrice = _and(seqe, grande_consommatrice)
        # Le tarif normal supporte la majoration au titre des zones non interconnectées
        # (L312-37-1), depuis le 1er août 2025 et nulle avant. Les tarifs réduits ne sont pas
        # majorés, et le gaz carburant ne relève pas des catégories fiscales des combustibles.
        taxe_normal_combustible = accise_annuelle(
            period,
            lambda mois: etablissement("consommation_gaz_combustible", mois),
            lambda mois: (
                parameters(mois).energies.gaz_naturel.accise.combustibles.tarif_normal
                + majoration_zni(parameters, mois)
            ),
        )

        return select(
            [
                condition_double_usage,
                condition_travaux_agricoles,
                condition_fabrication_mineraux,
                condition_exoneration_autres,
                condition_legumes,
                condition_seqe,
                condition_grande_consommatrice,
            ],
            [
                accise_combustible(lambda c: c.tarifs_reduits.doubles_usages),
                taxe_travaux_agricoles,
                accise_combustible(lambda c: c.tarifs_reduits.fabrication_mineraux),
                0,
                etablissement("taxe_interieure_consommation_gaz_naturel_legumes", period),
                etablissement(
                    "taxe_interieure_taxation_consommation_gaz_naturel_seqe",
                    period,
                ),
                ticgn_grande_conso,
            ],
            default=taxe_normal_combustible,
        )


class taxe_accise_gaz_naturel_carburant(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Pour combiner les gaz naturels combustible et carburant"
    reference = ""

    def formula_2022_01_01(etablissement, period, parameters):
        gaz_double_usage = etablissement("gaz_double_usage", period)
        gaz_travaux_agricoles_et_forestiers = etablissement("gaz_travaux_agricoles_et_forestiers", period)
        gaz_extraction_production = etablissement("gaz_extraction_production", period)
        gaz_production_mineraux_non_metalliques = etablissement("gaz_production_mineraux_non_metalliques", period)

        seqe = etablissement("installation_seqe", period)
        grande_consommatrice = etablissement("installation_grande_consommatrice_energie", period)

        ticgn_grande_conso = etablissement("taxe_interieure_consommation_gaz_naturel_grande_consommatrice", period)

        def accise_carburant(choisir):
            """Accise de l'année sur le gaz carburant au tarif désigné, mois par mois."""
            return accise_annuelle(
                period,
                lambda mois: etablissement("consommation_gaz_carburant", mois),
                lambda mois: choisir(parameters(mois).energies.gaz_naturel.accise.carburants),
            )

        condition_double_usage = gaz_double_usage
        condition_travaux_agricoles = gaz_travaux_agricoles_et_forestiers
        taxe_travaux_agricoles = accise_carburant(lambda c: c.tarifs_reduits.travaux_agricoles_forestiers)
        # La fabrication de produits minéraux relève d'un tarif réduit propre, porté par un
        # paramètre. L'extraction et la production de gaz sont en revanche exclues du champ de
        # l'accise : elles restent à zéro, sans paramètre au barème.
        condition_fabrication_mineraux = gaz_production_mineraux_non_metalliques
        condition_exoneration = gaz_extraction_production
        condition_grande_consommatrice = _and(seqe, grande_consommatrice)
        taxe_normal_carburant = accise_carburant(lambda c: c.tarif_normal)

        return select(
            [
                condition_double_usage,
                condition_travaux_agricoles,
                condition_fabrication_mineraux,
                condition_exoneration,
                condition_grande_consommatrice,
            ],
            [
                accise_carburant(lambda c: c.tarifs_reduits.doubles_usages),
                taxe_travaux_agricoles,
                accise_carburant(lambda c: c.tarifs_reduits.fabrication_mineraux),
                0,
                ticgn_grande_conso,
            ],
            default=taxe_normal_carburant,
        )


class taxe_interieure_taxation_consommation_gaz_naturel_concurrence_internationale(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75/77"
    reference = ""

    def formula_2007_01_01(etablissement, period, parameters):
        # faut changer la date après
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: (
                parameters(mois).energies.gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_indirect_SEQE
            ),
        )


class taxe_interieure_taxation_consommation_gaz_naturel_seqe(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Sous L312-75/76"
    reference = ""

    def formula_2007_01_01(etablissement, period, parameters):
        # faut changer la date après
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: (
                parameters(mois).energies.gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_SEQE
            ),
        )


class taxe_interieure_consommation_gaz_naturel_legumes(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037988864/2019-01-01/"

    def formula_2019_01_01(etablissement, period, parameters):
        # taux_reduit_legumes faisait doublon avec taux_reduit_deshydratation
        # (même valeur, même date, même disposition : LF 2019, art. 67).
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: parameters(mois).energies.gaz_naturel.ticgn.taux_reduits.deshydratation,
        )

    def formula_2022_01_01(etablissement, period, parameters):
        """Le tarif réduit déshydratation passe sous l'accise (CIBS) au 1er janvier 2022.

        Valeur inchangée (1.6) ; la série TICGN est clôturée à cette date.
        """
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: parameters(mois).energies.gaz_naturel.accise.combustibles.tarifs_reduits.deshydratation,
        )


class taxe_interieure_consommation_gaz_naturel_taux_normal(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        """Régime à seuil et abattement — délibérément laissé annuel.

        Cette formule n'est pas de la forme ``assiette * tarif`` : elle compare l'assiette à un
        seuil d'exonération (5 000 000) et lui retranche un abattement mensuel porté à l'année
        (400 000 * 12). Le seuil et l'abattement mordent sur le cumul de l'année, pas sur chaque
        mois pris isolément : les décomposer mois par mois durcirait le seuil d'un facteur douze
        et changerait le droit appliqué. L'assiette est donc sommée sur l'année avant comparaison.

        Le tarif reste une moyenne mensuelle, ce qui est exact tant que la consommation qui
        franchit le seuil n'a pas de profil infra-annuel connu — et le régime disparaît au
        1er janvier 2008, avant toute donnée 2040-TIC.
        """
        seuil = tarif_moyen_annuel(
            period,
            lambda mois: parameters(mois).energies.gaz_naturel.ticgn.seuil_exoneration,
        )
        # 5000000
        abattement = (
            tarif_moyen_annuel(
                period,
                lambda mois: parameters(mois).energies.gaz_naturel.ticgn.abattement,
            )
            * 12
        )
        # 400000
        assiette = etablissement("assiette_ticgn", period, options=[ADD])
        taux = tarif_moyen_annuel(
            period,
            lambda mois: parameters(mois).energies.gaz_naturel.ticgn.taux_normal,
        )
        return (assiette >= seuil) * (assiette - abattement) * taux

    def formula_2008_01_01(etablissement, period, parameters):
        """[à noter : plus de seuil ni d'abattement]."""
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: parameters(mois).energies.gaz_naturel.ticgn.taux_normal,
        )

    def formula_2014_01_01(etablissement, period, parameters):
        """Plus de seuil ni d'abattement — et pas de conversion PCS/PCI.

        La formule multipliait le taux par ``conversion_pcs_pci`` (1,11), au motif que le tarif
        est exprimé en €/MWh PCI depuis le 1er avril 2014 alors que l'assiette serait en MWh PCS.

        **Cette conversion n'a pas lieu d'être** : la quantité déclarée suit l'unité dans
        laquelle la loi exprime le tarif. Quand le texte porte sur du PCS, les données d'entrée
        sont en PCS ; quand il porte sur du PCI, elles sont en PCI. Il n'y a donc jamais deux
        unités à réconcilier, et un millésime se lit toujours dans l'unité de son droit.

        Les agrégats 2040-TIC le confirment : la case `_911237` déclare 8,4300 €/MWh tout rond,
        soit exactement le taux normal de la TICGN au 1er janvier 2021, sans facteur. Le rapport
        entre ce que rendait le modèle et le montant déclaré valait 1,11 exactement, sur les
        quatre millésimes et sans résidu. Voir le constat n° 9 d'``AGREGATS_TIC.md``.

        Le paramètre ``conversion_pcs_pci`` reste au barème : le coefficient physique existe, il
        n'a simplement pas à intervenir dans la liquidation.
        """
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: parameters(mois).energies.gaz_naturel.ticgn.taux_normal,
        )


class taxe_interieure_consommation_gaz_naturel_grande_consommatrice(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_2014_01_01(etablissement, period, parameters):
        """[à noter : plus de seuil ni d'abattement].

        Le tarif réduit « grande consommatrice » naît au 2014-04-01 (arbitrage §2) : il gèle à
        1,19 €/MWh le tarif normal d'avant la réforme, quand celui-ci passe à 1,41. Sur
        janvier-mars 2014, ce tarif réduit n'existe pas et une grande consommatrice relève du
        tarif normal — l'article 266 quinquies dans sa version en vigueur du 2014-01-01 au
        2014-04-01 ne prévoit ni exonération ni tarif réduit pour ces installations, et fixe le
        tarif à 1,19. Le repli laisse donc l'année 2014 plate à 1,19 ; replier sur zéro donnerait
        0,8925, soit 25 % de moins.
        """
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            tarif_avec_repli(
                lambda mois: parameters(mois).energies.gaz_naturel.ticgn.taux_reduits.grandes_consommatrices,
                lambda mois: parameters(mois).energies.gaz_naturel.ticgn.taux_normal,
            ),
        )

    def formula_2022_01_01(etablissement, period, parameters):
        """Sous le CIBS, le tarif « grande consommatrice » devient le tarif réduit SEQE.

        La notion TICGN d'entreprise grande consommatrice d'énergie disparaît avec la réforme :
        le barème IPP ne conserve, pour les gaz naturels combustibles, que les tarifs réduits
        « intensive en énergie soumise au SEQE » (1.52) et « SEQE indirect » (1.6). Le tarif SEQE
        reprend exactement la valeur que portait le tarif réduit grandes consommatrices depuis
        2016 (1.52) : le résultat est donc inchangé, seule la source du paramètre l'est.
        """
        return accise_annuelle(
            period,
            lambda mois: etablissement("assiette_ticgn", mois),
            lambda mois: (
                parameters(mois).energies.gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_SEQE
            ),
        )


class assiette_ticgn(Variable):
    # dès 1986, seules les usages comme combustible sont soumis à la TICGN.
    # dès 2020, les usages comme carbrant y sont somis aussi.
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = "Tax on gas consumption - TICGN"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006615168/1992-12-31/"

    def formula_1986_01_01(etablissement, period, parameters):
        """Taxe sur la consommation de gaz naturel.

        Todo:
        Le gaz consommé :
            - comme matière première
            - comme combustible pour la fabrication d'huiles minérales
            - à destination du chauffage des immeubles d'habitation
            est exonéré.
        """
        conso = etablissement("consommation_gaz_combustible", period)

        conso_exoneree = etablissement("consommation_gaz_chauffage_habitation", period)
        return max(0, conso - conso_exoneree)

    def formula_2000_01_01(etablissement, period, parameters):
        """Taxe sur la consommation de gaz naturel.

        Todo:
        Le gaz consommé :
            - comme matière première
            - comme combustible pour la fabrication d'huiles minérales
            - à destination du chauffage des immeubles d'habitation
            est exonéré.
        """
        conso = etablissement("consommation_gaz_combustible", period)

        # Caractéristique annuelle de l'établissement, lue à l'année depuis une formule mensuelle.
        date_installation_cogeneration = etablissement("date_installation_cogeneration", period.this_year)
        ticgn = parameters(period).energies.gaz_naturel.ticgn
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (
            date_installation_cogeneration < ticgn.annee_limite_cogeneration_exoneree
        ):
            cogeneration_exoneree = True

        conso_exoneree = etablissement(  # noqa: RUF005
            "consommation_gaz_chauffage_habitation",
            period,
        ) + [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        return max(0, conso - conso_exoneree)

    def formula_2006_01_01(etablissement, period, parameters):
        """ajouté consommation_gaz_production_electricite."""
        conso = etablissement("consommation_gaz_combustible", period)

        # Caractéristique annuelle de l'établissement, lue à l'année depuis une formule mensuelle.
        date_installation_cogeneration = etablissement("date_installation_cogeneration", period.this_year)
        ticgn = parameters(period).energies.gaz_naturel.ticgn
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (
            date_installation_cogeneration < ticgn.annee_limite_cogeneration_exoneree
        ):
            cogeneration_exoneree = True

        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period)
            + etablissement("consommation_gaz_production_electricite", period)
            + [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )
        return max(0, conso - conso_exoneree)

    def formula_2007_01_01(etablissement, period, parameters):
        """ajouté consommation_autres_produits_energetique_ticgn."""
        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement(
            "consommation_autres_produits_energetique_ticgn",
            period,
        )

        # Caractéristique annuelle de l'établissement, lue à l'année depuis une formule mensuelle.
        date_installation_cogeneration = etablissement("date_installation_cogeneration", period.this_year)
        ticgn = parameters(period).energies.gaz_naturel.ticgn
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (
            date_installation_cogeneration < ticgn.annee_limite_cogeneration_exoneree
        ):
            cogeneration_exoneree = True

        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period)
            + etablissement("consommation_gaz_production_electricite", period)
            + [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )
        return max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)

    def formula_2008_01_01(etablissement, period, parameters):
        """[à noter : plus de seuil ni d'abattement].

        Todo:
        Ajout des nouvelles exonérations du gaz consommé :
            - autrement que comme combustible
            - à un double usage
            - dans un procédé de fabrication de produits minéraux non métalliques
            - dans les conditions prévues au III de l'article 265 C du CDD (consommation_gaz_fabrication_soi)
            - pour la production d'électricité
                *
                    sauf pour les installations visées à l'article 266 quinquies A
                    (cogeneration, qui existe depuis longtemps)
            ^par rapport à précedement, doit-on en créer un nouveau ?
            - pour les besoins de l'extraction et de la production de gaz naturel (gaz_extraction_production)
            - pour la consommation des particuliers (consommation_gaz_particuliers)
        """
        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement(
            "consommation_autres_produits_energetique_ticgn",
            period,
        )

        # Caractéristique annuelle de l'établissement, lue à l'année depuis une formule mensuelle.
        date_installation_cogeneration = etablissement("date_installation_cogeneration", period.this_year)
        ticgn = parameters(period).energies.gaz_naturel.ticgn
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (
            date_installation_cogeneration < ticgn.annee_limite_cogeneration_exoneree
        ):
            cogeneration_exoneree = True

        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period)
            + etablissement("consommation_gaz_fabrication_soi", period)
            + etablissement("consommation_gaz_production_electricite", period)
            + etablissement("consommation_gaz_particuliers", period)
            + etablissement("consommation_gaz_nc_4401_4402", period)
            + etablissement("consommation_gaz_nc_2705", period)
            + [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )

        return max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)

    def formula_2011_01_01(etablissement, period, parameters):
        """Todo.

        (par rapport à précédemment, )
            la consommation du gaz utilisé pour la production d'électricité par les
            petits producteurs d'électricité au sens du 4° du V de l'article L. 3333-2
            du code général des collectivités territoriales.
            n'est plus exonérée à partir du 1er janvier 2011. Cette condition est
            intégrée comme une exception de consommation_gaz_production_electricite.
        """
        # Caractéristique annuelle de l'établissement, lue à l'année depuis une formule mensuelle.
        date_installation_cogeneration = etablissement("date_installation_cogeneration", period.this_year)
        ticgn = parameters(period).energies.gaz_naturel.ticgn
        cogeneration_exoneree = False

        if (date_installation_cogeneration <= period.start.year <= date_installation_cogeneration + 5) and (
            date_installation_cogeneration < ticgn.annee_limite_cogeneration_exoneree
        ):
            cogeneration_exoneree = True

        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement(
            "consommation_autres_produits_energetique_ticgn",
            period,
        )
        conso_exoneree = (
            etablissement("consommation_gaz_chauffage_habitation", period)
            + etablissement("consommation_gaz_fabrication_soi", period)
            + etablissement("consommation_gaz_production_electricite", period)
            - etablissement("consommation_gaz_electricite_petits_producteurs", period)
            + etablissement("consommation_gaz_particuliers", period)
            + etablissement("consommation_gaz_nc_4401_4402", period)
            + etablissement("consommation_gaz_nc_2705", period)
            + [cogeneration_exoneree * etablissement("consommation_gaz_cogeneration", period)]
        )

        return max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)

    def formula_2014_01_01(etablissement, period, parameters):
        """Todo.

        (par rapport à précédemment, )
        ajouté
        -consommation_gaz_nc_2711_29
        suprimmé
        -consommation_gaz_chauffage_habitation
        -cogéneration car 2011 était la dernière année qu'il était possible de beneficier à une telle éxoneration.
        """
        conso = etablissement("consommation_gaz_combustible", period)
        consommation_autres_produits_energetique_ticgn = etablissement(
            "consommation_autres_produits_energetique_ticgn",
            period,
        )

        conso_exoneree = (
            etablissement("consommation_gaz_fabrication_soi", period)
            + etablissement("consommation_gaz_production_electricite", period)
            - etablissement("consommation_gaz_electricite_petits_producteurs", period)
            + etablissement("consommation_gaz_particuliers", period)
            + etablissement("consommation_gaz_nc_4401_4402", period)
            + etablissement("consommation_gaz_nc_2705", period)
            + etablissement("consommation_gaz_nc_2711_29", period)
        )

        return max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)

    def formula_2020_01_01(etablissement, period, parameters):
        """Todo.

        (par rapport à précédemment, )
            Réintégration des usages carburants dans le champ de la TICGN >=
            consommation_gaz_carburant est ajoutée dans la formule de la variable
            consommation_gaz_naturel
            https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/
            LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#
            LEGIARTI000006615168
        avant c'était consideré comme un produit petrolier, et en 2020 il sont dit
        qu'ils sont desormais consideré comme du gaz naturel.
        """
        conso = etablissement("consommation_gaz_combustible", period) + etablissement(
            "consommation_gaz_carburant",
            period,
        )
        consommation_autres_produits_energetique_ticgn = etablissement(
            "consommation_autres_produits_energetique_ticgn",
            period,
        )
        conso_exoneree = (
            etablissement("consommation_gaz_fabrication_soi", period)
            + etablissement("consommation_gaz_production_electricite", period)
            - etablissement("consommation_gaz_electricite_petits_producteurs", period)
            + etablissement("consommation_gaz_particuliers", period)
            + etablissement("consommation_gaz_nc_4401_4402", period)
            + etablissement("consommation_gaz_nc_2705", period)
            + etablissement("consommation_gaz_nc_2711_29", period)
        )
        return max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)

    def formula_2021_01_01(etablissement, period, parameters):
        """suprimmé consommation_gaz_nc_2705."""
        conso = etablissement("consommation_gaz_combustible", period) + etablissement(
            "consommation_gaz_carburant",
            period,
        )
        consommation_autres_produits_energetique_ticgn = etablissement(
            "consommation_autres_produits_energetique_ticgn",
            period,
        )
        conso_exoneree = (
            etablissement("consommation_gaz_fabrication_soi", period)
            + etablissement("consommation_gaz_production_electricite", period)
            - etablissement("consommation_gaz_electricite_petits_producteurs", period)
            + etablissement("consommation_gaz_particuliers", period)
            + etablissement("consommation_gaz_nc_4401_4402", period)
            + etablissement("consommation_gaz_nc_2711_29", period)
        )

        return max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)

        # pas de ticgn à partir de 2022
        # def formula_2022_01_01(etablissement, period, parameters):
        #     """suprimmé consommation_gaz_nc_4401_4402
        #     """
        #     conso = etablissement("consommation_gaz_combustible", period) +
        etablissement("consommation_gaz_carburant", period)
        return None

    #
    # period)
    #     conso_exoneree = (
    #         etablissement("consommation_gaz_fabrication_soi", period) +
    #         etablissement("consommation_gaz_production_electricite", period)
    #         - etablissement("consommation_gaz_electricite_petits_producteurs", period) +
    #         etablissement("consommation_gaz_particuliers", period) +
    #         etablissement('consommation_gaz_nc_2711_29', period)
    #     )

    #     consommation = max(0, conso + consommation_autres_produits_energetique_ticgn - conso_exoneree)
    #     return consommation
