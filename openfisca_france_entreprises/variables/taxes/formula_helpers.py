"""Shared vectorized logical helpers for taxation energy formulas."""

from functools import reduce

import numpy as np
from numpy import logical_and, logical_or
from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.model_api import MONTH, not_

_ABSENT = object()


def tarif_moyen_annuel(period, lire_tarif, defaut_si_absent=_ABSENT):
    """Moyenne mensuelle d'un tarif sur l'année.

    Le modèle raisonne en périodes annuelles, mais de nombreux tarifs entrent en vigueur en
    cours d'année (TICC au 2014-04-01, TICGN, tarifs d'accise au 2025-02-01, bouclier au
    2023-02-01…). Lire le paramètre au 1er janvier applique alors le tarif ancien — ou le
    nouveau — à toute l'année.

    La consommation étant répartie uniformément sur l'année, la taxe due vaut
    ``somme sur les mois (conso / 12 * tarif du mois)``, soit ``conso * moyenne des tarifs``.
    Cette fonction renvoie cette moyenne, de sorte que les formules conservent leur forme
    ``assiette * tarif`` tout en devenant exactes sur les entrées en vigueur infra-annuelles.

    Exemple - TICC 2014 (1,19 jusqu'au 31 mars, 2,29 a partir du 1er avril) : la moyenne vaut
    (3 * 1,19 + 9 * 2,29) / 12 = 2,015, au lieu de 1,19 en lisant le seul 1er janvier.

    Abrogation en cours d'année : si un produit est retiré du tarif (paramètre clôturé par
    ``value: null``) à une date infra-annuelle, passer ``defaut_si_absent=0`` fait compter zéro
    pour les mois postérieurs à la clôture — la moyenne reflète alors correctement les mois taxés
    puis les mois abrogés. Sans cet argument, un mois clôturé lève ``ParameterNotFoundError``,
    ce qui reste voulu ailleurs pour détecter une lecture de tarif avant son existence.

    :param period: la période annuelle de la formule appelante.
    :param lire_tarif: fonction prenant une période mensuelle et renvoyant le tarif applicable,
        typiquement ``lambda mois: parameters(mois).energies...``.
    :param defaut_si_absent: valeur substituée aux mois où le paramètre est absent/clôturé ;
        par défaut l'absence propage l'erreur.
    """
    mois = list(period.get_subperiods(MONTH))

    def _lire(m):
        if defaut_si_absent is _ABSENT:
            return lire_tarif(m)
        try:
            return lire_tarif(m)
        except ParameterNotFoundError:
            return defaut_si_absent

    return sum(_lire(m) for m in mois) / len(mois)


def tarif_avec_repli(lire_principal, lire_repli):
    """Lecture de tarif avec repli sur un autre paramètre une fois la ligne supprimée.

    ``defaut_si_absent`` de ``tarif_moyen_annuel`` ne sait substituer qu'une constante, ce qui
    convient à une abrogation sèche : le produit sort du tarif et n'est plus taxé (émulsions
    eau-gazole, retirées du tableau B au 2020-07-01 — voir §5 des arbitrages).

    Une ligne de tarif *réduit* peut au contraire disparaître sans que le produit cesse d'être
    taxé : les consommations qu'elle couvrait basculent alors sur le tarif normal. C'est le cas
    des GPL « sous condition d'emploi » — indices 30 bis (propane), 31 bis (butanes) et 33 bis
    (autres GPL), à 15,90 €/100 kg — supprimés du tableau B de l'article 265 du code des douanes
    au 2020-07-01 par l'article 60 I 1° de la loi 2019-1479 (LF 2020). Les versions consolidées
    le montrent sans ambiguïté : présents dans la version en vigueur du 2020-01-01 au 2020-07-01,
    absents dès celle du 2020-07-01 au 2020-08-01, sans article successeur. Ces consommations
    relèvent depuis des indices généraux 30 ter / 31 ter / 34, à 20,71 €/100 kg.

    Replier sur zéro les modéliserait comme non taxées, ce que le tarif ne dit pas. À distinguer
    du gazole non routier, dont la ligne quitte aussi le tableau B mais dont l'article 265 octies
    A et B maintient le tarif : là, c'est le paramètre lui-même qu'il fallait prolonger.

    :param lire_principal: lecture du tarif tant que la ligne existe.
    :param lire_repli: lecture du tarif applicable une fois la ligne supprimée.
    :return: une fonction ``mois -> tarif``, à passer à ``tarif_moyen_annuel``.
    """

    def _lire(mois):
        try:
            return lire_principal(mois)
        except ParameterNotFoundError:
            return lire_repli(mois)

    return _lire


def _and(*args):
    """Vectorized logical and over two or more arrays."""
    r = args[0]
    for a in args[1:]:
        r = logical_and(r, a)
    return r


def _or(*args):
    """Vectorized logical or over two or more arrays."""
    r = args[0]
    for a in args[1:]:
        r = logical_or(r, a)
    return r


def _not(x):
    """Vectorized logical not."""
    return not_(x)


def _dep_in(departement, codes):
    """Vectorized: True where departement is in codes."""
    if len(codes) == 1:
        return departement == codes[0]
    return reduce(lambda a, b: a | b, (departement == c for c in codes))


def departement_commune(etablissement, period):
    """Clé (département, commune) pour indexation des paramètres TCCFE/TDCFE.

    Retourne le vecteur au format "dep_commune" (ex. "1_1", "02A_123").
    Pour les tests : (dep="manqu", commune="ant") retourne "manquant".
    """
    dep = etablissement("departement", period).astype("U32")
    comm = etablissement("commune", period).astype("U32")
    key = np.char.add(np.char.add(dep, "_"), comm)
    return np.where((dep == "manqu") & (comm == "ant"), "manquant", key)
