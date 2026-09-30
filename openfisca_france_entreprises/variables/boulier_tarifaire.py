"""This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors

from openfisca_core.model_api import ADD, YEAR, Variable, where
from openfisca_core.periods import Instant

from openfisca_france_entreprises.entities import Etablissement


def _tarif_bouclier(etablissement, period, parameters, instant):
    """Tarif du bouclier selon la catégorie fiscale de l'électricité.

    Le bouclier minore le tarif d'accise à deux niveaux distincts, et le barème porte les
    deux : `bouclier_tarifaire.menages` et `bouclier_tarifaire.entreprises` — 1,00 contre
    0,50 en 2022, 21,00 contre 20,50 en 2024. La formule ne lisait que le second, sans
    jamais regarder la catégorie fiscale, et rendait donc la moitié du montant dû aux
    ménages en 2022. Voir le constat n° 5 d'`AGREGATS_TIC.md`.

    La déclaration 2040-TIC sépare nettement les deux régimes en cases distinctes —
    `_911371` « ménages » contre `_911369` « entreprises » en 2022, `_913035` contre
    `_913037` en 2024 —, et les tarifs qu'elle applique sont exactement ceux du barème.

    Le partage suit la catégorie fiscale de l'accise (L312-24 du code des impositions sur
    les biens et services) : les ménages et assimilés sont les puissances de raccordement
    inférieures à 36 kVA, seuil déjà porté par
    `ticfe.categorie_fiscale_petite_et_moyenne_entreprise` et utilisé par
    `taxe_accise_electricite_taux_normal`.

    Ampérage non renseigné (zéro) : le tarif « entreprises » s'applique. Le modèle décrit
    des établissements, pas des ménages ; à défaut de puissance déclarée, c'est le régime
    de droit commun de ses redevables.

    :param instant: l'instant auquel lire le barème. Le bouclier prend effet au 1er février
        et la variable est annuelle : l'instant reste forcé, comme avant. Le traitement
        mensuel du dispositif est un chantier distinct — il encode un basculement de régime,
        pas un changement de tarif.
    """
    bouclier = parameters(instant).energies.electricite.accise.bouclier_tarifaire
    seuil = parameters(period).energies.electricite.ticfe.categorie_fiscale_petite_et_moyenne_entreprise
    amperage = etablissement("amperage", period)
    menages_et_assimiles = (amperage != 0) & (amperage < seuil)
    return where(menages_et_assimiles, bouclier.menages, bouclier.entreprises)


class taxe_electricite_bouclier_tarifaire(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""

    def formula_2022_01_01(etablissement, period, parameters):
        # L'assiette est mensuelle depuis la bascule. Le bouclier conserve pour l'instant son
        # traitement annuel — tarif forcé au 1er février, proratisation à la main dans
        # taxe_electricite — parce qu'il encode un basculement de régime et non un changement de
        # tarif : le passer au mois est un changement de droit, à instruire à part.
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period, options=[ADD])
        # 1,00 pour les ménages et assimilés, 0,50 pour les entreprises.
        taux = _tarif_bouclier(etablissement, period, parameters, Instant((2022, 2, 1)))
        taxe = assiette_taxe_electricite * taux
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        return where(taxe > taxe_accise_electricite, taxe_accise_electricite, taxe)

    def formula_2023_01_01(etablissement, period, parameters):
        # L'assiette est mensuelle depuis la bascule. Le bouclier conserve pour l'instant son
        # traitement annuel — tarif forcé au 1er février, proratisation à la main dans
        # taxe_electricite — parce qu'il encode un basculement de régime et non un changement de
        # tarif : le passer au mois est un changement de droit, à instruire à part.
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period, options=[ADD])
        # 1,00 pour les ménages et assimilés, 0,50 pour les entreprises.
        taux = _tarif_bouclier(etablissement, period, parameters, Instant((2023, 2, 1)))
        taxe = assiette_taxe_electricite * taux
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        return where(taxe > taxe_accise_electricite, taxe_accise_electricite, taxe)

    def formula_2024_01_01(etablissement, period, parameters):
        """2024 est une année à deux niveaux de bouclier, et janvier relève du précédent.

        Le bouclier bascule au 1er février : janvier 2024 est le douzième et dernier mois du
        bouclier ouvert au 1er février 2023, et reste donc à 1,00 / 0,50 €/MWh, quand le
        bouclier de 2024 porte 21,00 / 20,50 à partir de février (arrêté du 25 janvier 2024).
        Lire le barème au seul 1er février faisait payer janvier au niveau de février.

        La déclaration 2040-TIC chiffre la part concernée : le millésime 2024 sert à la fois
        les cases du niveau ancien — `_911369` (47,8 TWh à 0,50 €/MWh) et `_911371`
        (93,8 TWh à 1,00) — et celles du nouveau, `_913037` et `_913035`. Deux niveaux de
        tarif dans une même déclaration annuelle : c'est la définition d'une année de
        bascule, et le modèle doit la restituer.

        Les années 2022 et 2023 n'ont pas ce besoin : janvier 2022 précède tout bouclier —
        `taxe_electricite` le proratise déjà à la main —, et janvier 2023 relève du bouclier
        de 2022, dont les niveaux sont identiques à ceux de 2023. 2025 garde son traitement
        propre, cf. `formula_2025_01_01`.
        """
        assiette_annuelle = etablissement("assiette_taxe_electricite", period, options=[ADD])
        assiette_janvier = etablissement("assiette_taxe_electricite", period.first_month)
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        # 1,00 / 0,50 en janvier, dernier mois du bouclier de 2023 ; 21,00 / 20,50 ensuite.
        taux_janvier = _tarif_bouclier(etablissement, period, parameters, Instant((2024, 1, 1)))
        taux = _tarif_bouclier(etablissement, period, parameters, Instant((2024, 2, 1)))
        taxe = assiette_janvier * taux_janvier + (assiette_annuelle - assiette_janvier) * taux
        return where(taxe > taxe_accise_electricite, taxe_accise_electricite, taxe)

    def formula_2025_01_01(etablissement, period, parameters):
        # Le bouclier s'éteint au 1er février 2025 : seul janvier en relève, au niveau de 2024.
        # `taxe_electricite` proratise à la main — 11/12 d'accise et 1/12 de bouclier —, et
        # cette formule lui rend donc le montant annualisé au tarif du bouclier, comme avant la
        # scission de janvier 2024. Le traitement mensuel du dispositif reste un chantier à part.
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period, options=[ADD])
        taxe_accise_electricite = etablissement("taxe_accise_electricite", period)
        # 21,00 pour les ménages et assimilés, 20,50 pour les entreprises.
        taux = _tarif_bouclier(etablissement, period, parameters, Instant((2024, 2, 1)))
        taxe = assiette_taxe_electricite * taux
        return where(taxe > taxe_accise_electricite, taxe_accise_electricite, taxe)


# On a fini par assumer que toutes les entreprises lui sont eligibles
# class eligibilite_bouclier_tarifaire(Variable):
#     value_type = float
#     entity = Etablissement
#     definition_period = YEAR
#
#
# "https://www.economie.gouv.fr/entreprises/tpe-pme-aides-hausse-prix-energie#:~:text=Bouclier%20tarifaire%20%3A%20de%20quoi%20s,de%20l%27%C3%A9lectricit%C3%A9%20en%202022"
#     reference = ""  #
#     def formula_2022_01_01(etablissement, period, parameters):

#         eligibilite = False

#         if (
#             etablissement("effectif_3112_ul", period) < 10
#             and etablissement("chiffre_affaires_ul", period) < 4000000
#             and etablissement("amperage", period) < 36
#         ):
#             eligibilite = True

#         return eligibilite

# Moins de 10 salariés.
# Un chiffre d'affaires inférieur à deux millions d'euros.
# Un compteur électrique d'une puissance inférieure à 36 kVA.


# Le bouclier tarifaire est un dispositif qui permet de contenir à 4 % la hausse des prix de l'électricité en 2022.
# class bouclier_tarifaire(Variable):
#     value_type = float
#     entity = Etablissement
#     definition_period = YEAR
#
#
# "https://www.economie.gouv.fr/entreprises/tpe-pme-aides-hausse-prix-energie#:~:text=Bouclier%20tarifaire%20%3A%20de%20quoi%20s,de%20l%27%C3%A9lectricit%C3%A9%20en%202022"
#     reference = ""  #
#     def formula_2022_01_01(etablissement, period, parameters):

#         fracteur_energie_avec_bouclier_tarifaire = etablissement("facture_energie_ul", 2023)

#         if etablissement("eligibilite_bouclier_tarifaire", 2023) == True:
#             if etablissement("facture_energie_ul", 2022) * 1.04 < etablissement("facture_energie_ul", 2023) :
#                 fracteur_energie_avec_bouclier_tarifaire =  etablissement("facture_energie_ul", 2022) * 1.04

#         return fracteur_energie_avec_bouclier_tarifaire
# on a fini par décidé que toutes les entreprises theoratiquement beneificienent dubouclier tarifiare
