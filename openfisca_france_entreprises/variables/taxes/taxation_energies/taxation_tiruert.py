"""Taxe incitative relative à l'utilisation d'énergie renouvelable dans les transports (TIRUERT).

⚠️ MODÉLISATION APPROCHÉE — À LIRE AVANT USAGE.

La TIRUERT (ex TIRIB), prévue à l'article 266 quindecies du code des douanes, remplace la TGAP
carburants au 1er janvier 2019. Elle est due par **celui qui met le carburant à la consommation**,
c'est-à-dire un fournisseur ou un distributeur, et son assiette est le **volume mis à la
consommation** par ce redevable.

Le modèle représente les établissements comme des **consommateurs** d'énergie : il ne connaît ni le
redevable légal, ni les volumes mis à la consommation. Par décision de modélisation, la taxe est
donc calculée ici **par approximation, sur la consommation propre de l'établissement**. Il en résulte
deux écarts au droit, assumés :

- l'**assiette** retenue (consommation de l'établissement) n'est pas l'assiette légale (volumes mis
  à la consommation) ;
- le **redevable** retenu (l'établissement consommateur) n'est pas le redevable légal (le fournisseur
  ou le distributeur).

Les montants produits ne valent donc pas liquidation de la taxe. Ils ne doivent pas être utilisés
comme tels, mais comme un ordre de grandeur de l'incitation portée par le dispositif.

Le coefficient légal est l'écart entre le pourcentage national cible d'incorporation d'énergie
renouvelable et la proportion d'énergie renouvelable contenue dans les carburants du redevable.
Cette proportion n'est pas connue du modèle : elle est portée par des variables d'entrée qui, à
défaut d'être renseignées, valent le pourcentage cible — de sorte que la taxe est **nulle par
défaut**, et ne devient positive que si l'utilisateur déclare une proportion inférieure à la cible.
"""

from openfisca_core.model_api import MONTH, YEAR, Variable, where

from openfisca_france_entreprises.entities import Etablissement

REFERENCE = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047501381"


class proportion_energie_renouvelable_essences(Variable):
    value_type = float
    unit = "/1"
    entity = Etablissement
    definition_period = YEAR
    label = "Proportion d'énergie renouvelable contenue dans les essences du redevable"
    reference = REFERENCE

    def formula_2019_01_01(etablissement, period, parameters):
        """À défaut d'être renseignée, la cible nationale est réputée atteinte : la taxe est nulle."""
        return parameters(period).energies.autres_produits_energetiques.taxes_incitatives_carburants.taux_essences


class proportion_energie_renouvelable_gazoles(Variable):
    value_type = float
    unit = "/1"
    entity = Etablissement
    definition_period = YEAR
    label = "Proportion d'énergie renouvelable contenue dans les gazoles du redevable"
    reference = REFERENCE

    def formula_2019_01_01(etablissement, period, parameters):
        """À défaut d'être renseignée, la cible nationale est réputée atteinte : la taxe est nulle."""
        return parameters(period).energies.autres_produits_energetiques.taxes_incitatives_carburants.taux_gazoles


class proportion_energie_renouvelable_carbureacteurs(Variable):
    value_type = float
    unit = "/1"
    entity = Etablissement
    definition_period = YEAR
    label = "Proportion d'énergie renouvelable contenue dans les carburéacteurs du redevable"
    reference = REFERENCE

    def formula_2022_01_01(etablissement, period, parameters):
        """À défaut d'être renseignée, la cible nationale est réputée atteinte : la taxe est nulle."""
        return parameters(
            period,
        ).energies.autres_produits_energetiques.taxes_incitatives_carburants.taux_carbureacteurs


def _composante(etablissement, period, parameters, conso, tarif, taux, proportion):
    """Une composante de la taxe : assiette * tarif * (cible - proportion), plancher à zéro.

    Le dépassement de la cible n'ouvre pas droit à restitution : l'écart est borné à zéro.

    Les consommations étant mensuelles depuis la bascule, la composante de l'année est la somme
    des composantes mensuelles : chaque mois porte sa quantité et son tarif. La proportion
    d'énergie renouvelable du redevable reste une caractéristique annuelle.
    """

    def composante_du_mois(mois):
        tic = parameters(mois).energies.autres_produits_energetiques.taxes_incitatives_carburants
        ecart = getattr(tic, taux) - etablissement(proportion, mois.this_year)
        return etablissement(conso, mois) * getattr(tic, tarif) * where(ecart > 0, ecart, 0)

    return sum(composante_du_mois(mois) for mois in period.get_subperiods(MONTH))


class taxe_incitative_energie_renouvelable_transports(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = "Taxe incitative relative à l'utilisation d'énergie renouvelable dans les transports (TIRUERT)"
    reference = REFERENCE
    documentation = """Modélisation approchée : assiette et redevable diffèrent du droit (cf. en-tête du module)."""

    def formula_2019_01_01(etablissement, period, parameters):
        """Essences et gazoles. La TIRUERT remplace la TGAP carburants, clôturée à cette date."""
        return _composante(
            etablissement,
            period,
            parameters,
            "consommation_essences_mwh",
            "tarifs_essences",
            "taux_essences",
            "proportion_energie_renouvelable_essences",
        ) + _composante(
            etablissement,
            period,
            parameters,
            "consommation_gazoles_mwh",
            "tarifs_gazoles",
            "taux_gazoles",
            "proportion_energie_renouvelable_gazoles",
        )

    def formula_2022_01_01(etablissement, period, parameters):
        """Par rapport à précédemment, ajout des carburéacteurs (cible de 1 % au 1er janvier 2022)."""
        return (
            _composante(
                etablissement,
                period,
                parameters,
                "consommation_essences_mwh",
                "tarifs_essences",
                "taux_essences",
                "proportion_energie_renouvelable_essences",
            )
            + _composante(
                etablissement,
                period,
                parameters,
                "consommation_gazoles_mwh",
                "tarifs_gazoles",
                "taux_gazoles",
                "proportion_energie_renouvelable_gazoles",
            )
            + _composante(
                etablissement,
                period,
                parameters,
                "consommation_carbureactuers_mwh",
                "tarifs_carbureacteurs",
                "taux_carbureacteurs",
                "proportion_energie_renouvelable_carbureacteurs",
            )
        )

    def formula_2025_01_01(etablissement, period, parameters):
        """Par rapport à précédemment, la composante carburéacteurs est clôturée au 1er janvier 2025."""
        return _composante(
            etablissement,
            period,
            parameters,
            "consommation_essences_mwh",
            "tarifs_essences",
            "taux_essences",
            "proportion_energie_renouvelable_essences",
        ) + _composante(
            etablissement,
            period,
            parameters,
            "consommation_gazoles_mwh",
            "tarifs_gazoles",
            "taux_gazoles",
            "proportion_energie_renouvelable_gazoles",
        )
