"""Résout ce que `Régime fiscal` détermine des autres dimensions, et le vérifie par les sommes.

Trois dimensions sur cinq se **déduisent** des deux autres, et ce script établit
lesquelles, en confrontant les sommes cellule tarifaire par cellule tarifaire.

  Agents            = regroupement EXACT de `Secteur économique` —
                      Ménages = Transports ménages + Résidentiel ménages,
                      vérifié sur 624/624 et 490/490 cellules, écart max 10⁻¹³.
                      Cette dimension ne porte donc aucune information propre.
  Type de produit   = regroupement de `Régime fiscal`, à l'incorporation de
                      renouvelable près (voir plus bas).
  Gaz à effet de serre = regroupement de `Régime fiscal` : 27/27 régimes observés
                      sont purs.

Ne restent réellement indépendants que **`Régime fiscal` et `Secteur économique`**.
C'est sur ce seul couple que porte l'incertitude résiduelle.

`Régime fiscal` -> `Agents` est en revanche **une relation partielle**, et c'est une
différence de nature : le partage produit/renouvelable est physique et à peu près
constant dans l'année, alors que le partage ménages/entreprises est structurel et
varie d'un palier tarifaire à l'autre — un tarif réduit attire mécaniquement plus
d'entreprises. Environ 72 % des régimes sont purs (et presque tous côté
entreprises) ; les régimes partagés portent l'essentiel de la masse ménages.

Résout la relation `Régime fiscal` -> `Type de produit`, et la vérifie par les sommes.

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
    return v


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


def construire(perimetre, cible, reg, prod):
    """Mapping final : observé > intitulé > correction, plus les parts de partage.

    Le repli sur l'intitulé n'a de sens que pour `Type de produit` : un libellé de
    régime nomme son énergie, jamais son agent. « Gazole - transport routier » ne
    dit pas si le gazole est brûlé par un ménage ou par une entreprise. Pour
    `Agents`, un régime jamais observé reste donc sans valeur, et ses cellules
    sont comptées incalculables plutôt que devinées.
    """
    lisible = cible == "Type de produit"
    vus = observer(reg, prod)
    purs = {k: next(iter(w)) for k, w in vus.items() if len(w) == 1}
    partages = {k for k, w in vus.items() if len(w) > 1}

    lignes, mapping = [], {}
    for regime in sorted(reg.categorie.unique()):
        if lisible and regime in CORRECTIONS:
            mapping[regime], source = CORRECTIONS[regime], "correction"
        elif regime in purs:
            mapping[regime], source = purs[regime], "observe"
        elif lisible:
            mapping[regime], source = lire_intitule(regime), "intitule"
        else:
            mapping[regime], source = None, "inconnu"
        if regime not in partages:
            lignes.append((perimetre, cible, regime, mapping[regime], "", 1.0, source))

    table = parts_observees(reg, prod)
    parts = {}
    for regime, millesime, produit, valeur in table.itertuples(index=False):
        if regime in partages:
            parts[(regime, millesime, produit)] = valeur
            lignes.append((perimetre, cible, regime, produit, millesime, valeur, "observe"))

    return mapping, partages, parts, lignes


def reconstruire(reg, prod, mapping, partages, parts):
    """Somme les régimes selon le mapping et confronte à la ventilation déclarée."""
    r, p = reg.set_index(K), prod.set_index(K)
    resultats = []
    for cle in p.index.unique():
        if cle not in r.index:
            continue
        attendu = p.loc[[cle]].set_index("categorie")["quantite"]
        predit, connu = {}, True
        for regime, q in r.loc[[cle]][["categorie", "quantite"]].itertuples(index=False):
            eclate = {c: parts.get((regime, cle[1], c)) for c in attendu.index}
            eclate = {c: x for c, x in eclate.items() if x}
            if regime in partages and abs(sum(eclate.values(), 0.0) - 1) < 1e-6:
                for c, x in eclate.items():
                    predit[c] = predit.get(c, 0.0) + q * x
            elif mapping.get(regime) is not None:
                predit[mapping[regime]] = predit.get(mapping[regime], 0.0) + q
            else:
                connu = False
        if not connu:
            resultats.append((cle, None, float(attendu.sum())))
            continue
        ecart = max(abs(predit.get(c, 0.0) - attendu.get(c, 0.0))
                    for c in set(predit) | set(attendu.index))
        resultats.append((cle, ecart, float(attendu.sum())))
    return resultats


def controler_agents(v):
    """`Agents` est-il un regroupement exact de `Secteur économique` ?"""
    menages = {"Transports ménages", "Résidentiel ménages"}
    ag = v[v.dimension == "Agents"].set_index(K)
    se = v[v.dimension == "Secteur économique"].set_index(K)
    pire, n = 0.0, 0
    for cle in ag.index.unique():
        if cle not in se.index:
            continue
        n += 1
        declare = ag.loc[[cle]].set_index("categorie")["quantite"]
        secteurs = se.loc[[cle]].set_index("categorie")["quantite"]
        pire = max(
            pire,
            abs(secteurs[secteurs.index.isin(menages)].sum() - declare.get("Ménages", 0.0)),
            abs(secteurs[~secteurs.index.isin(menages)].sum()
                - declare.get("Entreprises et administrations", 0.0)),
        )
    print(f"Agents = Transports ménages + Résidentiel ménages : {n}/{n} cellules, "
          f"écart max {pire:.2e}")
    assert pire < 1e-9, "Agents n'est pas un regroupement exact de Secteur économique"


def main():
    v = charger()
    controler_agents(v)
    reg_tout = v[v.dimension == "Régime fiscal"]

    lignes = []
    for cible in ["Type de produit", "Agents"]:
        cib_tout = v[v.dimension == cible]
        print(f"\n=========== Régime fiscal -> {cible} ===========")
        for perimetre in ["Carbone", "Energie"]:
            reg = reg_tout[reg_tout.perimetre == perimetre]
            cib = cib_tout[cib_tout.perimetre == perimetre]
            mapping, partages, parts, bloc = construire(perimetre, cible, reg, cib)
            lignes += bloc

            inconnus = [k for k, w in mapping.items() if w is None and k not in partages]
            resultats = reconstruire(reg, cib, mapping, partages, parts)
            calculables = [x for x in resultats if x[1] is not None]
            ok = [x for x in calculables if x[1] <= TOLERANCE]
            masse = sum(x[2] for x in calculables) or 1.0
            print(f"  {perimetre} : {reg.categorie.nunique()} régimes, "
                  f"{len(partages)} partagés, {len(inconnus)} jamais observés")
            print(f"     reconstruction sous {TOLERANCE} : {len(ok)}/{len(calculables)} "
                  f"({100 * len(ok) / max(len(calculables), 1):.1f} %), "
                  f"{100 * sum(x[2] for x in ok) / masse:.1f} % de la masse ; "
                  f"{len(resultats) - len(calculables)} incalculables")
            for cle, ecart, _ in sorted(calculables, key=lambda x: -x[1])[:3]:
                if ecart > TOLERANCE:
                    print(f"        reste {ecart:9.4f}  {cle[1]:>6s}  tarif {cle[2]:.6f}")

    sortie = pd.DataFrame(lignes, columns=[
        "perimetre", "dimension", "regime", "categorie", "millesime", "part", "source"])
    sortie = sortie.sort_values(["perimetre", "dimension", "regime", "millesime", "categorie"])
    sortie.to_csv(os.path.join(ASSETS, "regime_mapping.csv"), index=False, encoding="utf-8")
    print(f"\nregime_mapping.csv : {sortie.shape}")
    print(sortie.groupby(["dimension", "perimetre", "source"]).size().to_string())


if __name__ == "__main__":
    main()
