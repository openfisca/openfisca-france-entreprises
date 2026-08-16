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

from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.model_api import MONTH, YEAR, Variable, where

from openfisca_france_entreprises.entities import Etablissement

REFERENCE = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047501381"

# Premier millésime des coefficients de conversion, cf. `_volume_hectolitres`.
_PREMIER_MILLESIME_COEFFICIENTS = "2023-01-01"


class proportion_energie_renouvelable_essences(Variable):
    value_type = float
    unit = "/1"
    entity = Etablissement
    definition_period = YEAR
    label = "Proportion d'énergie renouvelable contenue dans les essences du redevable"
    reference = REFERENCE

    def formula_2019_01_01(etablissement, period, parameters):
        """À défaut d'être renseignée, la cible nationale est réputée atteinte : la taxe est nulle."""
        return parameters(period).energies.autres_produits_energetiques.tiruert.taux_essences


class proportion_energie_renouvelable_gazoles(Variable):
    value_type = float
    unit = "/1"
    entity = Etablissement
    definition_period = YEAR
    label = "Proportion d'énergie renouvelable contenue dans les gazoles du redevable"
    reference = REFERENCE

    def formula_2019_01_01(etablissement, period, parameters):
        """À défaut d'être renseignée, la cible nationale est réputée atteinte : la taxe est nulle."""
        return parameters(period).energies.autres_produits_energetiques.tiruert.taux_gazoles


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
        ).energies.autres_produits_energetiques.tiruert.taux_carbureacteurs


def _volume_hectolitres(parameters, mois, produit, energie_mwh):
    """Volume en hectolitres correspondant à une énergie en mégawattheures.

    L'assiette légale est un **volume** — « le volume total, respectivement, des essences, des
    gazoles et des carburéacteurs pour lesquels elle est devenue exigible » (III de l'article
    266 quindecies) — et le tarif est **en euros par hectolitre**, le IV l'intitulant ainsi en
    toutes lettres : essences 140, gazoles 140, carburéacteurs 168 au 1er janvier 2023.

    Le modèle, lui, porte les consommations de carburants en MWh depuis la recodification. La
    conversion est celle de l'arrêté du 30 décembre 2022 : un hectolitre vaut
    ``coefficients_conversion.<produit>`` gigajoules, soit ce nombre divisé par 3,6
    mégawattheures. D'où ``hL = MWh x 3,6 / GJ_par_hL``.

    Le coefficient vaut 3,6 GJ/hL pour les gazoles — la conversion est alors l'identité, ce qui
    explique que le défaut soit resté invisible de ce côté — 3,2 pour les essences et 3,4 pour
    les carburéacteurs.

    Réserve assumée : le barème date ces coefficients du 1er janvier 2023, date de l'arrêté qui
    les *constate*, et non celle où la physique commencerait. La TIRUERT s'applique depuis 2019 ;
    pour les années antérieures on retient la même valeur. La correction propre est de faire
    remonter la série en amont, au barème.
    """
    conversion = parameters(mois).energies.coefficients_conversion
    try:
        gigajoules_par_hectolitre = getattr(conversion, produit)
    except ParameterNotFoundError:
        gigajoules_par_hectolitre = getattr(
            parameters(_PREMIER_MILLESIME_COEFFICIENTS).energies.coefficients_conversion,
            produit,
        )
    return energie_mwh * 3.6 / gigajoules_par_hectolitre


def _composante(etablissement, period, parameters, conso, produit, tarif, taux, proportion):
    """Une composante de la taxe : assiette * tarif * (cible - proportion), plancher à zéro.

    Le dépassement de la cible n'ouvre pas droit à restitution : l'écart est borné à zéro.

    L'assiette est convertie en hectolitres, unité du tarif : voir ``_volume_hectolitres``.

    Les consommations étant mensuelles depuis la bascule, la composante de l'année est la somme
    des composantes mensuelles : chaque mois porte sa quantité et son tarif. La proportion
    d'énergie renouvelable du redevable reste une caractéristique annuelle.
    """

    def composante_du_mois(mois):
        tic = parameters(mois).energies.autres_produits_energetiques.tiruert
        ecart = getattr(tic, taux) - etablissement(proportion, mois.this_year)
        volume = _volume_hectolitres(parameters, mois, produit, etablissement(conso, mois))
        return volume * getattr(tic, tarif) * where(ecart > 0, ecart, 0)

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
            "essences",
            "tarifs_essences",
            "taux_essences",
            "proportion_energie_renouvelable_essences",
        ) + _composante(
            etablissement,
            period,
            parameters,
            "consommation_gazoles_mwh",
            "gazoles",
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
                "essences",
                "tarifs_essences",
                "taux_essences",
                "proportion_energie_renouvelable_essences",
            )
            + _composante(
                etablissement,
                period,
                parameters,
                "consommation_gazoles_mwh",
                "gazoles",
                "tarifs_gazoles",
                "taux_gazoles",
                "proportion_energie_renouvelable_gazoles",
            )
            + _composante(
                etablissement,
                period,
                parameters,
                "consommation_carbureactuers_mwh",
                "carbureacteurs",
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
            "essences",
            "tarifs_essences",
            "taux_essences",
            "proportion_energie_renouvelable_essences",
        ) + _composante(
            etablissement,
            period,
            parameters,
            "consommation_gazoles_mwh",
            "gazoles",
            "tarifs_gazoles",
            "taux_gazoles",
            "proportion_energie_renouvelable_gazoles",
        )
