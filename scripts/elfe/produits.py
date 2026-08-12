"""Résout la relation `Régime fiscal` -> `Type de produit`, et la vérifie par les sommes.

L'hypothèse de départ — un régime fiscal porte une énergie et une seule, donc
`Type de produit` regroupe des régimes — est **presque** vraie. Elle se vérifie
en reconstruisant la ventilation par produit comme somme des régimes, cellule
tarifaire par cellule tarifaire.

Le mapping n'est pas deviné depuis les intitulés : il est **mesuré**, dans les
deux sens, sur les cellules dégénérées —

  produit unique sur la cellule  -> tous ses régimes portent ce produit
  régime unique sur la cellule   -> il porte tous les produits de la cellule

puis complété par lecture des intitulés pour les régimes que ces deux vues
n'atteignent jamais. La lecture des intitulés retrouve 27/27 des régimes purs
observés côté carbone : elle est fiable, mais elle ne suffit pas — voir
CORRECTIONS.

Trois régimes se **partagent** entre produits, et chaque partage est
interprétable :

  - côté énergie, treize régimes de carburants et de gaz portent une part
    renouvelable (E85 58 %, E10 6,5 %, gazole routier 7,5 %, essence 3,3 %,
    biométhane 0,4 à 21 % selon l'usage) classée `Chaleur et biomasse` ;
  - côté carbone, `Autres produits pétroliers` porte ~29 % d'usages non
    énergétiques — lubrifiants, bitumes, solvants, charges pétrochimiques —
    sans CO2 de combustion, donc classés `Non combustible`.

L'intérêt : cette relation étant déterministe, elle annule les (R−1)(S−1) degrés
de liberté entre ces deux dimensions. C'est le seul morceau de table croisée que
les marginales publiées permettent de reconstituer.
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(RACINE, "assets", "elfe")

K = ["perimetre", "millesime", "tarif"]
PRECISION_CLE = 9
TOLERANCE = 0.01  # MtCO2 ou TWh

# Deux régimes que l'intitulé classe mal, et que l'écart de reconstruction
# identifie sans ambiguïté : après correction, les produits concernés tombent
# exactement sur leur valeur déclarée.
CORRECTIONS = {
    "Méthane": "Non combustible",      # méthane fugitif et agricole, hors combustion
    "Gaz de raffinerie": "Pétrole",    # produit de raffinage, pas gaz naturel
}

# Résidu non résolu, périmètre carbone, cellule de tarif nul uniquement — les
# onze seules cellules qui résistent. Le signe est constant : `Non combustible`
# est prédit trop haut de 2,06 à 2,49 MtCO2 selon le millésime, `Pétrole` trop
# bas d'autant. Un régime aujourd'hui rangé en `Non combustible` appartient donc
# au pétrole.
#
# Piste non concluante : `CO2 non énergétique` (0,4626) + `CO2 non énergétique
# procédés industriels` (1,6173) somment à 2,0799 en 2023 contre un résidu de
# 2,0590 — proche, hors tolérance, et non vérifié sur les autres millésimes.
#
# Piste écartée : le rapport résidu / « Autres produits pétroliers » est stable
# (0,247 à 0,295), ce qui suggérait une part d'usages non énergétiques dans ce
# régime. Mais le signe l'interdit — il faudrait *retirer* de `Non combustible`,
# pas y ajouter. La stabilité du ratio est une coïncidence d'échelle.
PART_NON_ENERGETIQUE = {}
TARIF_NUL_SEULEMENT = set()

PREFIXES = [
    (("charbon",), "Charbon"),
    (("gaz -", "gaz de raffinerie", "méthane - production"), "Gaz"),
    (("bois de chauffage", "chaleur"), "Chaleur et biomasse"),
    (("méthane", "co2 énergétique incinération"), "Déchets et biomasse"),
    (("co2 non énergétique", "hfc", "n2o", "autres gaz fluorés"), "Non combustible"),
    (("autres produits pétroliers", "e10", "e85", "essence", "fioul", "gpl", "gazole",
      "kerosene"), "Pétrole"),
    (("aéroports", "consommations", "datacenters", "electricité", "installations hyper",
      "pertes réseau", "transport de personnes", "exemption", "exonération"), "Électricité"),
]


def lire_intitule(regime):
    """Le produit déduit du seul intitulé. Fiable, mais pas suffisant."""
    minuscule = regime.lower()
    for prefixes, produit in PREFIXES:
        if minuscule.startswith(prefixes):
            return produit
    return None


def charger():
    v = pd.read_csv(os.path.join(ASSETS, "elfe.csv"))
    v["tarif"] = v["tarif"].round(PRECISION_CLE)
    return v[v.dimension == "Régime fiscal"], v[v.dimension == "Type de produit"]


def observer(reg, prod):
    """Mapping mesuré dans les deux sens sur les cellules dégénérées."""
    vus = {}
    n_prod = prod.groupby(K)["categorie"].nunique()
    n_reg = reg.groupby(K)["categorie"].nunique()
    p, r = prod.set_index(K), reg.set_index(K)
    for cle in n_prod[n_prod == 1].index:
        produit = p.loc[[cle], "categorie"].iloc[0]
        for regime in r.loc[[cle], "categorie"]:
            vus.setdefault(regime, set()).add(produit)
    for cle in n_reg[n_reg == 1].index:
        regime = r.loc[[cle], "categorie"].iloc[0]
        if cle in p.index:
            for produit in p.loc[[cle], "categorie"]:
                vus.setdefault(regime, set()).add(produit)
    return vus


def parts_observees(reg, prod):
    """Part de chaque produit dans un régime, par millésime, sur cellules à régime unique."""
    n_reg = reg.groupby(K)["categorie"].nunique()
    etiquette = reg.set_index(K)["categorie"]
    etiquette = etiquette[~etiquette.index.duplicated()]
    d = prod.set_index(K)
    d = d[d.index.isin(n_reg[n_reg == 1].index)].reset_index()
    d["regime"] = d.set_index(K).index.map(etiquette)
    t = d.groupby(["regime", "millesime", "categorie"])["quantite"].sum()
    return (t / t.groupby(["regime", "millesime"]).sum()).rename("part").reset_index()


def construire(perimetre, reg, prod):
    """Mapping final : observé > intitulé > correction, plus les parts de partage."""
    vus = observer(reg, prod)
    purs = {k: next(iter(w)) for k, w in vus.items() if len(w) == 1}
    partages = {k for k, w in vus.items() if len(w) > 1}

    lignes, mapping = [], {}
    for regime in sorted(reg.categorie.unique()):
        if regime in CORRECTIONS:
            mapping[regime], source = CORRECTIONS[regime], "correction"
        elif regime in purs:
            mapping[regime], source = purs[regime], "observe"
        else:
            mapping[regime], source = lire_intitule(regime), "intitule"
        if regime not in partages:
            lignes.append((perimetre, regime, mapping[regime], "", 1.0, source))

    table = parts_observees(reg, prod)
    parts = {}
    for regime, millesime, produit, valeur in table.itertuples(index=False):
        if regime in partages:
            parts[(regime, millesime, produit)] = valeur
            lignes.append((perimetre, regime, produit, millesime, valeur, "observe"))

    for regime, (produit, valeur) in PART_NON_ENERGETIQUE.get(perimetre, {}).items():
        if regime in mapping:
            partages.add(regime)
            principal = mapping[regime]
            for millesime in sorted(reg.millesime.unique()):
                parts[(regime, millesime, produit)] = valeur
                parts[(regime, millesime, principal)] = 1 - valeur
            lignes = [x for x in lignes if x[1] != regime]
            lignes += [(perimetre, regime, produit, "", valeur, "residu"),
                       (perimetre, regime, principal, "", 1 - valeur, "residu")]

    return mapping, partages, parts, lignes


def reconstruire(reg, prod, mapping, partages, parts):
    """Somme les régimes selon le mapping et confronte à la ventilation déclarée."""
    r, p = reg.set_index(K), prod.set_index(K)
    resultats = []
    for cle in p.index.unique():
        if cle not in r.index:
            continue
        attendu = p.loc[[cle]].set_index("categorie")["quantite"]
        predit = {}
        for regime, q in r.loc[[cle]][["categorie", "quantite"]].itertuples(index=False):
            eclate = {c: parts.get((regime, cle[1], c)) for c in attendu.index}
            eclate = {c: x for c, x in eclate.items() if x}
            applicable = regime not in TARIF_NUL_SEULEMENT or cle[2] == 0
            if regime in partages and applicable and abs(sum(eclate.values(), 0.0) - 1) < 1e-6:
                for c, x in eclate.items():
                    predit[c] = predit.get(c, 0.0) + q * x
            else:
                predit[mapping[regime]] = predit.get(mapping[regime], 0.0) + q
        ecart = max(abs(predit.get(c, 0.0) - attendu.get(c, 0.0))
                    for c in set(predit) | set(attendu.index))
        resultats.append((cle, ecart, float(attendu.sum())))
    return resultats


def main():
    reg_tout, prod_tout = charger()
    lignes = []
    for perimetre in ["Carbone", "Energie"]:
        reg = reg_tout[reg_tout.perimetre == perimetre]
        prod = prod_tout[prod_tout.perimetre == perimetre]
        mapping, partages, parts, bloc = construire(perimetre, reg, prod)
        lignes += bloc

        manquants = [k for k, w in mapping.items() if w is None]
        resultats = reconstruire(reg, prod, mapping, partages, parts)
        ok = [x for x in resultats if x[1] <= TOLERANCE]
        masse = sum(x[2] for x in resultats)
        print(f"##### {perimetre} : {len(reg.categorie.unique())} régimes, "
              f"{len(partages)} partagés, {len(manquants)} sans produit #####")
        print(f"   reconstruction sous {TOLERANCE} : {len(ok)}/{len(resultats)} cellules "
              f"({100 * len(ok) / len(resultats):.1f} %), "
              f"{100 * sum(x[2] for x in ok) / masse:.1f} % de la masse")
        for cle, ecart, _ in sorted(resultats, key=lambda x: -x[1])[:3]:
            if ecart > TOLERANCE:
                print(f"      reste  {ecart:8.4f}  {cle[1]:>6s}  tarif {cle[2]:.6f}")

    sortie = pd.DataFrame(lignes, columns=[
        "perimetre", "regime", "produit", "millesime", "part", "source"])
    sortie = sortie.sort_values(["perimetre", "regime", "millesime", "produit"])
    chemin = os.path.join(ASSETS, "regime_produit.csv")
    sortie.to_csv(chemin, index=False, encoding="utf-8")
    print(f"\nregime_produit.csv : {sortie.shape}")
    print(sortie.groupby(["perimetre", "source"]).size().to_string())


if __name__ == "__main__":
    main()
