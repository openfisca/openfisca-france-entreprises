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

**118 tests générés, dont 116 verts et 2 rouges assumés** sous
`openfisca_france_entreprises/tests/taxes/taxes_energies/agregats/` (78 cellules
tarifaires, 30 exonérations). Les fichiers sont générés : ne pas les éditer à la
main.

> ## Depuis la bascule mensuelle, la quantité se pose sur son mois
>
> État au 2026-08-13. Les variables de consommation sont passées en
> `definition_period = MONTH` : le générateur ne répartit donc plus la quantité sur
> l'année, il la pose sur **un mois où le barème porte le tarif que la case déclare**.
> Une case de la 2040-TIC est une cellule tarifaire homogène — elle porte la quantité
> taxée à *son* tarif, qu'elle nomme souvent dans son propre libellé —, et la répartir
> sur douze mois faisait calculer au modèle une moyenne annuelle que la déclaration ne
> pratique jamais.
>
> Cela éteint **cinq rouges** et referme les constats n° 6 et n° 8. Quand aucun mois de
> l'année ne porte le tarif déclaré, la quantité est posée sur janvier : le désaccord
> avec le barème apparaît alors seul, sans être mêlé d'annualisation.

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

Répartition des 2 rouges :

| cas | cellules | constat |
|---|---|---|
| 2 | `_911243` (2024-2025) | n° 3 — tarif SEQE clos trop tôt au barème |

**Les deux derniers tiennent au barème**, et à lui seul : le tarif réduit
`intensive_energie_indirect_SEQE` s'arrête au 2024-01-01 alors que la case le déclare
encore en 2024 et 2025. Il se corrige dans `baremes-ipp-yaml`.

Les constats n° 2, 4, 5, 6, 7, 8 et 9 sont clos : tarifs gaz élucidés, majoration ZNI
appliquée au tarif normal, bouclier lisant le tarif ménages, bascule mensuelle, paliers
d'électro-intensité, hypothèse de consommation uniforme et conversion PCS/PCI.

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

### 2. Gaz naturel combustible : trois tarifs — ✅ élucidés le 2026-08-13

| case | libellé | déclaré | ce que c'est |
|---|---|---|---|
| `_911237` | **TICGN** — tarif plein, au titre de l'année N | 8,43 | taux normal de la TICGN au 1er janvier 2021 (art. 61 LF 2021) |
| `_911264` | tarif plein, au titre de l'année N+1 | 8,41 | tarif normal de l'accise en 2022 (arrêté du 8 septembre 2021) |
| `_911272` | usage combustible, tarif à 8,37 €/MWh | 8,37 | tarif normal de l'accise en 2023 (arrêté du 13 décembre 2022, art. 2) |

Aucun des trois n'était « absent du barème ». Deux causes se cumulaient.

**Le barème confondait une valeur de tableau avec le tarif applicable.** L'article
L312-36 du CIBS porte 8,45 €/MWh, mais son dernier alinéa, dans sa version en vigueur du
1er janvier 2022 au 1er janvier 2024, prévoit que le tarif normal des gaz naturels est ce
montant **minoré de la part de biométhane injectée dans les réseaux**, constatée chaque
année par arrêté. D'où 8,41 en 2022 et 8,37 en 2023. L'arrêté publie même les données du
calcul : 4,3 TWh injectés en 2021 pour 480 TWh consommés, soit `8,45 × (1 − 0,008958) =
8,3743`, arrondi à 8,37. Corrigé au barème.

**Et la 2040-TIC tient deux blocs distincts.** `_911237` est libellée « **TICGN** — Taux
plein », pas « Accise gaz naturels » : c'est une case de régularisation au dernier taux de
la TICGN, celui de 2021, figé sur les quatre millésimes. Elle pointait le paramètre de
l'accise avec `annee_tarif=2022`. Repointée sur `ticgn.taux_normal` en 2021.

`_911264` et `_911272` quittent les lacunes de couverture et sont **vertes** sur tous
leurs millésimes.

`_911237` reste rouge, mais pour une tout autre raison — voir le constat n° 9.

### 3. Gaz : le tarif « risque de fuite de carbone » est clos trop tôt

`gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_indirect_SEQE`
s'arrête au **2024-01-01**. Or la case `_911243` déclare toujours 1,60 €/MWh en
2024 (6 881 031 MWh) et en 2025 (5 761 764 MWh). Le paramètre doit être prolongé,
ou la fermeture justifiée. **Testée et rouge sur 2024 et 2025.**

### 4. Majoration ZNI — ✅ clos le 2026-08-13

`energies.majoration_zni` ne portait qu'une valeur, `2026-02-01 = 5,66`. Les
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

**Ce n'est pas un régime propre aux zones non interconnectées.** L'article L312-37-1 du
CIBS, en vigueur depuis le 1er août 2025, majore les tarifs normaux des combustibles et de
l'électricité d'un montant affecté au financement des ZNI — dû par **tous** les redevables
du tarif normal, son dénominateur étant la consommation d'énergie totale du pays. C'est
pourquoi l'arrêté du 13 décembre 2022 publie le « tarif normal majoré » comme chiffre de
tête, et pourquoi la plupart des sources annoncent une accise gaz autour de 16 €/MWh quand
le barème n'en porte que la fraction, 10,54.

Porté le 2026-08-13 :

- le barème reçoit la valeur manquante, `2025-08-01 = 4,89`, et les cinq séries de tarifs
  normaux portent une note renvoyant vers `majoration_zni` ;
- le helper `majoration_zni` de `formula_helpers.py` l'ajoute au tarif normal de
  l'électricité, du charbon et du gaz combustible — jamais aux tarifs réduits, que
  L312-37-1 ne vise pas, ni au gaz carburant, qui n'est pas une catégorie combustible ;
- trois des quatre cases quittent les lacunes de couverture et sont **vertes**. Le
  générateur pose leur quantité sur **2025-08**, mois qu'il identifie seul comme celui où
  le barème porte 15,43 / 29,98 / 25,79.

La quatrième, `_914396` (charbon), reste sans test : elle n'a **aucune ligne au millésime
2025** dans le fichier, et vaut zéro sur 2022-2024. Elle existe au Cerfa mais n'a jamais
été servie.

---

## Constats de modélisation

### 5. Le bouclier tarifaire n'applique jamais le tarif « ménages » — ✅ clos le 2026-08-13

[`variables/boulier_tarifaire.py`](openfisca_france_entreprises/variables/boulier_tarifaire.py)
lit `bouclier_tarifaire.entreprises` dans ses trois formules (2022, 2023, 2024),
sans jamais regarder la catégorie fiscale. Le paramètre
`bouclier_tarifaire.menages` existe et n'est lu nulle part.

Les déclarations distinguent nettement les deux :

| millésime | entreprises | ménages |
|---|---|---|
| 2022 | 0,50 (`_911369`) | 1,00 (`_911371`) |
| 2024 | 20,50 (`_913037`) | 21,00 (`_913035`) |

En 2022, `_911371` porte 136 133 610 MWh : le modèle rendait la moitié du montant
déclaré. Six cas étaient rouges pour ce motif — `_911371` sur les quatre millésimes et
`_913035` sur 2024-2025.

**Corrigé le 2026-08-13.** Les trois formules passent par `_tarif_bouclier`, qui choisit
entre les deux paramètres selon la catégorie fiscale de l'accise : les ménages et
assimilés sont les puissances de raccordement inférieures à 36 kVA, seuil déjà porté par
`ticfe.categorie_fiscale_petite_et_moyenne_entreprise`. Les six cas sont verts.

Ampérage non renseigné : le tarif « entreprises » s'applique. Le modèle décrit des
établissements, pas des ménages ; à défaut de puissance déclarée, c'est le régime de
droit commun de ses redevables — et c'est ce que suppose le test annuel du dépôt, qui
n'indique pas d'ampérage et attend 20,50.

Le contournement `Instant((AAAA, 2, 1))` est conservé : la variable reste annuelle, le
bouclier prenant effet au 1er février. Son traitement mensuel est un chantier distinct,
recensé au point 11 d'`ACTIONS_EN_ATTENTE.md`.

### 6. Le pas tarifaire du 1er février est lu au 1er janvier — ✅ clos le 2026-08-13

Les tarifs normaux d'électricité changent au 1er février (32,0625 → 33,70 en 2025).
Les variables étant en `definition_period = YEAR`, `parameters(period)` rend la
valeur du 1er janvier. Le modèle applique donc 32,0625 là où les déclarations
appliquent 33,70 (`_914195`) et 26,23 (`_914197`).

Le contournement existait dans le dépôt — les formules du bouclier forçaient
`Instant((AAAA, 2, 1))` — mais il n'était pas appliqué aux tarifs normaux.

**Clos par la bascule mensuelle.** Les variables de consommation étant en
`definition_period = MONTH`, la quantité de `_914195` et `_914197` se pose sur un mois
où s'applique le tarif déclaré, et le modèle le restitue. Les deux cas sont verts. Le
contournement `Instant((AAAA, 2, 1))` subsiste dans le seul bouclier tarifaire, où il
tient lieu de tout autre chose — voir le constat n° 5 et le point 11
d'`ACTIONS_EN_ATTENTE.md`.

### 7. Bornes des tranches d'électro-intensité — ✅ arbitré le 2026-08-13

Les taux concordent (7,5 / 5 / 2 €/MWh, cases `_911331` / `_911329` / `_911327`).
Les **bornes** divergent :

- la déclaration découpe à **1,5 et 3** kWh par € de valeur ajoutée ;
- `taxe_accise_electricite_electro_intensive_activite_industrielle` découpe à
  **0,5 et 3,375**.

Les paramètres aux bornes de la déclaration existent au barème
(`electricite/ticfe/electro_intensive/seuil_1_5_kwh_par_va` et `seuil_3_kwh_par_va`)
mais ne servent que les formules TICFE antérieures à 2022.

**Arbitré : les deux grilles ne sont pas commensurables, et le libellé de la
déclaration est périmé.**

L'article L312-65 du CIBS fixe des **niveaux minimaux d'électro-intensité exprimés en
pourcentage** — 0,5 %, 3,375 %, 6,75 % pour l'activité industrielle, plus 13,5 % pour la
concurrence internationale. Et l'électro-intensité n'est pas une consommation par euro :
le dernier alinéa de L312-45 la définit comme le niveau d'intensité énergétique en valeur
ajoutée du 2° de L312-44, apprécié sur la seule électricité, soit le quotient entre le
**montant d'accise au tarif normal haute puissance** et la valeur ajoutée. C'est un
rapport euros sur euros, sans dimension.

Les bornes « 1,5 et 3 kWh par € de VA » du libellé sont celles de la **TICFE d'avant
2022** (article 266 quinquies C du code des douanes). Le Cerfa a gardé le vocabulaire
alors que les tarifs qu'il porte — 7,5 / 5 / 2 — sont ceux du CIBS. Il n'y a donc pas de
divergence de droit à trancher : il y a un libellé qui n'a pas suivi la recodification.

Conséquences portées le 2026-08-13 :

- le barème exprime les paliers en proportion (0,005 / 0,03375 / 0,0675 / 0,135) et les
  place sous `electricite/accise/tarifs_reduits/electro_intensives/seuils/niveau_*` ;
- `taxe_accise_electricite_electro_intensive_activite_industrielle` lisait `niveau_0_5`
  comme un **plafond** et non comme un minimum : ses trois bandes étaient décalées d'un
  cran, `niveau_6_75` n'était jamais lu, et une électro-intensité nulle ouvrait le tarif
  le plus favorable. Corrigé ;
- sous 0,5 %, la condition du 1° des articles L312-71 à L312-73 n'est pas remplie : les
  deux formules replient désormais sur le tarif normal, là où elles rendaient zéro ;
- les entrées `electro_intensite` de `correspondance.py` et des tests écrits à la main
  étaient exprimées dans l'ancienne unité ; elles sont ramenées à des proportions.

Les huit cellules `_911327` / `_911329` / `_911331` sont vertes.

### 8. L'hypothèse de consommation uniforme, contredite par les déclarations — ✅ clos le 2026-08-13

État au 2026-08-12, après fusion de `feat/periodes-mensuelles` (merge `e18a6b7`).
Constat apparu avec cette fusion — trois cellules qui passaient échouaient alors :

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
ponctuel, pas par correction : il casserait si le pas se déplaçait. **Cela reste vrai
après la bascule** — le bouclier est le seul dispositif à conserver ce contournement,
faute d'un traitement mensuel de son basculement de régime.

**Ce qu'il ne faut pas faire.** Recalculer les attendus sur la moyenne mensuelle.
Ce sont des montants déclarés : ils vérifient le droit. Les aligner sur la
convention d'annualisation du modèle graverait cette convention dans des valeurs
censées la contrôler, et le test cesserait de tester quoi que ce soit de légal.

**La vraie réponse était** `definition_period = MONTH` sur les variables énergies.
**Elle est appliquée depuis le 2026-08-13** : les 106 variables de quantité —
consommations et assiettes — sont mensuelles, avec `set_input_divide_by_period`, et la
taxe de l'année est la somme des taxes mensuelles. `tarif_moyen_annuel` a cédé la place
à `accise_annuelle` et `tarif_du_mois`.

Le générateur pose désormais la quantité de chaque case sur un mois où s'applique le
tarif qu'elle déclare. Les trois cellules ci-dessus sont vertes, ainsi que `_914195` et
`_914197` du constat n° 6. `_911243` 2025, qui cumulait ce constat et celui du barème,
ne porte plus que le second : son rapport passe de 9,00 à 10,72, soit exactement
16,37 / 1,60 puis 17,16 / 1,60.

Trois régimes restent volontairement annuels, leurs bornes mordant sur le cumul de
l'année et non sur chaque mois — le seuil d'exonération et l'abattement de la TICGN
d'avant 2008, le plafond de 1 GWh des centres de stockage de données, et le bouclier
tarifaire, qui encode un basculement de régime et non un changement de tarif.

*À noter pour la suite* : les agrégats Elfe (`ELFE.md`) demandent l'inverse. Elfe
publie des tarifs **déjà moyennés sur l'année**, donc `tarif_moyen_annuel` lui
convient. Une variable annuelle ne peut pas servir les deux sources ; la bascule
mensuelle est ce qui les réconcilie, puisqu'elle permet de moyenner à la demande
sans figer la convention dans les formules.

### 9. Le facteur PCS/PCI de 1,11 — ✅ arbitré le 2026-08-13

Mesuré en remappant `_911237` sur la TICGN, puis tranché.

`taxe_interieure_consommation_gaz_naturel_taux_normal.formula_2014_01_01` multiplie le
taux normal par `energies.gaz_naturel.ticgn.conversion_pcs_pci`, soit **1,11**, pour
convertir un tarif exprimé en €/MWh PCI vers une assiette en MWh PCS. Le commentaire qui
l'accompagne porte depuis toujours un « ***faut vérrifier », et `ACTIONS_EN_ATTENTE.md` le
liste en décision humaine n° 4.

La déclaration tranche. Sur `_911237`, elle applique **8,4300 tout rond** :

| millésime | quantité (MWh) | montant (€) | rapport |
|---|---|---|---|
| 2022 | 58 552 445 | 493 597 111,35 | 8,4300 |
| 2023 | 1 615 957 | 13 622 518 | 8,4300 |
| 2024 | 14 784 040 | 124 629 457 | 8,4300 |
| 2025 | 529 315 | 4 462 125 | 8,4300 |

Le modèle, lui, rend `8,43 × 1,11 = 9,3573`. Le rapport modèle/déclaration vaut
**exactement 1,11 sur les quatre millésimes**, sans résidu : `493 597 120 × 1,11 =
547 892 803` contre `547 892 800` calculés. Il n'y a donc pas d'autre écart caché derrière
celui-ci.

**Arbitrage : la conversion n'a pas lieu d'être.** La question « les données sont-elles en
PCS ou en PCI ? » est mal posée, parce qu'elle suppose une unité fixe. Les données
déclarées **changent de nature en même temps que la loi** : quand le texte exprime le tarif
en PCS, l'assiette déclarée est en PCS ; quand il l'exprime en PCI, elle est en PCI. Il n'y
a donc jamais deux unités à réconcilier, et chaque millésime se lit dans l'unité de son
propre droit.

Le facteur est retiré des trois sites qui l'appliquaient — la formule 2014 de la TICGN et
les deux formules d'intensité énergétique en valeur ajoutée. Le paramètre
`conversion_pcs_pci` reste au barème : le coefficient physique existe, il n'a simplement
pas à intervenir dans la liquidation.

Les quatre cellules `_911237` sont vertes. L'attendu du test d'intensité énergétique, qui
incorporait le 1,11, passe de 0,561676 à **0,5428** — `(22 500 + 14 620 + 17 160) / 100 000`.
C'est le seul attendu recalculé de tout le chantier, et c'en est un écrit à la main, pas un
montant déclaré.

Ferme du même coup la décision humaine n° 4 d'`ACTIONS_EN_ATTENTE.md` et l'arbitrage §7
d'`ARBITRAGES_JURIDIQUES_ENERGIES.md`, qui traînaient un `***faut vérrifier` depuis
l'origine.

---

## Lacunes de couverture

Les **3 cellules non testées** — le modèle n'ayant ni variable ni entrée pour
elles, il n'y a rien à confronter. À distinguer des 6 rouges, qui sont des
désaccords chiffrés : ici le calculateur ne répond pas du tout.

`_911321` et `_911323` (indexation TCFE, constat n° 1), `_912995` (manutention portuaire).

Six cellules en sont sorties le 2026-08-13 : les quatre ZNI (constat n° 4 — trois testées
et vertes, la quatrième sans donnée) et `_911264` / `_911272`, une fois la série de
l'accise gaz corrigée au barème (constat n° 2).

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
2. ~~Arbitrer les points 5 à 7 (modèle), de même. Le point **5 vaut 6 rouges**~~
   Point 5 **fait le 2026-08-13** : `boulier_tarifaire.py` lit `bouclier_tarifaire.menages`
   sous 36 kVA, ce qui éteint `_911371` ×4 et `_913035` ×2. Restent les points 6 et 7,
   qui ne valent aucun rouge — le 7 (bornes des tranches d'électro-intensité) demande un
   arbitrage contre l'article L312-65, les agrégats ne le tranchant pas seuls.
3. ~~**Basculer les variables énergies en `definition_period = MONTH`** (point 8).~~
   **Fait le 2026-08-13** : 5 rouges éteints (`_914195`, `_914197`, `_911293`,
   `_911319`, `_914201`), points 6 et 8 clos, et la source réconciliée avec les agrégats
   Elfe — une quantité fournie à l'année reste répartie sur douze mois, ce qui redonne
   la moyenne dont Elfe a besoin. Le contournement `Instant((AAAA, 2, 1))` subsiste
   dans le seul bouclier tarifaire : il y encode un basculement de régime, dont le
   traitement mensuel est un chantier distinct.
4. Cartographier les majorations TCCFE de janvier 2023.
5. Élucider les deux écarts de ventilation avec le producteur du fichier micro.
