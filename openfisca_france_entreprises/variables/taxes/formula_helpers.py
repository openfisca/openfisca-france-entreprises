"""Shared vectorized logical helpers for taxation energy formulas."""

from functools import reduce

import numpy as np
from numpy import logical_and, logical_or
from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.model_api import MONTH, not_

_ABSENT = object()


def _tarif_du_mois(lire_tarif, mois, defaut_si_absent):
    """Tarif applicable au mois, en substituant une valeur aux mois où il n'existe pas."""
    if defaut_si_absent is _ABSENT:
        return lire_tarif(mois)
    try:
        return lire_tarif(mois)
    except ParameterNotFoundError:
        return defaut_si_absent


def majoration_zni(parameters, mois):
    """Majoration du tarif normal au titre des zones non interconnectées, pour un mois donné.

    L'article L312-37-1 du code des impositions sur les biens et services, en vigueur depuis
    le 1er août 2025, majore les tarifs normaux d'accise des catégories fiscales des
    combustibles et de l'électricité — ceux qui résultent des articles L312-36 et L312-37 —
    d'un montant affecté au financement des zones non interconnectées.

    Ce n'est pas un régime propre aux ZNI : la majoration est due par **tous** les redevables
    du tarif normal, son dénominateur étant la consommation d'énergie totale du pays. C'est
    pourquoi l'arrêté du 13 décembre 2022 publie le « tarif normal majoré » comme chiffre de
    tête — 15,43 €/MWh pour le gaz du 1er août 2025 au 31 janvier 2026, puis 16,39 —, et c'est
    ce montant que citent la plupart des sources.

    Elle ne s'applique **qu'aux tarifs normaux** : un redevable relevant d'un tarif réduit
    acquitte ce tarif réduit, sans majoration.

    Le montant court du 1er février d'une année civile au 31 janvier de la suivante, sauf la
    première période qui démarre au 1er août 2025 avec l'entrée en vigueur de l'article. Les
    formules s'évaluant mois par mois depuis la bascule mensuelle, il suffit de lire le
    paramètre au mois pour que le découpage soit exact.

    Avant le 1er août 2025 le paramètre n'existe pas, et la majoration vaut zéro.

    :param parameters: l'accesseur de paramètres de la formule appelante.
    :param mois: la période mensuelle courante.
    """
    return _tarif_du_mois(lambda m: parameters(m).energies.majoration_zni, mois, 0)


def tarif_du_mois(mois, lire_tarif, defaut_si_absent=_ABSENT):
    """Tarif applicable au mois, avec substitution aux mois où le paramètre n'existe pas.

    À utiliser dans une formule dont le corps s'évalue mois par mois. ``defaut_si_absent``
    a le même rôle que dans ``accise_annuelle`` : il fait compter une valeur donnée — zéro,
    typiquement — pour les mois où le tarif est absent ou clôturé, au lieu de lever
    ``ParameterNotFoundError``.

    :param mois: la période mensuelle courante.
    :param lire_tarif: fonction ``mois -> tarif``, typiquement
        ``lambda mois: parameters(mois).energies...``.
    :param defaut_si_absent: valeur substituée aux mois où le paramètre est absent ou clôturé.
    """
    return _tarif_du_mois(lire_tarif, mois, defaut_si_absent)


def accise_annuelle(period, lire_assiette, lire_tarif, defaut_si_absent=_ABSENT):
    """Accise due au titre de l'année : somme des accises mensuelles.

    ``somme sur les mois (assiette du mois * tarif du mois)``.

    Remplace ``assiette annuelle * tarif_moyen_annuel(...)``, qui suppose la consommation
    répartie uniformément sur l'année. Cette hypothèse est fausse, et les déclarations
    2040-TIC le montrent : elles ne moyennent jamais, elles ségrègent les tarifs en cases
    distinctes, chaque case portant la quantité taxée à *son* tarif. Une case s'intitule
    littéralement « Usage combustible : tarif à 17,16 €/MWh » — elle nomme son propre tarif.
    Voir le constat n° 8 d'``AGREGATS_TIC.md``.

    Les variables de consommation étant désormais mensuelles (``definition_period = MONTH``)
    et portant ``set_input = set_input_divide_by_period``, les deux usages coexistent sans
    que le modèle ait à trancher :

    - une quantité fournie à l'année est répartie sur les douze mois, et la somme redonne
      ``quantité * moyenne des tarifs`` — exactement la valeur d'avant la bascule. C'est ce
      dont les agrégats Elfe ont besoin, eux qui publient des tarifs déjà moyennés ;
    - une quantité fournie au mois est taxée au tarif de ce mois. C'est ce que la 2040-TIC
      permet, elle qui publie la répartition infra-annuelle réelle.

    La convention d'annualisation cesse ainsi d'être gravée dans les formules.

    :param period: la période annuelle de la formule appelante.
    :param lire_assiette: fonction ``mois -> assiette``, typiquement
        ``lambda mois: etablissement("assiette_ticc", mois)``.
    :param lire_tarif: fonction ``mois -> tarif``, typiquement
        ``lambda mois: parameters(mois).energies...``.
    :param defaut_si_absent: valeur substituée aux mois où le paramètre est absent ou
        clôturé ; par défaut l'absence propage ``ParameterNotFoundError``, ce qui reste
        voulu pour détecter une lecture de tarif avant son existence.
    """
    return sum(
        lire_assiette(mois) * _tarif_du_mois(lire_tarif, mois, defaut_si_absent)
        for mois in period.get_subperiods(MONTH)
    )


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
    return sum(_tarif_du_mois(lire_tarif, m, defaut_si_absent) for m in mois) / len(mois)


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
