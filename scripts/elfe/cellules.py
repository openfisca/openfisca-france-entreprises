"""Rebuild the cell-level tables the Shiny app never exports.

The CGDD application publishes six *marginal* views of one underlying cell set.
No single export carries them jointly. Two keys let us recombine them:

  (perimetre, millesime, tarif)             the implicit tax value — universal,
                                            présent à l'identique dans les six vues
  (perimetre, millesime, tarif, quantite)   un *atome* : les quantités portent ~15
                                            chiffres significatifs, donc une même
                                            valeur dans deux vues désigne le même
                                            jeu d'enregistrements

Trois sorties, à trois grains :

  elfe_cellules.csv       une ligne par valeur de tarif implicite. Composantes en
                          colonnes. C'est la table qui SOMME juste.
  elfe_atomes.csv         une ligne par atome, avec les libellés de toutes les
                          dimensions qui le reconnaissent. C'est la table la plus
                          RENSEIGNÉE — mais c'est une union de marginales, pas une
                          partition : voir l'avertissement sur `n_dimensions`.
  elfe_sous_cellules.csv  les lignes Instruments intactes, quand un même tarif naît
                          de mélanges de composantes différents.

Ce que ces fichiers ne font pas : reconstituer la table croisée complète. Les
dimensions sont des marginales et leur jointe n'est pas identifiée. Les colonnes
`*_n` et `n_dimensions` disent exactement ce qui est su.
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(RACINE, "assets", "elfe")

# Tarifs et quantités sont des flottants venus de .xlsx distincts. Arrondir à 9
# décimales apparie 1114/1114 clés tarifaires ; à 10, l'appariement se dégrade.
PRECISION_CLE = 9
CLE = ["perimetre", "millesime", "tarif"]
CLE_ATOME = CLE + ["quantite"]

COMPOSANTES = [
    "taux_taxation",
    "composante_carbone",
    "boucliers_et_aides",
    "prix_quotas_ets",
    "prix_reel_quotas_ets",
    "remboursement_indirect_ets",
]

# Identité additive vérifiée sur la source. `composante_carbone` en est exclue :
# c'est un report indicatif, qui peut excéder le taux de taxation net.
IDENTITE = ["taux_taxation", "boucliers_et_aides", "prix_quotas_ets"]

DIMENSIONS = {
    "Régime fiscal": "regime_fiscal",
    "Secteur économique": "secteur_economique",
    "Agents": "agents",
    "Type de produit": "type_de_produit",
    "Gaz à effet de serre": "gaz_a_effet_de_serre",
}


def charger():
    ventilation = pd.read_csv(os.path.join(ASSETS, "elfe.csv"))
    instruments = pd.read_csv(os.path.join(ASSETS, "elfe_instruments.csv"))
    instruments["tarif"] = instruments["tarif_effectif"]
    for table in (ventilation, instruments):
        table["tarif"] = table["tarif"].round(PRECISION_CLE)
        table["quantite"] = table["quantite"].round(PRECISION_CLE)
    for colonne in COMPOSANTES:
        if colonne not in instruments:
            instruments[colonne] = 0.0
    instruments[COMPOSANTES] = instruments[COMPOSANTES].fillna(0.0)
    return ventilation, instruments


def sous_cellules(instruments):
    """Les lignes Instruments, intactes, rangées sous leur clé tarifaire.

    Une même valeur de tarif effectif peut naître de mélanges différents — le cas
    le plus fréquent oppose quotas ETS gratuits et quotas achetés, qui partagent
    `prix_quotas_ets` mais se séparent sur `prix_reel_quotas_ets`. Agréger
    détruirait cette information : on la garde ici.
    """
    d = instruments.sort_values(CLE + ["quantite"], ascending=[True, True, True, False]).copy()
    d["rang"] = d.groupby(CLE).cumcount() + 1
    colonnes = CLE + ["rang"] + COMPOSANTES + ["quantite", "unite_tarif", "unite_quantite"]
    return d[colonnes].reset_index(drop=True)


def agreger_composantes(instruments):
    """Une ligne par clé tarifaire, composantes moyennées par les quantités.

    La moyenne pondérée est exacte au sens de l'identité : toutes les
    sous-cellules d'une clé partagent le même tarif effectif, donc toute
    combinaison convexe de leurs vecteurs de composantes le vérifie encore. Rien
    n'est approché ; seule la distinction entre sous-cellules est perdue, et
    `decomposition_homogene` dit où.
    """
    lignes = []
    for cle, groupe in instruments.groupby(CLE, sort=False):
        poids = groupe["quantite"].to_numpy()
        total = poids.sum()
        normalise = poids / total if total > 0 else None
        ligne = dict(zip(CLE, cle))
        for colonne in COMPOSANTES:
            valeurs = groupe[colonne].to_numpy()
            ligne[colonne] = float(
                valeurs @ normalise if normalise is not None else valeurs.mean()
            )
        ligne["quantite"] = float(total)
        ligne["n_sous_cellules"] = len(groupe)
        ligne["decomposition_homogene"] = (
            groupe[COMPOSANTES].round(PRECISION_CLE).drop_duplicates().shape[0] == 1
        )
        ligne["unite_tarif"] = groupe["unite_tarif"].iloc[0]
        ligne["unite_quantite"] = groupe["unite_quantite"].iloc[0]
        lignes.append(ligne)
    return pd.DataFrame(lignes)


def libelles(ventilation, cle):
    """Libellé par dimension sur la clé demandée, quand il est sans ambiguïté."""
    sortie = []
    for libelle, slug in DIMENSIONS.items():
        d = ventilation[ventilation["dimension"] == libelle]
        if d.empty:
            continue
        groupe = d.groupby(cle)["categorie"]
        sortie.append(pd.concat([
            groupe.agg(lambda s: s.iloc[0] if s.nunique() == 1 else pd.NA).rename(slug),
            groupe.nunique().rename(f"{slug}_n"),
        ], axis=1))
    return sortie


def attacher_dimensions(cellules, ventilation):
    """Sur le grain tarifaire, un tarif ne détermine pas une catégorie.

    Jusqu'à 36 régimes fiscaux partagent le tarif nul. `<dim>_n` porte le nombre
    de catégories, `<dim>` le libellé quand il n'y en a qu'une. La ventilation
    complète reste dans elfe.csv, qui se joint sur la même clé.
    """
    for bloc in libelles(ventilation, CLE):
        cellules = cellules.merge(bloc.reset_index(), on=CLE, how="left")
        slug = bloc.columns[0]
        cellules[f"{slug}_n"] = cellules[f"{slug}_n"].fillna(0).astype(int)
    return cellules


def atomes(ventilation, instruments, cellules):
    """Le grain le plus renseigné : (tarif, quantité), recoupé entre dimensions.

    AVERTISSEMENT — cette table est une UNION de marginales, pas une partition.
    Deux dimensions qui découpent une même cellule tarifaire différemment y
    produisent des atomes distincts et redondants. Sommer `quantite` sur toute la
    table donne ~3 fois la masse réelle. Pour sommer, utiliser elfe_cellules.csv,
    ou filtrer elfe.csv sur une seule dimension.

    `n_dimensions` dit combien de vues reconnaissent l'atome. À 1, c'est un
    découpage propre à une dimension ; au-delà, les dimensions concordent et les
    libellés se lisent conjointement — c'est le morceau de table croisée qui est
    réellement identifié.
    """
    base = ventilation[CLE_ATOME].drop_duplicates().reset_index(drop=True)

    for bloc in libelles(ventilation, CLE_ATOME):
        base = base.merge(bloc.reset_index(), on=CLE_ATOME, how="left")
        slug = bloc.columns[0]
        base[f"{slug}_n"] = base[f"{slug}_n"].fillna(0).astype(int)

    # Héritage : quand une dimension ne porte qu'une catégorie sur toute la
    # cellule tarifaire, ce libellé vaut pour chacun de ses atomes, y compris
    # ceux découpés par une autre dimension. C'est un gain gratuit et exact.
    slugs = [s for s in DIMENSIONS.values() if s in base]
    index_cellule = base.set_index(CLE).index
    for slug in slugs:
        if slug not in cellules:
            continue
        unique_cellule = cellules.set_index(CLE)[slug].reindex(index_cellule)
        herite = base[slug].isna() & pd.Series(unique_cellule.notna().to_numpy())
        base[slug] = base[slug].fillna(pd.Series(unique_cellule.to_numpy()))
        base[f"{slug}_herite"] = herite

    base["n_dimensions"] = base[slugs].notna().sum(axis=1)
    base["n_dimensions_propres"] = (base[[f"{s}_n" for s in slugs]] > 0).sum(axis=1)

    # Décomposition exacte quand l'atome existe tel quel dans Instruments ;
    # sinon repli sur la moyenne pondérée du grain tarifaire, signalé.
    exacte = instruments.drop_duplicates(CLE_ATOME).set_index(CLE_ATOME)[COMPOSANTES]
    base = base.merge(exacte, on=CLE_ATOME, how="left")
    base["decomposition_exacte"] = base[COMPOSANTES[0]].notna()
    repli = cellules.set_index(CLE)[COMPOSANTES]
    jointure = base.set_index(CLE).index
    for colonne in COMPOSANTES:
        base[colonne] = base[colonne].fillna(pd.Series(repli[colonne].reindex(jointure).to_numpy()))

    # Une cellule tarifaire dont les atomes multi-dimensions épuisent la masse
    # est réellement partitionnée : ses lignes se somment sans doublon.
    # Sur les libellés PROPRES uniquement : un libellé hérité ne prouve pas que
    # les dimensions découpent la cellule de la même façon.
    part = base[base["n_dimensions_propres"] >= 2].groupby(CLE)["quantite"].sum()
    total = cellules.set_index(CLE)["quantite"]
    complete = (part - total.reindex(part.index)).abs() < 1e-6
    base["partition_verifiee"] = base.set_index(CLE).index.map(
        complete.reindex(base.set_index(CLE).index.unique(), fill_value=False)
    )
    return base


def controler(cellules, sous, ventilation, instruments):
    """Quatre contrôles, dont deux ne dépendent d'aucune hypothèse de ce script."""
    brut = (instruments["tarif_effectif"] - instruments[IDENTITE].sum(axis=1)).abs().max()
    print(f"identité sur les lignes Instruments brutes : écart max {brut:.2e}")
    assert brut < 1e-9, "l'identité additive ne tient pas dans la source"

    # Après pondération l'identité doit survivre : les sous-cellules d'une clé
    # partagent le même tarif, donc toute combinaison convexe le vérifie encore.
    # Le résidu est celui de l'arrondi de la clé, pas une approximation.
    pondere = (cellules["tarif"] - cellules[IDENTITE].sum(axis=1)).abs().max()
    print(f"identité après pondération                 : écart max {pondere:.2e}")
    assert pondere < 10 ** -PRECISION_CLE, "la pondération a cassé l'identité"

    quantites = ventilation.groupby(CLE + ["dimension"])["quantite"].sum().unstack()
    dispersion = (quantites.max(axis=1) - quantites.min(axis=1)).max()
    print(f"quantité identique entre les dimensions    : écart max {dispersion:.2e}")
    assert dispersion < 1e-6, "les dimensions ne décrivent pas le même jeu de cellules"

    joint = cellules.merge(
        quantites.max(axis=1).rename("q_ventilation").reset_index(), on=CLE, how="left",
    )
    ecart = (joint["quantite"] - joint["q_ventilation"]).abs().max()
    print(f"quantité Instruments vs ventilation        : écart max {ecart:.2e}")
    assert ecart < 1e-6, "Instruments et ventilation ne portent pas les mêmes masses"

    assert len(sous) == len(cellules) + (cellules["n_sous_cellules"] - 1).sum()


def rapporter(cellules, base):
    for perimetre, d in cellules.groupby("perimetre"):
        a = base[base["perimetre"] == perimetre]
        slugs = [s for s in DIMENSIONS.values() if f"{s}_n" in d and (d[f"{s}_n"] > 0).any()]
        masse = d["quantite"].sum()
        print()
        print(f"{perimetre} : {len(d)} cellules tarifaires, {len(a)} atomes, "
              f"masse {masse:.1f} {d['unite_quantite'].iloc[0]}")
        print(f"   décomposition hétérogène : {int((~d['decomposition_homogene']).sum())} cellules")
        print(f"   décomposition exacte     : {int(a['decomposition_exacte'].sum())} atomes, "
              f"{100 * a.loc[a['decomposition_exacte'], 'quantite'].sum() / masse:.1f} % de la masse")
        # La masse cumulée sur les atomes est redondante (union de marginales) :
        # on rapporte des effectifs, pas des taux de couverture.
        for n in range(1, len(slugs) + 1):
            s = a[a["n_dimensions"] >= n]
            if not len(s):
                break
            propres = (a["n_dimensions_propres"] >= n).sum()
            print(f"   >= {n} libellé(s) : {len(s):5d} atomes "
                  f"(dont {propres:5d} sans héritage)")
        cellules_partitionnees = a.loc[a["partition_verifiee"], CLE].drop_duplicates()
        print(f"   partition vérifiée       : {len(cellules_partitionnees)} cellules sur {len(d)}")


def main():
    ventilation, instruments = charger()

    sous = sous_cellules(instruments)
    cellules = agreger_composantes(instruments)

    # Ce que le calculateur couvre, et ce qu'il ne couvrira jamais : l'accise
    # nette de boucliers se compare à nos variables, le prix des quotas non.
    cellules["taux_taxation_net"] = cellules["taux_taxation"] + cellules["boucliers_et_aides"]
    cellules["hors_calculateur"] = cellules["prix_quotas_ets"]

    cellules = attacher_dimensions(cellules, ventilation)
    controler(cellules, sous, ventilation, instruments)
    base = atomes(ventilation, instruments, cellules)

    entete = CLE + ["quantite"] + COMPOSANTES + [
        "taux_taxation_net", "hors_calculateur", "n_sous_cellules", "decomposition_homogene",
    ]
    for slug in DIMENSIONS.values():
        if slug in cellules:
            entete += [slug, f"{slug}_n"]
    entete += ["unite_tarif", "unite_quantite"]
    cellules = cellules[entete].sort_values(CLE).reset_index(drop=True)

    entete_atomes = CLE_ATOME + COMPOSANTES + [
        "decomposition_exacte", "n_dimensions", "n_dimensions_propres", "partition_verifiee",
    ]
    for slug in DIMENSIONS.values():
        if slug in base:
            entete_atomes += [slug, f"{slug}_n", f"{slug}_herite"]
    base = base[entete_atomes].sort_values(CLE_ATOME).reset_index(drop=True)

    cellules.to_csv(os.path.join(ASSETS, "elfe_cellules.csv"), index=False, encoding="utf-8")
    base.to_csv(os.path.join(ASSETS, "elfe_atomes.csv"), index=False, encoding="utf-8")
    sous.to_csv(os.path.join(ASSETS, "elfe_sous_cellules.csv"), index=False, encoding="utf-8")
    print(f"\nelfe_cellules.csv      : {cellules.shape}")
    print(f"elfe_atomes.csv        : {base.shape}")
    print(f"elfe_sous_cellules.csv : {sous.shape}")
    rapporter(cellules, base)


if __name__ == "__main__":
    main()
