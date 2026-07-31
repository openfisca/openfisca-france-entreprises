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
**jointure sur le tarif effectif**, vérifiée à 100 % et sans ambiguïté sur les deux
périmètres (2022 et 2023). La jointure sur le couple (tarif, quantité) ne rend que
40 % et ne doit pas être utilisée : `Instruments` regroupe les cellules partageant
une même décomposition.

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

## Contrôle d'intégrité de l'extraction

Pour un couple (périmètre, millésime) donné, la quantité totale doit être identique
quelle que soit la dimension de ventilation. Vérifié : les cinq dimensions du
périmètre carbone donnent le même total, au centième, sur les onze millésimes
(475,98 MtCO2 en 2014 … 400,22 en 2023). L'extraction est donc fidèle.

Ce contrôle a vocation à devenir un garde-fou permanent de la donnée.
