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

**108 tests générés, dont 91 verts et 17 rouges assumés** sous
`openfisca_france_entreprises/tests/taxes/taxes_energies/agregats/` (78 cellules
tarifaires, 30 exonérations). Les fichiers sont générés : ne pas les éditer à la
main.

> ## La suite est rouge, et il ne faut pas la « réparer »
>
> **Toute cellule que le modèle sait calculer est émise**, y compris — surtout —
> quand son résultat contredit la déclaration. Ces cas portent une annotation
> `DÉSACCORD` dans le YAML généré, qui en dit la nature et renvoie au constat
> correspondant.
>
> Le principe du chantier est que **la déclaration fiscale a raison, et que le
> calculateur comme le barème peuvent avoir tort**. Un désaccord rangé hors du
> chemin est un désaccord tu : c'est précisément ce que ces données servent à
> éviter.
>
> **Ne pas recalculer ces attendus sur ce que rend le modèle.** Ce sont des
> montants réellement déclarés par les redevables ; ils vérifient le droit. Les
> aligner sur le calcul ferait disparaître le désaccord au lieu de le résoudre, et
> le test cesserait de tester quoi que ce soit de légal.

Répartition des 17 rouges :

| cas | cellules | constat |
|---|---|---|
| 4 | `_911237` (2022-2025) | n° 2 — tarif gaz 8,43 absent du barème |
| 2 | `_911243` (2024-2025) | n° 3 — tarif SEQE clos trop tôt au barème |
| 4 | `_911371` (2022-2025) | n° 5 — le bouclier ne lit jamais le tarif ménages |
| 2 | `_913035` (2024-2025) | n° 5 — idem |
| 2 | `_914195`, `_914197` (2025) | n° 6 — pas du 1er février lu au 1er janvier |
| 3 | `_911293`, `_911319`, `_914201` (2025) | n° 8 — tarif infra-annuel moyenné |

Six d'entre eux mettent en cause le **barème** (n° 2 et n° 3), onze le **modèle**.

Seules restent écartées les **9 cellules pour lesquelles le modèle n'a ni variable
ni entrée** : il n'y a alors rien à confronter. Ce sont des lacunes de couverture,
recensées plus bas et remontées par `audit.py`.

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

`_911237` est **testée et rouge sur les quatre millésimes**. Les deux autres cases
n'ont pas de variable au modèle : `_911264` (acomptes N+1) relève d'une notion
absente, `_911272` d'une lacune de couverture.

### 3. Gaz : le tarif « risque de fuite de carbone » est clos trop tôt

`gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_indirect_SEQE`
s'arrête au **2024-01-01**. Or la case `_911243` déclare toujours 1,60 €/MWh en
2024 (6 881 031 MWh) et en 2025 (5 761 764 MWh). Le paramètre doit être prolongé,
ou la fermeture justifiée. **Testée et rouge sur 2024 et 2025.**

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
déclaré. **Six cas sont rouges pour ce motif** — `_911371` sur les quatre
millésimes et `_913035` sur 2024-2025.

### 6. Le pas tarifaire du 1er février est lu au 1er janvier

Les tarifs normaux d'électricité changent au 1er février (32,0625 → 33,70 en 2025).
Les variables étant en `definition_period = YEAR`, `parameters(period)` rend la
valeur du 1er janvier. Le modèle applique donc 32,0625 là où les déclarations
appliquent 33,70 (`_914195`) et 26,23 (`_914197`).

Le contournement existe déjà dans le dépôt — les formules du bouclier forcent
`Instant((AAAA, 2, 1))` — mais il n'est pas appliqué aux tarifs normaux.
**`_914195` et `_914197` sont testées et rouges sur 2025.**

Depuis la fusion de `feat/periodes-mensuelles`, ces tarifs passent par
`tarif_moyen_annuel` : le modèle ne rend plus la valeur du 1er janvier mais la
moyenne des douze mois. Le désaccord change de forme, pas de nature — voir le
constat n° 8, qui le généralise et donne la seule sortie durable.

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

### 8. L'hypothèse de consommation uniforme, contredite par les déclarations

État au 2026-08-12, après fusion de `feat/periodes-mensuelles` (merge `e18a6b7`).
Constat apparu avec cette fusion — trois cellules qui passaient échouent désormais :

| case | énergie | an | déclaré | moyenne mensuelle | écart |
|---|---|---|---|---|---|
| `_914201` | gaz naturel combustible | 2025 | 17,1600 | 14,4017 | **−16,07 %** |
| `_911293` | charbon, tarif plein | 2025 | 14,6200 | 12,9200 | **−11,63 %** |
| `_911319` | électricité > 250 kVA | 2025 | 22,5000 | 21,8333 | **−2,96 %** |

Le rapport résultat/attendu vaut **exactement** moyenne ÷ tarif déclaré.
`tarif_moyen_annuel` fonctionne donc comme spécifié : c'est sa spécification qui
est en cause. Son docstring la pose sans détour — « La consommation étant répartie
uniformément sur l'année ».

**La déclaration falsifie cette hypothèse.** Elle ne moyenne jamais : elle ségrège
les tarifs en cases distinctes, et une case porte la quantité taxée à *son* tarif.
`_914201` s'intitule littéralement « Usage combustible : **tarif à 17,16 €/MWh** » —
elle nomme son propre tarif. La 2040-TIC publie donc la répartition infra-annuelle
réelle, c'est-à-dire précisément l'information que l'hypothèse d'uniformité
suppose absente.

**Le barème n'est pas en cause, et c'est vérifié.**
`gaz_naturel/accise/combustibles/tarif_normal.yaml` porte 17,16 au `2025-01-01`
puis 10,54 au `2025-08-01`, sur l'article 20 de la loi 2025-127 du 14 février 2025.
Deux corroborations indépendantes :

- la déclaration 2025 ne comporte **aucune** case métropole à 10,54 — cohérent,
  le millésime est l'année de dépôt et la période post-août se déclarera en 2026 ;
- la case ZNI `_914387` / `_914388` / `_914389` décompose 15,43 = **10,54** + 4,89,
  ce qui confirme la valeur post-août par une autre voie.

**Une quatrième cellule échappe au problème, pour une mauvaise raison.**
`_913037` (bouclier, 2024) voit aussi son tarif varier dans l'année — 0,50 en
janvier, 20,50 ensuite, moyenne 18,8333 — mais ses formules forcent
`Instant((AAAA, 2, 1))` et lisent donc 20,50. Le test passe par contournement
ponctuel, pas par correction : il casserait si le pas se déplaçait. C'est le même
contournement que celui relevé au constat n° 6.

**Ce qu'il ne faut pas faire.** Recalculer les attendus sur la moyenne mensuelle.
Ce sont des montants déclarés : ils vérifient le droit. Les aligner sur la
convention d'annualisation du modèle graverait cette convention dans des valeurs
censées la contrôler, et le test cesserait de tester quoi que ce soit de légal.

**La vraie réponse** est `definition_period = MONTH` sur les variables énergies.
La branche `origin/refactor/energies-periodes-mensuelles` (9 commits d'avance sur
`main`) porte déjà le terrain : `formula_helpers.py`,
`taxation_autres_produits_energetiques.py`, `taxation_charbon.py`,
`taxation_electricite.py`, `taxation_gaz_naturel.py`. Une fois la bascule faite, la
2040-TIC devient testable au mois — chaque case sur les mois où son tarif
s'applique — et ce constat se referme, avec le n° 6 et le contournement du
bouclier.

*À noter pour la suite* : les agrégats Elfe (`ELFE.md`) demandent l'inverse. Elfe
publie des tarifs **déjà moyennés sur l'année**, donc `tarif_moyen_annuel` lui
convient. Une variable annuelle ne peut pas servir les deux sources ; la bascule
mensuelle est ce qui les réconcilie, puisqu'elle permet de moyenner à la demande
sans figer la convention dans les formules.

---

## Lacunes de couverture

Les **9 cellules non testées** — le modèle n'ayant ni variable ni entrée pour
elles, il n'y a rien à confronter. À distinguer des 17 rouges, qui sont des
désaccords chiffrés : ici le calculateur ne répond pas du tout.

`_911264` (acomptes N+1), `_911272` (tarif gaz 8,37), `_911321` et `_911323`
(indexation TCFE, constat n° 1), `_912995` (manutention portuaire), `_914374`,
`_914377`, `_914387` et `_914396` (majoration ZNI 2025, constat n° 4).

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

Chaque suite ci-dessous se mesure au nombre de rouges qu'elle éteint. La suite
n'est verte que lorsque le calculateur et le barème rejoignent la déclaration.

1. Arbitrer les points 1 à 4 (barème) contre les textes, puis porter les
   corrections sur une branche dédiée — cette branche ne modifie ni `variables/`
   ni `parameters/`. Les points **2 et 3 valent 6 rouges** (`_911237` ×4,
   `_911243` ×2) et se corrigent dans `baremes-ipp-yaml` avant d'être repris ici.
2. Arbitrer les points 5 à 7 (modèle), de même. Le point **5 vaut 6 rouges**
   (`_911371` ×4, `_913035` ×2) : `boulier_tarifaire.py` doit lire
   `bouclier_tarifaire.menages` selon la catégorie fiscale.
3. **Basculer les variables énergies en `definition_period = MONTH`** (point 8).
   **Vaut 5 rouges** (`_914195`, `_914197`, `_911293`, `_911319`, `_914201`) :
   c'est ce qui referme les points 6 et 8 d'un coup, supprime le contournement
   `Instant((AAAA, 2, 1))` du bouclier, et réconcilie cette source avec les
   agrégats Elfe. Terrain déjà défriché sur
   `origin/refactor/energies-periodes-mensuelles`.
4. Cartographier les majorations TCCFE de janvier 2023.
5. Élucider les deux écarts de ventilation avec le producteur du fichier micro.
