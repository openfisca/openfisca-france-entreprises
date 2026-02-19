# Paramètres en dur dans les formules – Audit et propositions

Résumé des constantes numériques ou littérales repérées dans les formules (variables Python) et propositions pour les déplacer vers des fichiers de paramètres OpenFisca (YAML).

---

## 1. Seuils d’intensité énergétique (SEQE / concurrence internationale)

**Valeurs :** `0.03` (3 %), `0.005` (0,5 %)

**Fichiers concernés :**
- `variables/taxes/taxation_energies/taxation_autres_produits_energetiques.py` (cond_seqe, cond_concurrence : intensité production ≥ 0.03, intensité VA ≥ 0.005)
- `variables/taxes/taxation_energies/taxation_charbon.py` (idem)
- `variables/taxes/taxation_energies/taxation_gaz_naturel.py` (idem)
- `variables/caracteristiques_etablissement.py` (installation_grande_consommatrice_energie : facture énergie ≥ 0.03 × CA, taxe ≥ 0.005 × VA)
- `variables/consommation_energie/electricite.py` (electro-intensité : taxe ≥ 0.005 × VA)

**Proposition :**
- Créer un paramètre commun (ex. sous `energies.seuils` ou `energies.accise.seuils_seqe`) :
  - `intensite_energetique_valeur_production_min` = 0.03
  - `intensite_energetique_valeur_ajoutee_min` = 0.005
- Pour la grande consommatrice : `part_facture_energie_chiffre_affaires_min` = 0.03, `part_taxe_valeur_ajoutee_min` = 0.005
- Fichiers YAML suggérés :  
  `parameters/energies/accise/seuils_seqe/intensite_production.yaml`,  
  `parameters/energies/accise/seuils_seqe/intensite_valeur_ajoutee.yaml`  
  (ou un seul nœud `seuils_seqe` avec sous-clés).

---

## 2. Seuils électro-intensité (TICFE / accise électricité)

**Valeurs :** `13.5`, `6.75`, `3.375`, `0.5` (kWh/€ VA) ; `25` (% intensité échanges avec pays tiers)

**Fichiers concernés :**
- `variables/taxes/taxation_energies/taxation_electricite.py` (formula electro_intensive_concurrence_internationale : comparaisons à 13.5, 6.75, 3.375 ; condition_13_5 avec intensite_echanges > 25)
- `variables/consommation_energie/electricite.py` (electricite_installations_industrielles_hyper_electro_intensives : consommation_par_valeur_ajoutee >= 0.006, intensite_echanges >= 25)

**Constat :** Les *taux* par tranche existent déjà en YAML (electro_intensive_13_virgule_5, etc.) ; les *seuils* (13.5, 6.75, 3.375, 0.5, 25) sont encore en dur dans le code.

**Proposition :**
- Sous `energies.electricite.ticfe.electro_intensive.seuils` (ou `concurrence_internationale.seuils`) :
  - `electro_intensite_tranche_1_max` = 3.375  (ou tranche 0.5)
  - `electro_intensite_tranche_2_max` = 6.75
  - `electro_intensite_tranche_3_max` = 13.5
  - `intensite_echanges_pays_tiers_min` = 25  (en %)
- Pour hyper-electro : sous `energies.electricite.ticfe.electro_intensive.hyper` :
  - `consommation_par_valeur_ajoutee_min` = 0.006  (6 kWh/€ VA)
  - `intensite_echanges_pays_tiers_min` = 25
- Réutiliser ces paramètres dans les formules au lieu des littéraux.

---

## 3. Puissance souscrite (kVA) – TDCFE / TCCFE

**Valeurs :** `36`, `250` (kVA)

**Fichiers concernés :**
- `variables/taxes/taxation_energies/tdcfe/tdcfe.py` (cond_36 : amperage <= 36, cond_250 : amperage <= 250, répété par formule annuelle)
- `variables/taxes/taxation_energies/tccfe/tccfe.py` (idem)

**Constat :** Les paramètres `categorie_fiscale_menage` / `categorie_fiscale_petite_et_moyenne_entreprise` (36) et `categorie_fiscale_haut_puissance` (250) existent déjà sous `energies.electricite.ticfe`. Les formules TDCFE/TCCFE utilisent toutefois les entiers 36 et 250 en dur.

**Proposition :**
- Utiliser les paramètres existants :
  - `parameters(period).energies.electricite.ticfe.categorie_fiscale_petite_et_moyenne_entreprise` pour 36
  - `parameters(period).energies.electricite.ticfe.categorie_fiscale_haut_puissance` pour 250
- Ou créer sous `energies.electricite.tcfe` deux paramètres dédiés (ex. `seuil_36kVA`, `seuil_250kVA`) si on ne veut pas coupler TDCFE/TCCFE à la TICFE. Réduit la duplication et permet d’évoluer (ex. changement de seuil dans le temps).

---

## 4. Prélèvement exceptionnel hydrocarbures (impôt sur les sociétés)

**Valeurs :** `100e6` (100 M€), `0.12` (12 %)

**Fichier :** `variables/taxes/impots_societes.py` (formula_1985_01_01 : chiffre_affaires <= 100e6, rate = 0.12)

**Proposition :**
- Créer un nœud de paramètres dédié, par ex. `impots_societes.prelevement_exceptionnel_hydrocarbures` :
  - `seuil_chiffre_affaires` = 100_000_000  (en euros)
  - `taux` = 0.12
- Fichiers YAML :  
  `parameters/impots_societes/prelevement_exceptionnel_hydrocarbures/seuil_chiffre_affaires.yaml`,  
  `parameters/impots_societes/prelevement_exceptionnel_hydrocarbures/taux.yaml`  
  (avec `values` par période si la loi a évolué dans le temps).

---

## 5. Répartition mensuelle (bouclier / accise électricité)

**Valeurs :** `12`, `11/12`, `1/12` (mois)

**Fichiers concernés :**
- `variables/taxes/taxation_energies/taxation_electricite.py` (formulas 2022–2025 : division par 12, `* 11 / 12`, `/ 12` pour proratiser annuel/mois de janvier)

**Constat :** Il s’agit de la répartition sur 12 mois (règle fixe). On peut soit les laisser en dur (constante “12 mois”), soit les paramétrer pour cohérence (ex. `mois_par_annee` = 12) si d’autres dispositifs utilisaient une autre base.

**Proposition :**
- Priorité basse : garder 12 en dur comme constante de période, ou ajouter un paramètre unique `energies.electricite.repartition_annuelle.nombre_mois` = 12 si on souhaite tout paramétrer.

---

## 6. Dates en dur (Instant)

**Valeurs :** `Instant((2022, 2, 1))`, `Instant((2023, 2, 1))`, `Instant((2024, 2, 1))`

**Fichiers concernés :**
- `variables/boulier_tarifaire.py` (accès au taux bouclier à une date fixe par formule)
- `variables/taxes/taxation_energies/taxation_charbon.py` (instant_electrite : paramètre à une date fixe)

**Proposition :**
- Les paramètres YAML sont déjà datés (values: 2022-01-01, etc.). Le code utilise une date précise (ex. 1er février) pour choisir la valeur. On peut :
  - Soit documenter que “la date d’effet” du bouclier est le 1er février et laisser le `Instant` en dur (règle métier stable).
  - Soit introduire un paramètre “date d’effet” (stocké en chaîne ou en sous-clés année/mois/jour) et construire l’`Instant` à partir de celui-ci pour éviter des dates dispersées dans le code.

---

## 7. Taux TDCFE / TCCFE par (département, commune)

**Constat :** Les fichiers `tdcfe/taux_2011.py` … `taux_2022.py` et `tccfe/taux_2011.py` … contiennent de très gros dictionnaires Python `(departement, commune) -> taux`. Ce sont des données de paramètres, pas de la logique.

**Proposition :**
- À moyen terme : migrer ces données vers des YAML (ou CSV importés en paramètres) par année, par ex. :
  - `parameters/energies/electricite/tcfe/tdcfe/coefficients_multiplicateurs/2011.yaml` (structure par département puis commune, ou liste (dep, com) -> valeur).
- OpenFisca permet des paramètres par clé (arbre de nœuds). Il faudra adapter le chargement (paramètres imbriqués ou paramètre “table” selon le format choisi) et les formules pour lire `parameters(period).energies.electricite.tcfe.tdcfe.coefficients_multiplicateurs[...]` au lieu du dict Python.
- Gain : maintenance des taux sans toucher au code, possibilité de reprise par d’autres outils, pas de gros fichiers Python dans le dépôt.

---

## Synthèse des actions proposées

| Priorité | Thème | Action |
|----------|--------|--------|
| Haute | Seuils SEQE (0.03, 0.005) | Créer `energies.accise.seuils_seqe` (ou équivalent) et les utiliser dans taxation_* et caracteristiques_etablissement, consommation_energie/electricite. |
| Haute | Seuils électro-intensité (13.5, 6.75, 3.375, 25, 0.006) | Créer `energies.electricite.ticfe.electro_intensive.seuils` (+ hyper) et remplacer les littéraux dans taxation_electricite et consommation_energie/electricite. |
| Haute | Prélèvement hydrocarbures (100e6, 0.12) | Créer `impots_societes.prelevement_exceptionnel_hydrocarbures.*` et l’utiliser dans impots_societes.py. |
| Moyenne | Seuils kVA (36, 250) TDCFE/TCCFE | Utiliser les paramètres TICFE existants ou créer `energies.electricite.tcfe.seuil_36kVA` / `seuil_250kVA` et les utiliser dans tdcfe.py et tccfe.py. |
| Basse | Répartition 12 mois | Laisser en dur ou ajouter un paramètre unique si souhait de cohérence. |
| Basse | Dates Instant (bouclier, charbon) | Documenter ou paramétrer la “date d’effet” si on veut éviter les dates en dur. |
| Moyenne / long terme | Coefficients TDCFE/TCCFE | Migrer les dictionnaires (dep, com) -> taux vers des fichiers de paramètres (YAML/CSV) et adapter le chargement. |

En commençant par les seuils SEQE, électro-intensité et prélèvement hydrocarbures, on retire la plupart des “magic numbers” des formules et on les centralise dans des paramètres YAML datés et documentés.
