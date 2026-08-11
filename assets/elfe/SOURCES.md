# Résultats du modèle Elfe (CGDD) — source et mode d'obtention

Données extraites le **2026-07-31**. Cette branche ne porte que la donnée : ni
outillage, ni tests, ni modification de `parameters/` ou `variables/`.

## Source

Modèle **Elfe** (tarification effective du carbone et de l'énergie), développé par
le **Commissariat général au développement durable (CGDD)**.
Coordination : Julien Divialle ; réalisation : Guillaume Yatibingui.

Application de visualisation :
<https://ssm-ecologie.shinyapps.io/Tarification_effective_carbone_et_energie/>

Le **code du modèle n'est pas publié** ; seuls les résultats le sont, via cette
application. Source principale amont : base **PEFA** du SDES, vieillie par les
bilans de l'énergie pour les millésimes récents.

## Licence

**etalab-2.0** (mention en pied de l'application). Redistribution autorisée sous
réserve d'attribution — c'est ce qui permet de verser ces fichiers au dépôt.

## Mode d'obtention

L'application n'expose aucun fichier statique : toute l'interface est rendue côté
serveur. L'extraction ouvre une session Shiny en websocket
(`/_w_<worker>/__sockjs__/n=1/<srv>/<sess>/websocket`, trames JSON brutes, sans
encapsulation SockJS), positionne les trois sélecteurs, puis tire le
`downloadHandler` `downloadData`, qui rend le tableau courant en `.xlsx`.

Sélecteurs : `choix_1` (périmètre), `choix_2` (dimension), `choix_3` (millésime).

> **Le script d'extraction n'est pas encore versionné.** Il vit pour l'instant hors
> dépôt. Tant qu'il n'y est pas, ces fichiers ne sont pas reproductibles depuis le
> dépôt seul — à corriger.

## Plan d'expérience

132 combinaisons théoriques, **106 réelles**, toutes extraites. Deux absences,
structurelles et non accidentelles :

| absence | combinaisons | motif |
|---|---|---|
| `Energie` avant 2017 | 18 | le périmètre énergie ne commence qu'en 2017 (HTTP 500 avant) |
| `Energie × Gaz à effet de serre` | 8 | ventiler des consommations d'énergie par GES n'a pas de sens |

Le millésime **`2024*` est provisoire** : son total est *rigoureusement identique* à
celui de 2023 (bilan PEFA non actualisé), mais les tarifs et la ventilation entre
régimes sont, eux, à jour. **Utilisable côté tarifs, pas côté quantités** ; ne pas
le traiter comme une observation indépendante de 2023 dans une analyse pondérée.

## Fichiers

### `elfe.csv` — 9 391 lignes

Tableau long, toutes dimensions sauf `Instruments`.

| colonne | contenu |
|---|---|
| `perimetre` | `Carbone` ou `Energie` |
| `millesime` | 2014 … 2023, `2024*` |
| `dimension` | `Régime fiscal`, `Secteur économique`, `Agents`, `Type de produit`, `Gaz à effet de serre` |
| `tarif` | tarification effective, en €/tCO2 ou €/MWh selon `unite_tarif` |
| `categorie` | modalité de la dimension |
| `quantite` | en MtCO2 ou TWh selon `unite_quantite` |
| `quantite_cumulee` | cumul, dans l'ordre croissant de tarif |
| `unite_tarif`, `unite_quantite` | unités |

Chaque ligne est une **cellule tarifaire homogène** : un palier de tarification pour
une modalité donnée.

### `elfe_instruments.csv` — 1 467 lignes

Décomposition du tarif effectif par instrument. Vérifié sur l'intégralité des deux
périmètres :

    tarification effective = taux_taxation + boucliers_et_aides + prix_quotas_ets

**759/759 lignes exactes côté carbone** (écart maximal 1,1 · 10⁻¹³) et **708/708
côté énergie** — soit du bruit de flottant, rien d'autre.

Deux pièges de lecture :

- `boucliers_et_aides` est **déjà porté en négatif** : l'identité est additive ;
- `composante_carbone` **n'entre pas** dans l'identité — montant reporté à titre
  indicatif, qui peut excéder le taux de taxation net.

Le tableau ne porte **aucun libellé de régime**. Il se raccroche à `elfe.csv` par
**jointure sur le tarif effectif** : 1 114 clés `(perimetre, millesime, tarif)` de
part et d'autre, **aucune ligne non appariée**, sur les onze millésimes.

> **Correction (2026-08-11).** L'unicité de cette jointure n'avait été vérifiée que
> sur 2022 et 2023. Sur l'ensemble des millésimes, **332 clés portent plusieurs
> décompositions distinctes** — un même tarif effectif naît de mélanges différents.
> Le cas dominant oppose **quotas ETS gratuits et quotas achetés** : même
> `prix_quotas_ets`, `prix_reel_quotas_ets` à 0 pour les uns et à sa valeur pleine
> pour les autres. C'est de l'information, pas du bruit d'agrégation.
>
> La jointure sur le couple **(tarif, quantité)** — écartée à tort — est précisément
> ce qui lève l'ambiguïté : elle rend la décomposition *exacte* sur 51,7 % de la
> masse carbone et 62,1 % de la masse énergie. Voir `elfe_atomes.csv`.

Côté énergie il n'y a pas de colonne `remboursement_indirect_ets` (sept colonnes
d'origine au lieu de neuf) ; elle est vide dans le fichier consolidé.

### `facteurs_emission_cgdd.csv` — 335 lignes, 42 régimes × 8 millésimes

Facteurs d'émission **implicites du CGDD**, en tCO2/MWh.

> ⚠️ **Série externe de comparaison, et non des paramètres.** Ces facteurs ne sont
> pas ceux du modèle et n'ont pas vocation à le devenir : les nôtres seront fixés
> indépendamment. Ceux-ci servent à *expliquer* l'écart entre les deux modèles, pas
> à l'arbitrer. C'est la raison pour laquelle ce fichier est rangé dans `assets/` et
> non dans `parameters/`.

Obtention : les quantités carbone sont en MtCO2, les quantités énergie en TWh, et
`MtCO2 / TWh = tCO2 / MWh` exactement. Le facteur se lit donc dans le **rapport des
quantités**, à régime et millésime donnés — sans passer par les tarifs, donc sans
pollution par l'ETS ni les boucliers, et y compris pour les régimes à tarif nul.

Stabilité temporelle mesurée sur 2017-2024 :

| | régimes |
|---|---|
| facteur constant (amplitude relative < 10⁻¹²) | **14** / 42 |
| coefficient de variation < 0,5 % | **27** / 42 |
| coefficient de variation ≥ 0,5 % | 15 / 42 |

Les valeurs constantes sont physiquement reconnaissables : fioul lourd 0,2808,
kérosène 0,2639, GPL 0,1908, autres produits pétroliers 0,2974 tCO2/MWh.

Les régimes qui dérivent sont **exactement les carburants incorporant des
biocarburants** — essence (cv 0,30 %), gazole routier (0,36 %), E10 (0,47 %) — dont
le taux d'incorporation monte d'année en année. Ce n'est pas du bruit mais un effet
de composition réel : sur ces régimes, un écart de facteur mêle désaccord de contenu
carbone et effet d'incorporation, et ne doit pas être lu comme le seul premier.

La colonne `cv_pct` reporte ce coefficient de variation, pour que la distinction
reste lisible sans recalcul.

## Fichiers reconstruits — `scripts/elfe/cellules.py`

L'application publie six vues **marginales** d'un même jeu de cellules ; aucun export
ne les porte conjointement. Deux clés permettent de les recombiner :

| clé | ce qu'elle identifie |
|---|---|
| `(perimetre, millesime, tarif)` | une **valeur de tarif implicite**, présente à l'identique dans les six vues |
| `(perimetre, millesime, tarif, quantite)` | un **atome** — les quantités portent ~15 chiffres significatifs, donc une même valeur dans deux vues désigne le même jeu d'enregistrements |

La quasi-injectivité de la quantité est mesurée : **20 collisions sur 9 391 lignes**.

### `elfe_cellules.csv` — 1 114 lignes

Une ligne par valeur de tarif implicite, **composantes en colonnes**. C'est la table
qui somme juste : la quantité d'une clé est identique d'une dimension à l'autre
(écart max mesuré 4 · 10⁻⁹, soit l'arrondi de la clé).

Colonnes propres : les six composantes, plus `taux_taxation_net` (= taux + boucliers,
ce que le calculateur couvre) et `hors_calculateur` (= prix des quotas, ce qu'il ne
couvrira jamais). Quand une clé porte plusieurs décompositions, elles sont moyennées
par les quantités — opération **exacte au sens de l'identité**, puisque toutes les
sous-cellules partagent le même tarif et que toute combinaison convexe le vérifie
encore. `decomposition_homogene` signale les 332 clés concernées.

Par dimension : `<dim>` porte le libellé quand la cellule n'en a qu'un, `<dim>_n` le
nombre de catégories. Un tarif ne détermine pas une catégorie — jusqu'à **36 régimes
fiscaux partagent le tarif nul**.

### `elfe_atomes.csv` — 6 347 lignes

Le grain le plus renseigné, et le seul qui recolle des libellés **entre** dimensions.

> ⚠️ **Union de marginales, pas une partition.** Deux dimensions qui découpent une
> même cellule différemment y produisent des atomes distincts et redondants. Sommer
> `quantite` sur toute la table donne ~3 fois la masse réelle. Pour sommer :
> `elfe_cellules.csv`, ou `elfe.csv` filtré sur une seule dimension.

| colonne | contenu |
|---|---|
| `n_dimensions_propres` | nombre de vues qui reconnaissent l'atome par sa quantité |
| `<dim>_herite` | le libellé vient de la cellule entière (dimension à catégorie unique) et non de l'atome |
| `n_dimensions` | libellés propres **et** hérités |
| `decomposition_exacte` | l'atome existe tel quel dans `Instruments` : composantes non moyennées |
| `partition_verifiee` | les atomes à `n_dimensions_propres ≥ 2` épuisent la masse de leur cellule — les dimensions y découpent à l'identique |

Rendement mesuré :

| | Carbone | Énergie |
|---|---|---|
| atomes | 3 706 | 2 641 |
| ≥ 2 libellés (dont propres) | 3 158 (980) | 2 204 (560) |
| ≥ 3 libellés (dont propres) | 2 735 (613) | 1 272 (280) |
| décomposition exacte | 496 atomes, 51,7 % de la masse | 281 atomes, 62,1 % |
| cellules à partition vérifiée | 378 / 624 | 342 / 490 |

**La table croisée complète n'est pas reconstituée, et ne peut pas l'être** : les
dimensions sont des marginales, leur jointe n'est pas identifiée. `Secteur
économique` est le goulot — catégorie unique sur ~35 % des cellules seulement. Les
colonnes `*_n` et `n_dimensions` disent exactement ce qui est su.

### `elfe_sous_cellules.csv` — 1 467 lignes

Les lignes `Instruments` intactes, rangées sous leur clé tarifaire avec un `rang`.
À utiliser quand la distinction quotas gratuits / quotas achetés compte, puisque
c'est elle que la moyenne pondérée de `elfe_cellules.csv` efface.

## Contrôle d'intégrité de l'extraction

Pour un couple (périmètre, millésime) donné, la quantité totale doit être identique
quelle que soit la dimension de ventilation. Vérifié : les cinq dimensions du
périmètre carbone donnent le même total, au centième, sur les onze millésimes
(475,98 MtCO2 en 2014 … 400,22 en 2023). L'extraction est donc fidèle.

Ce contrôle a vocation à devenir un garde-fou permanent de la donnée.
