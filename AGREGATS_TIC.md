# Agrégats 2040-TIC : confrontation au barème et au modèle

État au 2026-07-30. Branche `assets/agregats-tic`, rebasée sur `convergence/energies` (PR #26).

## Ce que sont les données

`assets/agregats.csv` porte les agrégats annuels de la déclaration **2040-TIC**
déposée par les fournisseurs d'énergie, construits depuis le fichier micro et
sommés à l'année. Millésimes 2022 à 2025, 220 cases, 850 lignes, 3 106 à 3 234
déclarants selon l'année.

Colonnes : `millesime`, `case` (numéro de case Cerfa), `sum` (somme sur tous les
redevables), `label` (libellé de la case), `ntot` (nombre de déclarants).

> Le millésime est **l'année de dépôt**, pas l'année de consommation. Une case
> ouverte pour un tarif donné continue de le porter les années suivantes, pour les
> régularisations : c'est pourquoi la case `_911237` affiche 8,43 €/MWh sur les
> quatre millésimes alors que le tarif du gaz, lui, passe de 8,45 à 17,16.

## Pourquoi ces agrégats testent le modèle

Chaque case est une **cellule tarifaire homogène** : un couple (produit, régime,
tarif). L'accise y étant strictement linéaire — pas de seuil, pas de franchise, pas
de barème progressif à l'intérieur d'une cellule — le rapport `montant / quantité`
restitue le tarif légal exact, et il est identique quel que soit le nombre de
redevables agrégés.

Vérification empirique : sur les 61 couples quantité/montant appariables, le
rapport est constant à la quatrième décimale sur les quatre millésimes. Exemple,
case `_911235` (gaz naturel carburant) :

| millésime | quantité (MWh) | montant (€) | rapport |
|---|---|---|---|
| 2022 | 5 789 178 | 30 277 400,94 | 5,2300 |
| 2023 | 5 977 829 | 31 264 045,67 | 5,2300 |
| 2024 | 6 224 511 | 32 554 192,53 | 5,2300 |
| 2025 | 4 900 549 | 25 629 871,27 | 5,2300 |

Un agrégat se comporte donc exactement comme un redevable unique : on injecte la
quantité déclarée comme assiette, on attend le montant déclaré. C'est ce qui rend
ces données utilisables comme cas de test, adossés à des déclarations effectives
plutôt qu'à des montants recalculés à la main.

Trente cases supplémentaires portent des quantités **sans montant** — exonérations
et exemptions. Elles fournissent la famille de tests symétrique : assiette non
nulle, accise nulle.

## Outillage

    scripts/agregats_tic/
      donnees.py         lecture, appariement quantité/montant, tarifs implicites,
                         lecture directe des YAML de paramètres
      correspondance.py  table cases → paramètre du barème / variable / entrées
      audit.py           confrontation au barème (CLI)
      generer_tests.py   génération des tests YAML (CLI)
      arbitrages/        cas en échec volontaire, hors CI

```bash
.venv/bin/python -m scripts.agregats_tic.audit
.venv/bin/python -m scripts.agregats_tic.generer_tests
PYTEST_ADDOPTS="--maxfail=300" .venv/bin/openfisca test \
    openfisca_france_entreprises/tests/taxes/taxes_energies/agregats/ \
    -c openfisca_france_entreprises
```

`addopts` du dépôt contient `--exitfirst` : sans `PYTEST_ADDOPTS`, le lancement
s'arrête au premier échec.

**94 tests générés, tous verts** sous
`openfisca_france_entreprises/tests/taxes/taxes_energies/agregats/` (64 cellules
tarifaires, 30 exonérations). Les fichiers sont générés : ne pas les éditer à la
main.

Les cellules dont le tarif déclaré ne concorde pas avec le barème, ou que le
modèle ne restitue pas, **ne sont pas émises en tests**. Les figer en attendus
rendrait le désaccord invisible ; les laisser en échec casserait la CI. Elles sont
consignées ci-dessous et remontées par `audit.py`.

---

## Écarts entre tarif déclaré et barème

### 1. Électricité : l'indexation des TCFE n'est pas appliquée

Le constat le plus net, et le seul qui touche des masses importantes.

| case | régime | déclaré | barème | écart |
|---|---|---|---|---|
| `_911321` | puissance de raccordement < 250 kVA | 25,8291 | 25,6875 | +0,1416 |
| `_911323` | activités économiques, puissance > 36 kVA | 23,6097 | 23,5625 | +0,0472 |

Les deux tarifs se décomposent en une part d'accise (22,50 €/MWh) et une part
TCFE. En isolant celle-ci :

| | part TCFE au barème | part TCFE déclarée | rapport |
|---|---|---|---|
| `_911321` | 3,1875 | 3,3291 | **1,044424** |
| `_911323` | 1,0625 | 1,1097 | **1,044424** |

Le même facteur, à six décimales, sur deux régimes distincts. Il ne s'agit donc pas
de deux erreurs indépendantes mais d'**un coefficient de revalorisation 2022 que le
barème n'applique pas** aux tarifs normaux d'électricité. Les valeurs
`tarifs_normaux.menages_et_assimiles` et `tarifs_normaux.pme_activites_economiques`
figent la part TCFE à sa valeur non indexée.

*À faire* : retrouver le coefficient réglementaire de revalorisation 2022 et
décider s'il se porte en paramètre distinct ou s'intègre aux tarifs normaux.

### 2. Gaz naturel combustible : trois tarifs absents du barème

| case | libellé | déclaré | barème |
|---|---|---|---|
| `_911237` | tarif plein, au titre de l'année N | 8,43 | 8,45 |
| `_911264` | tarif plein, au titre de l'année N+1 | 8,41 | 8,45 |
| `_911272` | usage combustible, tarif à 8,37 €/MWh | 8,37 | 8,45 |

Les trois sont stables sur les quatre millésimes. `_911272` annonce son tarif dans
son propre libellé, ce qui confirme que 8,37 est bien un tarif de droit et non un
artefact d'agrégation. Aucune des trois valeurs n'existe au barème, qui ne porte
que 8,45 puis 16,37 puis 17,16.

L'écart de 0,02 entre 8,43 et 8,45 est trop régulier pour être du bruit : il porte
sur 58 552 445 MWh en 2022.

### 3. Gaz : le tarif « risque de fuite de carbone » est clos trop tôt

`gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_indirect_SEQE`
s'arrête au **2024-01-01**. Or la case `_911243` déclare toujours 1,60 €/MWh en
2024 (6 881 031 MWh) et en 2025 (5 761 764 MWh). Le paramètre doit être prolongé,
ou la fermeture justifiée.

### 4. Majoration ZNI : absente pour 2025

`energies.majoration_zni` ne porte qu'une valeur, `2026-02-01 = 5,66`. Les
déclarations 2025 appliquent une majoration de **4,89 €/MWh**, isolée dans une case
de montant dédiée, sur les trois énergies :

| énergie | cases | tarif total | fraction | majoration |
|---|---|---|---|---|
| électricité | `_914374` / `_914375` + `_914376` | 29,98 | 25,09 | 4,89 |
| électricité | `_914377` / `_914378` + `_914379` | 25,79 | 20,90 | 4,89 |
| gaz naturel | `_914387` / `_914388` + `_914389` | 15,43 | 10,54 | 4,89 |
| charbon | `_914396` / `_914397` + `_914398` | 15,43 | 10,54 | 4,89 |

Ces cases sont la seule source du dépôt sur la structure ZNI 2025 : le tarif s'y
déclare en deux montants distincts pour une même quantité.

---

## Constats de modélisation

### 5. Le bouclier tarifaire n'applique jamais le tarif « ménages »

[`variables/boulier_tarifaire.py`](openfisca_france_entreprises/variables/boulier_tarifaire.py)
lit `bouclier_tarifaire.entreprises` dans ses trois formules (2022, 2023, 2024),
sans jamais regarder la catégorie fiscale. Le paramètre
`bouclier_tarifaire.menages` existe et n'est lu nulle part.

Les déclarations distinguent nettement les deux :

| millésime | entreprises | ménages |
|---|---|---|
| 2022 | 0,50 (`_911369`) | 1,00 (`_911371`) |
| 2024 | 20,50 (`_913037`) | 21,00 (`_913035`) |

En 2022, `_911371` porte 136 133 610 MWh : le modèle rend la moitié du montant
déclaré. Six cellules sont écartées des tests pour ce motif.

### 6. Le pas tarifaire du 1er février est lu au 1er janvier

Les tarifs normaux d'électricité changent au 1er février (32,0625 → 33,70 en 2025).
Les variables étant en `definition_period = YEAR`, `parameters(period)` rend la
valeur du 1er janvier. Le modèle applique donc 32,0625 là où les déclarations
appliquent 33,70 (`_914195`) et 26,23 (`_914197`).

Le contournement existe déjà dans le dépôt — les formules du bouclier forcent
`Instant((AAAA, 2, 1))` — mais il n'est pas appliqué aux tarifs normaux.

### 7. Bornes des tranches d'électro-intensité : à arbitrer

Les taux concordent (7,5 / 5 / 2 €/MWh, cases `_911331` / `_911329` / `_911327`).
Les **bornes** divergent :

- la déclaration découpe à **1,5 et 3** kWh par € de valeur ajoutée ;
- `taxe_accise_electricite_electro_intensive_activite_industrielle` découpe à
  **0,5 et 3,375**.

Les paramètres aux bornes de la déclaration existent au barème
(`electricite/ticfe/electro_intensive/seuil_1_5_kwh_par_va` et `seuil_3_kwh_par_va`)
mais ne servent que les formules TICFE antérieures à 2022.

Aucune cellule déclarée ne tombe dans les bandes litigieuses `[0,5 ; 1,5[` ou
`[3 ; 3,375[` : les agrégats ne tranchent pas seuls. Deux cas construisent la
situation manquante dans
[`scripts/agregats_tic/arbitrages/test_tranches_electro_intensite.yaml`](scripts/agregats_tic/arbitrages/test_tranches_electro_intensite.yaml)
— **en échec volontaire**, hors CI, à lancer à la demande. À arbitrer contre
l'article L312-65 du code des impositions sur les biens et services.

---

## Lacunes de couverture

- **`electricite_manutention_portuaire`** existe comme variable d'entrée et le
  tarif est au barème (0,5 €/MWh depuis 2023), mais la variable n'est branchée dans
  aucun `select` de l'accise 2022+. La case `_912995` déclare 48 980 MWh en 2024 et
  48 636 en 2025.
- **Acomptes au titre de N+1** : la case `_911264` isole les quantités rattachées à
  l'exercice suivant (181 099 310 MWh en 2022). Le modèle n'a pas cette notion.
- **Majorations TCCFE de janvier 2023** : huit cellules non encore cartographiées
  (`_911310`, `_911312`, `_911394`, `_911396`, `_911398`, `_911400`, `_911467`,
  `_911469`), aux tarifs 2,08 / 1,56 / 6,63 / 6,24 / 4,68 / 2,21 / 9,36 / 3,12
  €/MWh. Chacune annonce son tarif dans son libellé et se recoupe seule. Les deux
  bornes de la grille sont au barème
  (`bouclier_tarifaire.majoration_tccfe_maximum = 9,36` et `..._minimum = 1,56`) ;
  les six échelons intermédiaires n'y sont pas.

## Identités comptables déclarées

Neuf cases TOTAL sont recoupées contre leurs composantes, millésime par millésime.
La composition change chaque année au fil des refontes du Cerfa et se retrouve
exactement : le trou 2023 de `_911239` vaut `_911272` au centime près, celui de
2025 vaut `_912998 + _911272 + _914201 + _914387`.

Sur 34 recoupements, 30 tombent juste (à quelques MWh d'arrondi d'agrégation près).
Quatre résistent :

| case | millésime | écart (MWh) | lecture |
|---|---|---|---|
| `_911358` | 2024 | 13 193 387 (28,6 %) | `_911353` non déclarée cette année-là |
| `_911259` | 2025 | 2 311 324 (4,2 %) | exemptions TICGN non ventilées |
| `_911347` | 2024 | 2 807 | cellule manquante, faible enjeu |
| `_911347` | 2025 | 2 355 | idem |

Les deux premiers méritent d'être élucidés auprès de la source : un total
d'exonérations qui excède la somme de ses composantes signale une ventilation
incomplète dans l'extraction, pas dans le modèle.

## Suites

1. Arbitrer les points 1 à 4 (barème) contre les textes, puis porter les
   corrections sur une branche dédiée — cette branche ne modifie ni `variables/`
   ni `parameters/`.
2. Arbitrer les points 5 à 7 (modèle), de même.
3. Cartographier les majorations TCCFE de janvier 2023.
4. Élucider les deux écarts de ventilation avec le producteur du fichier micro.
