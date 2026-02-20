"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from functools import reduce

from numpy import logical_and, logical_or
from openfisca_core.model_api import YEAR, Variable, not_, select

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import Etablissement


def _and(*args):
    r = args[0]
    for a in args[1:]:
        r = logical_and(r, a)
    return r


def _or(*args):
    r = args[0]
    for a in args[1:]:
        r = logical_or(r, a)
    return r


def _not(x):
    return not_(x)


def _dep_in(departement, codes):
    """Vectorized: True where departement is in codes."""
    if len(codes) == 1:
        return departement == codes[0]
    return reduce(lambda a, b: a | b, (departement == c for c in codes))


class taxe_interieure_consommation_sur_produits_energetiques(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"
    # etablissement('', period) * parameters(period).
    # etablissement('', period) * parameters(period).
    # NB : pour cette variable, j'ai commencé avec l'année 2021, puis j'ai
    # traveilé en inverse. Donc, les changements sont par rapport à l'année
    # suivante, pas precedante.

    # les changements décrits en dessous sont remarqués par rapport aux années
    # suivantes ; ils s'appliquent aux années précédents
    # 2000
    # rien de changements
    # 2001
    # rien de changements
    # 2002
    # beaucoup de changements à vérfier
    # fioul autre, 27 n'exist que pour 2002, exemption
    # Fiouls lourds 28, 28 bis taxable > vérifie rélation à 24 pour 2003
    #
    # 2003
    # pas de changements
    # 2004
    # les majorations regionales n'existent pas, tandis que les autres majorations par l'état
    # 2006
    # “2. Une réfaction peut être effectuée sur les taux de taxe intérieure de consommation applicable
    # au supercarburant repris aux indices d'identification 11 et 11 ter et au gazole repris à
    # l'indice d'identification 22. A compter du 1er janvier 2006, le montant de cette réfaction
    # est de 1,77 euro par hectolitre pour le supercarburant et de 1,15 euro par hectolitre pour le gazole.”
    # *** TODO: mais où peut-on trouver qui est concerné par cette majoration ? ^

    # consommation_supercarburant_e85
    # ^exempté
    def formula_2000_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e5
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            # + etablissement('consommation_supercarburant_e10', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            # + etablissement('consommation_carbureacteurs_essence_autres_hL', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            #     (combiner en une variable de consommation)
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.gazole
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            # + etablissement('consommation_supercarburant_e85', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            # + etablissement(
            #     'consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires',
            #     period
            # ) * (
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # )
            + etablissement(
                "consommation_carbureacteurs_essence_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    # 2007
    # (par rapport à précédement) majoration régionale pour consommation_gazole
    # et consommation_supercarburant_e5, en plus de la réfaction
    # NB : quelquels changements dans les indices
    # par rapport aux années suivantes; ces changements s'appliquent aux années précédents :
    # 1° Huiles légères, indice 4 bis, hectolitre, taxe intérieure applicable
    # au fioul domestique visé à l'indice 20.
    # parameters(period).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
    #
    # exempté :
    # parameters(period).energies.autres_produits_energetiques.ticpe.
    #     gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
    #
    # remarques peu importantes :
    # ---huiles lubrifiantes et autres, exemption
    # Ex 2715-00, Bitumes fluxés ("cut-backs"), émulsions de bitume de pétrole
    # et similaires : indice 47, exemption.
    # 3403-11, Préparations pour le traitement des matières textiles, du cuir,
    # des pelleteries ou d'autres matières, contenant moins de 70 % en poids
    # d'huiles de pétrole ou de minéraux bitumineux : indice 48, exemption.
    # Ex 3403-19, Préparations lubrifiantes contenant moins de 70 % en poids
    # d'huiles de pétrole ou de minéraux bitumineux : indice 49, exemption.
    # 3811 21-00, Additifs pour huiles lubrifiantes, contenant des huiles de
    # pétrole ou de minéraux bitumineux : indice 51, exemption.
    #
    # il a pas de tariff explicite après 2008, non plus
    #
    #
    def formula_2007_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            # + etablissement('consommation_supercarburant_e10', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.super.super_e10
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            # + etablissement(
            #     'consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires',
            #     period
            # ) * (
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # )
            + etablissement(
                "consommation_carbureacteurs_essence_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    # 2008
    # par rapport aux années suivantes; ces changements s'appliquent aux années précédents :
    #  consommation_supercarburant_e10 exempté
    def formula_2008_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e10
            + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            + etablissement(
                "consommation_carbureacteurs_essence_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    # *** TODO : vérifie quand e10 s'est apparu 2011 pas 2012 ?
    # 2012
    # par rapport à précédement,
    # la majoration régionale inclus désormais 11 ter, consommation_supercarburant_e10
    # par rapport aux années suivantes; ces changements s'appliquent aux années précédents :
    # ajouté
    # parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
    # parameters(period).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
    def formula_2012_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e10
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            + etablissement(
                "consommation_carbureacteurs_essence_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.sous_conditions_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_sous_conditions_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.sous_conditions_hL
        ]
        return total

    # 2014
    # pas de changement par rapport à 2015
    # 2015:
    # pas de changement par rapport à 2016
    # 2016:
    # consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole
    # ^exempté en 2016 et celles d'avant
    def formula_2014_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e10
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            # + etablissement('consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total

    # 2017:
    # parameters(period).energies.autres_produits_energetiques.ticpe.
    #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
    # ^est exempté, également pendant les années précédantes
    # parameters(period).energies.autres_produits_energetiques.ticpe.
    #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
    # ^également pour ça
    # consommation_carburant_constitue_100_estars_methyliques_acides_gras
    # parameters\energies\autres_produits_energetiques\ticpe\gazole\gazole_b_10_hectolitre.yaml
    # ^également
    def formula_2017_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e10
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            # + etablissement('consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            # + etablissement('consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets', period) *
            # parameters(period).energies.autres_produits_energetiques.ticpe.
            #     butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement(
                "consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            # + etablissement('consommation_carburant_constitue_100_estars_methyliques_acides_gras', period) *
            #     parameters(period).energies.autres_produits_energetiques.ticpe.
            #     carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement("consommation_gazole_b_10_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.gazole_b_10_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total

    # 2018: pareil que 2019
    # 2019 : par rapport à 2020,
    # parameters(period).energies.autres_produits_energetiques.ticpe.gazole.gazole_b_10_hectolitre
    # parameters(period).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
    # parameters(period).energies.autres_produits_energetiques.ticpe.
    #     gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
    def formula_2018_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e10
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement(
                "consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement(
                "consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement(
                "consommation_carburant_constitue_100_estars_methyliques_acides_gras",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
            + etablissement("consommation_gazole_b_10_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.gazole_b_10_hectolitre
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilises_comme_carburants", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilises_comme_carburants
            + etablissement(
                "consommation_gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gaz_naturel_etat_gazeux_utilise_sous_conditions_aux_moteurs_stationnaires
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total

    # 2020 : par rapport à 2021,
    # carburants_sous_conditions_hectolitre,
    # sous_conditions_100kg_nets (propane)
    # parameters(period).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
    #
    # parameters(period).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
    #
    # parameters(period).energies.autres_produits_energetiques.ticpe.
    #     autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
    # (en dessous est un nouveau catagorie)
    # parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
    #
    # parameters(period).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
    def formula_2020_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e10
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement(
                "consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement(
                "consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement(
                "consommation_carburant_constitue_100_estars_methyliques_acides_gras",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            # additions, en plus de 2021
            + etablissement(
                "consommation_propane_carburants_sous_conditions_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.sous_conditions_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_sous_condition_100kg_nets", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.sous_condition_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_sous_condition_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.sous_conditions_100kg
            + etablissement(
                "consommation_emulsion_eau_gazoles_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.sous_conditions_hectolitre
            + etablissement(
                "consommation_emulsion_eau_gazoles_autres_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.emulsion_eau_gazole.autres_hectolitre
        ]
        return total

    def formula_2021_01_01(etablissement, period, parameters):
        total = [
            # chaque objet dans la liste est positioné selon sa position dans le code législatif
            etablissement("consommation_goudrons_utilises_comme_combustibles", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.goudrons_utilises_comme_combustibles
            + etablissement(
                "consommation_white_spirit_utilise_comme_combustible", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.white_spirit_utilise_comme_combustible
            + etablissement(
                "consommation_essences_speciales_utilisees_comme_carburants_combustibles",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.essences_speciales_utilisees_comme_carburants_combustibles
            + etablissement(
                "consommation_huiles_legeres_preparation_essence_aviation", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres_preparation_essence_aviation
            + etablissement("consommation_supercarburant_e5", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e5
                + etablissement(
                    "ticpe_majoration_regionale_supercarburant_95_98", period
                )
            )
            + etablissement("consommation_super_ars", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_plombe
            + etablissement("consommation_supercarburant_e10", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.super.super_e10
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_carbureacteurs_essence_carburants_avion_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.carburants_avion_hL
            + etablissement("consommation_carbureacteurs_essence_autres_hL", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.essence.autres_hL
            + etablissement(
                "consommation_huiles_legeres_combustible_carburant_ou_autres", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_legeres
            + etablissement(
                "consommation_petrole_lampant_utilise_comme_combustible_hectolitre",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.utilise_comme_combustible_hectolitre
            + etablissement("consommation_petrole_lampant_autre_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.petrole_lampant.autre_hectolitre
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_carburant_moteurs_avion_hL",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.carburant_moteurs_avion_hL
            + etablissement(
                "consommation_carbureacteurs_petrole_lampant_autres_hL", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carbureacteurs.petrole_lampant.autres_hL
            + etablissement("consommation_huiles_moyennes_autres", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.huiles.huiles_moyennes
            + etablissement(
                "consommation_gazoles_carburants_sous_conditions_hectolitre", period
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.carburants_sous_conditions_hectolitre
            + etablissement("consommation_galzole_fioul_domestique_hectolitre", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.gazole.fioul_domestique_hectolitre
            + etablissement("consommation_gazoles", period)
            * (
                parameters(
                    period
                ).energies.autres_produits_energetiques.ticpe.gazole.gazole
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_fioul_lourd_100kg_net", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.fioul.fioul_lourd_100kg_net
            + etablissement("consommation_propane_carburants_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.autres_100kg_nets
            + etablissement(
                "consommation_propane_carburants_usages_autres_que_comme_carburant_100kg_nets",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.propane_carburants.usages_autres_que_comme_carburant_100kg_nets
            + etablissement("consommation_butanes_liquefies_autres_100kg_nets", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.autres_100kg_nets
            + etablissement(
                "consommation_butanes_liquefies_usages_autres_que_comme_carburant_100kg_nets",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.butanes_liquefies.usages_autres_que_comme_carburant_100kg_nets
            + etablissement(
                "consommation_autres_gaz_de_petrole_liquefies_utilises_comme_carburants_autres_100kg",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres_100kg
            + etablissement("consommation_supercarburant_e85", period)
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.super.super_e85
            + etablissement(
                "consommation_carburant_constitue_minimum_90_alcool_ethylique_agricole",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_minimum_90_alcool_ethylique_agricole
            + etablissement(
                "consommation_carburant_constitue_100_estars_methyliques_acides_gras",
                period,
            )
            * parameters(
                period
            ).energies.autres_produits_energetiques.ticpe.carburant_constitue_100_estars_methyliques_acides_gras
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
            # etablissement('', period) * parameters(period).
        ]
        return total

    def formula_2022_01_01(etablissement, period, parameters):
        # à noter que l'accise est mise en effet dès cette année. beaucoup des categories sont éliminées
        # les majorations régionales sont manquants.
        # manutention portuaire : paramètre absent en 2022 (existe à partir de 2023)
        p = parameters(period).energies.autres_produits_energetiques.accise
        t = p.taux_selon_activite
        c = p.carburants
        comb = p.combustibles
        part = p.tariffs_particuliers

        # Variables utilisées comme conditions (booléen pour select)
        gazoles_transport_guide = etablissement("gazoles_transport_guide", period) != 0
        gazoles_engins_travaux_statiques = (
            etablissement("gazoles_engins_travaux_statiques", period) != 0
        )
        gazoles_transport_collective_personnes = (
            etablissement("gazoles_transport_collective_personnes", period) != 0
        )
        gazoles_transport_taxi = etablissement("gazoles_transport_taxi", period) != 0
        gazoles_transport_routier_marchandises = (
            etablissement("gazoles_transport_routier_marchandises", period) != 0
        )
        autres_produits_travaux_agricoles = (
            etablissement("autres_produits_travaux_agricoles_et_forestiers", period)
            != 0
        )
        gazoles_extraction_mineraux = (
            etablissement("gazoles_extraction_mineraux_industriels", period) != 0
        )
        gazoles_amenagement_pistes = (
            etablissement(
                "gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux",
                period,
            )
            != 0
        )
        intervention_incendie_secours = (
            etablissement(
                "autres_produits_intervention_vehicules_services_incendie_secours",
                period,
            )
            != 0
        )
        essence_transport_taxi = etablissement("essence_transport_taxi", period) != 0

        taux_gazoles = select(
            [
                gazoles_transport_guide,
                gazoles_engins_travaux_statiques,
                gazoles_transport_collective_personnes,
                gazoles_transport_taxi,
                gazoles_transport_routier_marchandises,
                autres_produits_travaux_agricoles,
                gazoles_extraction_mineraux,
                gazoles_amenagement_pistes,
                intervention_incendie_secours,
            ],
            [
                t.gazoles_transport_guide,
                c.gazoles_engins_travaux_statiques,
                t.gazoles_transport_collectif_routier_de_personnes,
                t.gazoles_transport_de_personnes_par_taxi,
                t.gazoles_transport_routier_de_marchandises,
                t.gazoles_travaux_agricoles,
                t.gazoles_extraction_de_mineraux_industriels,
                t.gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux,
                0,
            ],
            default=c.gazoles,
        )

        taux_essence = select(
            [
                intervention_incendie_secours,
                essence_transport_taxi,
            ],
            [
                0,
                t.essences_transport_de_personnes_par_taxi,
            ],
            default=c.essences,
        )

        # gaz_de_petrole_liquefies_combustible_travaux_agricoles n'existe qu'à partir de 2023
        if period.start.year >= 2023:
            taux_gaz_de_petrole_liquefies_combustible = select(
                [autres_produits_travaux_agricoles],
                [t.gaz_de_petrole_liquefies_combustible_travaux_agricoles],
                default=comb.gaz_de_petrole_liquefies_combustibles,
            )
        else:
            taux_gaz_de_petrole_liquefies_combustible = (
                comb.gaz_de_petrole_liquefies_combustibles
            )

        installation_seqe = etablissement("installation_seqe", period) != 0
        risque_de_fuite_carbone_eta = (
            etablissement("risque_de_fuite_carbone_eta", period) != 0
        )
        intensite_energetique_valeur_production = etablissement(
            "intensite_energetique_valeur_production", period
        )
        intensite_energetique_valeur_ajoutee = etablissement(
            "intensite_energetique_valeur_ajoutee", period
        )

        seuils = parameters(period).energies.seuils_seqe
        cond_seqe = _or(
            _and(
                installation_seqe,
                intensite_energetique_valeur_production
                >= seuils.intensite_production_min,
            ),
            _and(
                installation_seqe,
                intensite_energetique_valeur_ajoutee
                >= seuils.intensite_valeur_ajoutee_min,
            ),
        )
        cond_concurrence = _or(
            _and(
                _not(installation_seqe),
                risque_de_fuite_carbone_eta,
                intensite_energetique_valeur_production
                >= seuils.intensite_production_min,
            ),
            _and(
                _not(installation_seqe),
                risque_de_fuite_carbone_eta,
                intensite_energetique_valeur_ajoutee
                >= seuils.intensite_valeur_ajoutee_min,
            ),
        )

        taux_fiouls_lourds = select(
            [
                autres_produits_travaux_agricoles,
                cond_seqe,
                cond_concurrence,
            ],
            [
                t.fiouls_lourds_travaux_agricoles,
                t.fiouls_lourds_seqe,
                t.fiouls_lourds_concurrence_internationale,
            ],
            default=comb.fiouls_lourds,
        )

        taux_fiouls_domestiques = select(
            [
                cond_seqe,
                cond_concurrence,
            ],
            [
                t.fiouls_domestiques_seqe,
                t.fiouls_domestiques_concurrence_internationale,
            ],
            default=comb.fiouls_domestiques,
        )

        taux_petrole_lampant = select(
            [
                cond_seqe,
                cond_concurrence,
            ],
            [
                t.petroles_lampants_seqe,
                t.petroles_lampants_concurrence_internationale,
            ],
            default=comb.petroles_lampants,
        )

        condition_exoneration = _or(
            etablissement("autres_produits_navigation_interieure", period) != 0,
            etablissement("autres_produits_navigation_maritime", period) != 0,
            etablissement("autres_produits_navigation_aerienne", period) != 0,
            etablissement("autres_produits_double_usage", period) != 0,
            etablissement(
                "autre_produits_fabrication_produits_mineraux_non_metalliques",
                period,
            )
            != 0,
            etablissement("autres_produits_secteurs_aeronautique_et_naval", period)
            != 0,
        )

        total_calcule = (
            etablissement("consommation_gazoles_mwh", period)
            * (
                taux_gazoles
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_carbureactuers_mwh", period)
            * c.carbureacteurs
            + etablissement("consommation_essences_mwh", period)
            * (
                taux_essence
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_gaz_de_petrole_liquefies_carburant_mwh", period
            )
            * c.gaz_de_petrole_liquefies_carburant
            + etablissement("consommation_fiouls_lourds_mwh", period)
            * taux_fiouls_lourds
            + etablissement("consommation_fiouls_domestiques_mwh", period)
            * taux_fiouls_domestiques
            + etablissement("consommation_petroles_lampants_mwh", period)
            * taux_petrole_lampant
            + etablissement(
                "consommation_gaz_de_petrole_liquefies_combustible_mwh", period
            )
            * taux_gaz_de_petrole_liquefies_combustible
            + etablissement("consommation_ethanol_diesel_ed95_mwh", period)
            * part.ethanol_diesel_ed95
            + etablissement("consommation_gazole_b100_mwh", period) * part.gazole_b100
            + etablissement("consommation_essence_aviation_mwh", period)
            * part.essence_aviation
            + etablissement("consommation_essence_sp95_e10_mwh", period)
            * part.essence_sp95_e10
            + etablissement("consommation_superethanol_e85_mwh", period)
            * part.superethanol_e85
            + etablissement(
                "consommation_grisou_et_gaz_assimiles_combustible_mwh", period
            )
            * part.grisou_et_gaz_assimiles_combustible
            + etablissement(
                "consommation_biogaz_combustible_non_injecte_dans_le_reseau_mwh",
                period,
            )
            * part.biogaz_combustible_non_injecte_dans_le_reseau
        )

        return select(
            [condition_exoneration],
            [0],
            default=total_calcule,
        )

    def formula_2024_01_01(etablissement, period, parameters):
        # par rapport à précédement, supprimé consommation_essence_aviation_mwh et quelques
        # tarifs visés seqe et concurrence internationale
        p = parameters(period).energies.autres_produits_energetiques.accise
        t = p.taux_selon_activite
        c = p.carburants
        comb = p.combustibles
        part = p.tariffs_particuliers

        gazoles_transport_guide = etablissement("gazoles_transport_guide", period) != 0
        gazoles_engins_travaux_statiques = (
            etablissement("gazoles_engins_travaux_statiques", period) != 0
        )
        gazoles_transport_collective_personnes = (
            etablissement("gazoles_transport_collective_personnes", period) != 0
        )
        gazoles_transport_taxi = etablissement("gazoles_transport_taxi", period) != 0
        gazoles_transport_routier_marchandises = (
            etablissement("gazoles_transport_routier_marchandises", period) != 0
        )
        gazoles_manutention_portuaire = (
            etablissement("gazoles_manutention_portuaire", period) != 0
        )
        autres_produits_travaux_agricoles = (
            etablissement("autres_produits_travaux_agricoles_et_forestiers", period)
            != 0
        )
        gazoles_extraction_mineraux = (
            etablissement("gazoles_extraction_mineraux_industriels", period) != 0
        )
        gazoles_amenagement_pistes = (
            etablissement(
                "gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux",
                period,
            )
            != 0
        )
        intervention_incendie_secours = (
            etablissement(
                "autres_produits_intervention_vehicules_services_incendie_secours",
                period,
            )
            != 0
        )
        essence_transport_taxi = etablissement("essence_transport_taxi", period) != 0

        taux_gazoles = select(
            [
                gazoles_transport_guide,
                gazoles_engins_travaux_statiques,
                gazoles_transport_collective_personnes,
                gazoles_transport_taxi,
                gazoles_transport_routier_marchandises,
                gazoles_manutention_portuaire,
                autres_produits_travaux_agricoles,
                gazoles_extraction_mineraux,
                gazoles_amenagement_pistes,
                intervention_incendie_secours,
            ],
            [
                t.gazoles_transport_guide,
                c.gazoles_engins_travaux_statiques,
                t.gazoles_transport_collectif_routier_de_personnes,
                t.gazoles_transport_de_personnes_par_taxi,
                t.gazoles_transport_routier_de_marchandises,
                t.gazoles_manutention_portuaire,
                t.gazoles_travaux_agricoles,
                t.gazoles_extraction_de_mineraux_industriels,
                t.gazoles_amenagement_et_entretien_pistes_routes_massifs_montagneux,
                0,
            ],
            default=c.gazoles,
        )

        taux_essence = select(
            [
                intervention_incendie_secours,
                essence_transport_taxi,
            ],
            [
                0,
                t.essences_transport_de_personnes_par_taxi,
            ],
            default=c.essences,
        )

        taux_gaz_de_petrole_liquefies_combustible = select(
            [autres_produits_travaux_agricoles],
            [t.gaz_de_petrole_liquefies_combustible_travaux_agricoles],
            default=comb.gaz_de_petrole_liquefies_combustibles,
        )

        taux_fiouls_lourds = select(
            [autres_produits_travaux_agricoles],
            [t.fiouls_lourds_travaux_agricoles],
            default=comb.fiouls_lourds,
        )

        taux_fiouls_domestiques = comb.fiouls_domestiques
        taux_petrole_lampant = comb.petroles_lampants

        condition_exoneration = _or(
            etablissement("autres_produits_navigation_interieure", period) != 0,
            etablissement("autres_produits_navigation_maritime", period) != 0,
            etablissement("autres_produits_navigation_aerienne", period) != 0,
            etablissement("autres_produits_double_usage", period) != 0,
            etablissement(
                "autre_produits_fabrication_produits_mineraux_non_metalliques",
                period,
            )
            != 0,
            etablissement("autres_produits_secteurs_aeronautique_et_naval", period)
            != 0,
        )

        total_calcule = (
            etablissement("consommation_gazoles_mwh", period)
            * (
                taux_gazoles
                + etablissement("ticpe_majoration_regionale_gazole", period)
            )
            + etablissement("consommation_carbureactuers_mwh", period)
            * c.carbureacteurs
            + etablissement("consommation_essences_mwh", period)
            * (
                taux_essence
                + etablissement("ticpe_majoration_regionale_supercarburant_e10", period)
            )
            + etablissement(
                "consommation_gaz_de_petrole_liquefies_carburant_mwh", period
            )
            * c.gaz_de_petrole_liquefies_carburant
            + etablissement("consommation_fiouls_lourds_mwh", period)
            * taux_fiouls_lourds
            + etablissement("consommation_fiouls_domestiques_mwh", period)
            * taux_fiouls_domestiques
            + etablissement("consommation_petroles_lampants_mwh", period)
            * taux_petrole_lampant
            + etablissement(
                "consommation_gaz_de_petrole_liquefies_combustible_mwh", period
            )
            * taux_gaz_de_petrole_liquefies_combustible
            + etablissement("consommation_ethanol_diesel_ed95_mwh", period)
            * part.ethanol_diesel_ed95
            + etablissement("consommation_gazole_b100_mwh", period) * part.gazole_b100
            + etablissement("consommation_essence_sp95_e10_mwh", period)
            * part.essence_sp95_e10
            + etablissement("consommation_superethanol_e85_mwh", period)
            * part.superethanol_e85
            + etablissement(
                "consommation_grisou_et_gaz_assimiles_combustible_mwh", period
            )
            * part.grisou_et_gaz_assimiles_combustible
            + etablissement(
                "consommation_biogaz_combustible_non_injecte_dans_le_reseau_mwh",
                period,
            )
            * part.biogaz_combustible_non_injecte_dans_le_reseau
        )

        return select(
            [condition_exoneration],
            [0],
            default=total_calcule,
        )


# 2007 e5, gazole

# 2012 e10


class ticpe_majoration_regionale_gazole(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"

    def formula_2007_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_gazole
        conditions = [
            _dep_in(departement, ["67", "68"]),
            _dep_in(departement, ["24", "33", "40", "47", "64"]),
            _dep_in(departement, ["3", "15", "43", "63"]),
            _dep_in(departement, ["14", "50", "61"]),
            _dep_in(departement, ["21", "58", "71", "89"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["8", "10", "51", "52"]),
            _dep_in(departement, ["02A", "02B"]),
            _dep_in(departement, ["25", "39", "70", "90"]),
            _dep_in(departement, ["27", "76"]),
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["11", "30", "34", "48", "66"]),
            _dep_in(departement, ["19", "23", "87"]),
            _dep_in(departement, ["54", "55", "57", "88"]),
            _dep_in(departement, ["9", "12", "31", "32", "46", "65", "81", "82"]),
            _dep_in(departement, ["59", "62"]),
            _dep_in(departement, ["4", "5", "6", "13", "83", "84"]),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["2", "60", "80"]),
            _dep_in(departement, ["16", "17", "79", "86"]),
            _dep_in(departement, ["1", "7", "26", "38", "42", "69", "73", "74"]),
        ]
        values = [
            p.alsace,
            p.aquitaine,
            p.auvergne,
            p.basse_normandie,
            p.bourgogne,
            p.bretagne,
            p.centre,
            p.champagne_ardennes,
            p.corse,
            p.franche_comte,
            p.haute_normandie,
            p.ile_france,
            p.languedoc_roussillon,
            p.limousin,
            p.lorraine,
            p.midi_pyrenees,
            p.nord_pas_calais,
            p.paca,
            p.pays_loire,
            p.picardie,
            p.poitou_charentes,
            p.rhone_alpes,
        ]
        return select(conditions, values, default=0)

    def formula_2017_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2017
        conditions = [
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["21", "25", "39", "58", "70", "71", "89", "90"]),
            _dep_in(departement, ["14", "27", "50", "61", "76"]),
            _dep_in(departement, ["02", "59", "60", "62", "80"]),
            _dep_in(
                departement,
                ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
            ),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(
                departement,
                [
                    "16",
                    "17",
                    "19",
                    "23",
                    "24",
                    "33",
                    "40",
                    "47",
                    "64",
                    "79",
                    "86",
                    "87",
                ],
            ),
            _dep_in(
                departement,
                [
                    "09",
                    "11",
                    "12",
                    "30",
                    "31",
                    "32",
                    "34",
                    "46",
                    "48",
                    "65",
                    "66",
                    "81",
                    "82",
                ],
            ),
            _dep_in(
                departement,
                [
                    "01",
                    "03",
                    "07",
                    "15",
                    "26",
                    "38",
                    "42",
                    "43",
                    "63",
                    "69",
                    "73",
                    "74",
                ],
            ),
            _dep_in(departement, ["04", "05", "06", "13", "83", "84"]),
            _dep_in(departement, ["2A", "2B"]),
        ]
        values = [
            p.ile_france,
            p.centre_val_loire,
            p.bourgogne_franche_comte,
            p.normandie,
            p.hauts_france,
            p.grand_est,
            p.pays_la_loire,
            p.bretagne,
            p.nouvelle_aquitaine,
            p.occitanie,
            p.auvergne_rhone_alpes,
            p.paca,
            p.corse,
        ]
        return select(conditions, values, default=0)

    def formula_2022_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_gazole.depuis_2022
        conditions = [
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["21", "25", "39", "58", "70", "71", "89", "90"]),
            _dep_in(departement, ["14", "27", "50", "61", "76"]),
            _dep_in(departement, ["02", "59", "60", "62", "80"]),
            _dep_in(
                departement,
                ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
            ),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(
                departement,
                [
                    "16",
                    "17",
                    "19",
                    "23",
                    "24",
                    "33",
                    "40",
                    "47",
                    "64",
                    "79",
                    "86",
                    "87",
                ],
            ),
            _dep_in(
                departement,
                [
                    "09",
                    "11",
                    "12",
                    "30",
                    "31",
                    "32",
                    "34",
                    "46",
                    "48",
                    "65",
                    "66",
                    "81",
                    "82",
                ],
            ),
            _dep_in(
                departement,
                [
                    "01",
                    "03",
                    "07",
                    "15",
                    "26",
                    "38",
                    "42",
                    "43",
                    "63",
                    "69",
                    "73",
                    "74",
                ],
            ),
            _dep_in(departement, ["04", "05", "06", "13", "83", "84"]),
            _dep_in(departement, ["2A", "2B"]),
        ]
        values = [
            p.ile_france,
            p.centre_val_loire,
            p.bourgogne_franche_comte,
            p.normandie,
            p.hauts_france,
            p.grand_est,
            p.pays_la_loire,
            p.bretagne,
            p.nouvelle_aquitaine,
            p.occitanie,
            p.auvergne_rhone_alpes,
            p.paca,
            p.corse,
        ]
        return select(conditions, values, default=0)


class ticpe_majoration_regionale_supercarburant_e10(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"

    def formula_2007_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10
        conditions = [
            _dep_in(departement, ["67", "68"]),
            _dep_in(departement, ["24", "33", "40", "47", "64"]),
            _dep_in(departement, ["3", "15", "43", "63"]),
            _dep_in(departement, ["14", "50", "61"]),
            _dep_in(departement, ["21", "58", "71", "89"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["8", "10", "51", "52"]),
            _dep_in(departement, ["2A", "2B"]),
            _dep_in(departement, ["25", "39", "70", "90"]),
            _dep_in(departement, ["27", "76"]),
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["11", "30", "34", "48", "66"]),
            _dep_in(departement, ["19", "23", "87"]),
            _dep_in(departement, ["54", "55", "57", "88"]),
            _dep_in(departement, ["9", "12", "31", "32", "46", "65", "81", "82"]),
            _dep_in(departement, ["59", "62"]),
            _dep_in(departement, ["4", "5", "6", "13", "83", "84"]),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["2", "60", "80"]),
            _dep_in(departement, ["16", "17", "79", "86"]),
            _dep_in(departement, ["1", "7", "26", "38", "42", "69", "73", "74"]),
        ]
        values = [
            p.alsace,
            p.aquitaine,
            p.auvergne,
            p.basse_normandie,
            p.bourgogne,
            p.bretagne,
            p.centre,
            p.champagne_ardennes,
            p.corse,
            p.franche_comte,
            p.haute_normandie,
            p.ile_france,
            p.languedoc_roussillon,
            p.limousin,
            p.lorraine,
            p.midi_pyrenees,
            p.nord_pas_calais,
            p.paca,
            p.pays_loire,
            p.picardie,
            p.poitou_charentes,
            p.rhone_alpes,
        ]
        return select(conditions, values, default=0)

    def formula_2017_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2017
        conditions = [
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["21", "25", "39", "58", "70", "71", "89", "90"]),
            _dep_in(departement, ["14", "27", "50", "61", "76"]),
            _dep_in(departement, ["02", "59", "60", "62", "80"]),
            _dep_in(
                departement,
                ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
            ),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(
                departement,
                [
                    "16",
                    "17",
                    "19",
                    "23",
                    "24",
                    "33",
                    "40",
                    "47",
                    "64",
                    "79",
                    "86",
                    "87",
                ],
            ),
            _dep_in(
                departement,
                [
                    "09",
                    "11",
                    "12",
                    "30",
                    "31",
                    "32",
                    "34",
                    "46",
                    "48",
                    "65",
                    "66",
                    "81",
                    "82",
                ],
            ),
            _dep_in(
                departement,
                [
                    "01",
                    "03",
                    "07",
                    "15",
                    "26",
                    "38",
                    "42",
                    "43",
                    "63",
                    "69",
                    "73",
                    "74",
                ],
            ),
            _dep_in(departement, ["04", "05", "06", "13", "83", "84"]),
            _dep_in(departement, ["2A", "2B"]),
        ]
        values = [
            p.ile_france,
            p.centre_val_loire,
            p.bourgogne_franche_comte,
            p.normandie,
            p.hauts_france,
            p.grand_est,
            p.pays_la_loire,
            p.bretagne,
            p.nouvelle_aquitaine,
            p.occitanie,
            p.auvergne_rhone_alpes,
            p.paca,
            p.corse,
        ]
        return select(conditions, values, default=0)

    def formula_2022_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_super_e10.depuis_2022
        conditions = [
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["21", "25", "39", "58", "70", "71", "89", "90"]),
            _dep_in(departement, ["14", "27", "50", "61", "76"]),
            _dep_in(departement, ["02", "59", "60", "62", "80"]),
            _dep_in(
                departement,
                ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
            ),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(
                departement,
                [
                    "16",
                    "17",
                    "19",
                    "23",
                    "24",
                    "33",
                    "40",
                    "47",
                    "64",
                    "79",
                    "86",
                    "87",
                ],
            ),
            _dep_in(
                departement,
                [
                    "09",
                    "11",
                    "12",
                    "30",
                    "31",
                    "32",
                    "34",
                    "46",
                    "48",
                    "65",
                    "66",
                    "81",
                    "82",
                ],
            ),
            _dep_in(
                departement,
                [
                    "01",
                    "03",
                    "07",
                    "15",
                    "26",
                    "38",
                    "42",
                    "43",
                    "63",
                    "69",
                    "73",
                    "74",
                ],
            ),
            _dep_in(departement, ["04", "05", "06", "13", "83", "84"]),
            _dep_in(departement, ["2A", "2B"]),
        ]
        values = [
            p.ile_france,
            p.centre_val_loire,
            p.bourgogne_franche_comte,
            p.normandie,
            p.hauts_france,
            p.grand_est,
            p.pays_la_loire,
            p.bretagne,
            p.nouvelle_aquitaine,
            p.occitanie,
            p.auvergne_rhone_alpes,
            p.paca,
            p.corse,
        ]
        return select(conditions, values, default=0)


class ticpe_majoration_regionale_supercarburant_95_98(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "taxe intérieure de consommation sur les produits énergétiques"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041505082/2025-04-16"

    def formula_2007_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98
        conditions = [
            _dep_in(departement, ["67", "68"]),
            _dep_in(departement, ["24", "33", "40", "47", "64"]),
            _dep_in(departement, ["3", "15", "43", "63"]),
            _dep_in(departement, ["14", "50", "61"]),
            _dep_in(departement, ["21", "58", "71", "89"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["8", "10", "51", "52"]),
            _dep_in(departement, ["2A", "2B"]),
            _dep_in(departement, ["25", "39", "70", "90"]),
            _dep_in(departement, ["27", "76"]),
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["11", "30", "34", "48", "66"]),
            _dep_in(departement, ["19", "23", "87"]),
            _dep_in(departement, ["54", "55", "57", "88"]),
            _dep_in(departement, ["9", "12", "31", "32", "46", "65", "81", "82"]),
            _dep_in(departement, ["59", "62"]),
            _dep_in(departement, ["4", "5", "6", "13", "83", "84"]),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["2", "60", "80"]),
            _dep_in(departement, ["16", "17", "79", "86"]),
            _dep_in(departement, ["1", "7", "26", "38", "42", "69", "73", "74"]),
        ]
        values = [
            p.alsace,
            p.aquitaine,
            p.auvergne,
            p.basse_normandie,
            p.bourgogne,
            p.bretagne,
            p.centre,
            p.champagne_ardennes,
            p.corse,
            p.franche_comte,
            p.haute_normandie,
            p.ile_france,
            p.languedoc_roussillon,
            p.limousin,
            p.lorraine,
            p.midi_pyrenees,
            p.nord_pas_calais,
            p.paca,
            p.pays_loire,
            p.picardie,
            p.poitou_charentes,
            p.rhone_alpes,
        ]
        return select(conditions, values, default=0)

    def formula_2017_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2017
        conditions = [
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["21", "25", "39", "58", "70", "71", "89", "90"]),
            _dep_in(departement, ["14", "27", "50", "61", "76"]),
            _dep_in(departement, ["02", "59", "60", "62", "80"]),
            _dep_in(
                departement,
                ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
            ),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(
                departement,
                [
                    "16",
                    "17",
                    "19",
                    "23",
                    "24",
                    "33",
                    "40",
                    "47",
                    "64",
                    "79",
                    "86",
                    "87",
                ],
            ),
            _dep_in(
                departement,
                [
                    "09",
                    "11",
                    "12",
                    "30",
                    "31",
                    "32",
                    "34",
                    "46",
                    "48",
                    "65",
                    "66",
                    "81",
                    "82",
                ],
            ),
            _dep_in(
                departement,
                [
                    "01",
                    "03",
                    "07",
                    "15",
                    "26",
                    "38",
                    "42",
                    "43",
                    "63",
                    "69",
                    "73",
                    "74",
                ],
            ),
            _dep_in(departement, ["04", "05", "06", "13", "83", "84"]),
            _dep_in(departement, ["2A", "2B"]),
        ]
        values = [
            p.ile_france,
            p.centre_val_loire,
            p.bourgogne_franche_comte,
            p.normandie,
            p.hauts_france,
            p.grand_est,
            p.pays_la_loire,
            p.bretagne,
            p.nouvelle_aquitaine,
            p.occitanie,
            p.auvergne_rhone_alpes,
            p.paca,
            p.corse,
        ]
        return select(conditions, values, default=0)

    def formula_2022_01_01(etablissement, period, parameters):
        departement = etablissement("departement", period)
        p = parameters(
            period
        ).energies.autres_produits_energetiques.major_regionale_ticpe_super_95_98.depuis_2022
        conditions = [
            _dep_in(departement, ["75", "77", "78", "91", "92", "93", "94", "95"]),
            _dep_in(departement, ["18", "28", "36", "37", "41", "45"]),
            _dep_in(departement, ["21", "25", "39", "58", "70", "71", "89", "90"]),
            _dep_in(departement, ["14", "27", "50", "61", "76"]),
            _dep_in(departement, ["02", "59", "60", "62", "80"]),
            _dep_in(
                departement,
                ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
            ),
            _dep_in(departement, ["44", "49", "53", "72", "85"]),
            _dep_in(departement, ["22", "29", "35", "56"]),
            _dep_in(
                departement,
                [
                    "16",
                    "17",
                    "19",
                    "23",
                    "24",
                    "33",
                    "40",
                    "47",
                    "64",
                    "79",
                    "86",
                    "87",
                ],
            ),
            _dep_in(
                departement,
                [
                    "09",
                    "11",
                    "12",
                    "30",
                    "31",
                    "32",
                    "34",
                    "46",
                    "48",
                    "65",
                    "66",
                    "81",
                    "82",
                ],
            ),
            _dep_in(
                departement,
                [
                    "01",
                    "03",
                    "07",
                    "15",
                    "26",
                    "38",
                    "42",
                    "43",
                    "63",
                    "69",
                    "73",
                    "74",
                ],
            ),
            _dep_in(departement, ["04", "05", "06", "13", "83", "84"]),
            _dep_in(departement, ["2A", "2B"]),
        ]
        values = [
            p.ile_france,
            p.centre_val_loire,
            p.bourgogne_franche_comte,
            p.normandie,
            p.hauts_france,
            p.grand_est,
            p.pays_la_loire,
            p.bretagne,
            p.nouvelle_aquitaine,
            p.occitanie,
            p.auvergne_rhone_alpes,
            p.paca,
            p.corse,
        ]
        return select(conditions, values, default=0)
