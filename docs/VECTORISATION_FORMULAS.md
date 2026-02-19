# Recensement des formules OpenFisca à vectoriser

**Référence officielle :** [Vectorial computing — OpenFisca](https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html) et [Enum & EnumArray](https://openfisca.org/doc/openfisca-python-api/enum_array.html).

Les formules OpenFisca **doivent retourner un vecteur** (tableau NumPy, un élément par entité). Les structures de contrôle Python (`if`/`else`, `or`, `and`) et les retours scalaires ne fonctionnent pas avec des tableaux.

## Règles de vectorisation (d’après openfisca.org)

- **Formules = vecteurs** : `person('salary', period)` est un tableau (ex. `array([41, 42, 45])`). Le `return` doit être un tableau de même longueur.
- **Pas de `if`/`else` sur des variables d’entité** : la condition doit s’appliquer au tableau entier, pas à un scalaire.
- **Alternatives recommandées** :
  - **Condition simple (valeur si vrai, 0 sinon)** : appliquer la comparaison au vecteur, puis multiplier :  
    `condition = persons('salary', period) < 1000` → `return condition * 200`
  - **Ternaire (valeur si vrai / valeur si faux)** : **`where(condition, valeur_si_vrai, valeur_si_faux)`** (NumPy, fourni par `openfisca_core.model_api`).
  - **Plusieurs conditions (plusieurs paliers)** : **`select([cond1, cond2, cond3], [val1, val2, val3])`** — la première condition satisfaite l’emporte ; sinon 0 par défaut.
  - **Conditions complexes** : utiliser `*` à la place de `and` et `+` à la place de `or` entre tableaux booléens (dernier recours ; privilégier `where`/`select` pour la lisibilité).
- **Booléens vectoriels** :  
  - `not` → **`not_(x)`** (model_api)  
  - `and` → **`x * y`** (ou `&` sur tableaux booléens)  
  - `or` → **`x + y`** (ou `|` sur tableaux booléens)
- **Enums** : `apet == naf._53_10Z` renvoie déjà un **tableau de booléens** (doc Enum & EnumArray). Pour « apet dans une liste de codes », **ne pas utiliser `apet in codes_eligibles`** (scalaire) : combiner des égalités avec `|` :  
  `(apet == c1) | (apet == c2) | (apet == c3)` ou une boucle `result = (apet == codes[0]); for c in codes[1:]: result = result | (apet == c)`.
- **Fonctions à utiliser** : importer depuis **`openfisca_core.model_api`** : `where`, `select`, `not_`, `min_`, `max_`, `round_` (les opérateurs `&` et `|` sur tableaux booléens sont aussi valides).

## Patterns à corriger dans ce projet

1. **`if apet in codes_eligibles`** → remplacer par une combinaison d’égalités vectorielles :  
   `(apet == c1) | (apet == c2) | ...` (ou boucle comme ci‑dessus).

2. **`determinant = False` puis `if ...: determinant = True` puis `return determinant`** → remplacer par une expression vectorielle :  
   `return (apet == ...)` ou `return (apet == a) | (apet == b)`, ou `where(condition, True, False)` si besoin.

3. **`if departement in ['67', '68']`** → `(departement == '67') | (departement == '68')` ou `numpy.isin(departement, ['67', '68'])`.

4. **`if/elif/else` avec `taux = ...` puis `return taux`** (ex. TDCFE/TCCFE) → **`select([cond1, cond2], [choice1, choice2], default=0)`** avec des tableaux.

---

## 1. `electricite.py`

| Lignes | Variable / formule | Problème |
|--------|--------------------|----------|
| 37-40 | `electricite_double_usage` | `double_usage = 0` puis `if apet == ... or ...: double_usage = 1` → vectoriser avec `(apet == _20_13B) \| (apet == _20_59Z) \| (apet == _25_50A)` |
| 61-65 | `electricite_production_a_bord` | `if apet in codes_eligibles` → pattern `result = (apet == c1) \| ...` |
| 100-104 | `electricite_transport_collectif_personnes` | `if apet == type_eta._49_39A` → `return (apet == type_eta._49_39A)` |
| 119-123 | `electricite_alimentation_a_quai` | idem `apet == type_eta._52_22Z` |
| 137-141 | `electricite_manutention_portuaire` | idem `apet == type_eta._52_24A` |
| 156-160 | `electricite_exploitation_aerodrome` (2019) | `if apet == ... and consommation_par_valeur_ajoutee > ...` → `(apet == _52_23Z) & (consommation_par_valeur_ajoutee > 0.000222)` |
| 166-170 | `electricite_exploitation_aerodrome` (2022) | `if apet == type_eta._52_23Z` → `return (apet == type_eta._52_23Z)` |
| 191-195 | `electricite_fabrication_produits_mineraux_non_metalliques` | `if apet in codes_eligibles` → pattern vectoriel sur liste de codes |
| 224-228 | `electricite_centres_de_stockage_donnees` | `if apet == type_eta._63_11Z` → `return (apet == type_eta._63_11Z)` |
| 243-247 | `electro_intensive_activite_industrielle` | `status = False` puis `if apet == ... or ...` → `(apet == _08_12Z) \| ...` |
| 276-280 | `electro_intensive_concurrence_internationale` | `if apet in codes_eligibles` → pattern vectoriel |
| 322-326 | `electricite_production_electricite` | `status = False` puis `if apet == type_eta._35_11Z` → `return (apet == type_eta._35_11Z)` |
| 348-356 | `electricite_installations_industrielles_electro_intensives` | `status = False` puis `if valeur_ajoutee_eta != 0 and taxe_... >= ...` → conditions vectorielles avec `&` |
| 372-377 | `electricite_installations_industrielles_hyper_electro_intensives` | `status = False` puis `if consommation_par_valeur_ajoutee >= ... and intensite_... >= 25` → vectoriser avec `&` |

**Note :** `electricite_transport_guide` a déjà été corrigé (pattern vectoriel avec `naf`).

---

## 2. `gaz_naturel.py`

| Lignes | Variable / formule | Problème |
|--------|--------------------|----------|
| 71-74 | `gaz_matiere_premiere` | `if apet in codes_eligibles` |
| 100-103 | `gaz_huiles_minerales` | `if apet in codes_eligibles` |
| 193-197 | `gaz_double_usage` | `if apet in codes_eligibles` |
| 218-223 | `gaz_production_mineraux_non_metalliques` | `if apet in codes_eligibles` |
| 240-244 | `gaz_extraction_production` | `if apet in codes_eligibles` |
| 276-281 | `gaz_dehydration_legumes_et_plantes_aromatiques` | `status = 0` puis `if apet == type_eta._10_39A: status = 1` → `return (apet == type_eta._10_39A)` (en bool ou 0/1 selon value_type) |

---

## 3. `autres_produits.py`

| Lignes | Variable / formule | Problème |
|--------|--------------------|----------|
| 652-656 | (variable avec codes_eligibles) | `if apet in codes_eligibles` |
| 679-683 | | `if apet == type_eta._49_39A` |
| 705-709 | | `if apet == type_eta._49_32Z` |
| 732-736 | | `if apet == type_eta._49_41A or apet == type_eta._49_41B` |
| 758-762 | | `if apet == type_eta._50_30Z or apet == type_eta._50_40Z` |
| 785-789 | | `if apet == type_eta._50_10Z or apet == type_eta._50_20Z` |
| 813-817 | | `if apet == type_eta._52_24A` |
| 840-844 | | `if apet == type_eta._51_10Z or apet == type_eta._51_21Z` |
| 867-871 | | `if apet == type_eta._08_11Z or ... or ...` |
| 885-889 | | `if apet == type_eta._49_32Z` |
| 940-944 | | `if apet in codes_eligibles` |
| 966-970 | | `if apet in codes_eligibles` |
| 989-993 | | `if apet in codes_eligibles` |

---

## 4. `charbon.py`

| Lignes | Variable / formule | Problème |
|--------|--------------------|----------|
| 97-100 | (double_usage) | `double_usage = 0` puis `if apet == ... or ...` |
| 192-196 | | `if apet in codes_eligibles` |
| 212-216 | | `if apet == type_eta._50_30Z or apet == type_eta._50_40Z` |
| 231-235 | | `if apet == type_eta._50_10Z or apet == type_eta._50_20Z` |
| 250-254 | | `if apet == type_eta._51_10Z or apet == type_eta._51_21Z` |
| 276-280 | | `if apet in codes_eligibles` |
| 299-303 | | `if apet in codes_eligibles` |

---

## 5. `caracteristiques_etablissement.py`

| Lignes | Variable / formule | Problème |
|--------|--------------------|----------|
| 109-113 | (formula_2019, condition seqe/chiffre_affaires/facture_energie) | `status = False` puis `if seqe == True and ...` → conditions vectorielles avec `&` |
| 156-159 | | `if apet in codes_eligibles` |

---

## 6. `taxation_autres_produits_energetiques.py`

| Lignes | Contexte | Problème |
|--------|----------|----------|
| 786, 883, 933, 992 | `if departement in ['67', '68']` | Remplacer par `np.isin(departement, ['67', '68'])` ou `(departement == '67') \| (departement == '68')` |
| 1089, 1139, 1292, 1342 | `if departement in ['75', '77', ...]` | Idem pour liste Île‑de‑France |

(Plusieurs formules 2007 / 2017 / 2022 concernées.)

---

## 7. `tdcfe/tdcfe.py` et `tccfe/tccfe.py`

| Fichier | Lignes | Problème |
|---------|--------|----------|
| tdcfe.py | 31-36, 39-44, … (toutes les formules 2011→2021) | `if amperage <= 36 and amperage != 0: taux = ...; elif amperage <= 250 and ...: taux = ...; else: taux = 0` → utiliser `numpy.select([cond1, cond2], [choice1, choice2], default=0)` avec des tableaux |
| tccfe.py | 29-36, 39-46, … (idem) | Même pattern if/elif/else sur `amperage` |

Chaque formule annuelle (2011 à 2021/2022) doit être réécrite en vectoriel (une fois le pattern `select` en place, les années peuvent être factorisées si besoin).

---

## 8. `taxation_gaz_naturel.py`

| Lignes | Contexte | Problème |
|--------|----------|----------|
| 134-137, 169-175, 208-212, etc. | Longues chaînes `elif ... == True:` puis `taxe = ...` | Remplacer par `numpy.select(liste_conditions, liste_valeurs, default=0)` (ou équivalent avec `where`), en s’assurant que chaque condition et chaque valeur sont des tableaux. |

---

## Résumé par type

| Type | Nombre (approx.) | Fichiers |
|------|-------------------|----------|
| `apet in codes_eligibles` | 18 | electricite, gaz_naturel, autres_produits, charbon, caracteristiques_etablissement |
| `if apet == x` ou `apet == x or apet == y` (scalaire) | 25+ | electricite, gaz_naturel, autres_produits, charbon |
| `status/determinant = False` puis `if ...: True` | idem (recoupement) | idem |
| `departement in [list]` | 8 | taxation_autres_produits_energetiques |
| `if/elif/else` sur amperage (taux) | 22 formules | tdcfe.py, tccfe.py |
| Chaînes `elif ... == True: taxe = ...` | plusieurs blocs | taxation_gaz_naturel.py |

---

## Bonnes pratiques pour la vectorisation (alignées sur openfisca.org)

Source : [Vectorial computing](https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html). Utiliser les imports de **`openfisca_core.model_api`** (`where`, `select`, `not_`, `min_`, `max_`, `round_`).

| Cas | À éviter | À faire (vectoriel) |
|-----|----------|----------------------|
| **Si condition alors valeur, sinon 0** | `if salary < 1000: return 200` / `else: return 0` | `condition = persons('salary', period) < 1000` puis `return condition * 200` |
| **Ternaire (valeur A si vrai, valeur B si faux)** | `if cond: return 200` / `else: return 100` | `return where(condition_salary, 200, 100)` |
| **Plusieurs paliers (ex. taux selon amperage)** | `if ... elif ... else: return taux` | `return select([cond1, cond2, cond3], [val1, val2, val3])` (première condition vraie gagne ; défaut 0) |
| **ET logique** | `if A and B` | `A * B` ou `A & B` (tableaux booléens) |
| **OU logique** | `if A or B` | `A + B` (dernier recours) ou `A \| B` (tableaux booléens) |
| **NOT** | `if not x` | `not_(x)` |
| **Enum : un code** | `if apet == type_eta._63_11Z: return True` | `return (apet == naf._63_11Z)` (retourne déjà un tableau de bool, doc [Enum & EnumArray](https://openfisca.org/doc/openfisca-python-api/enum_array.html)) |
| **Enum : plusieurs codes (“apet in liste”)** | `if apet in codes_eligibles` | `(apet == c1) \| (apet == c2) \| ...` ou boucle `result = (apet == codes[0]); for c in codes[1:]: result = result \| (apet == c)` |
| **String dans une liste (département)** | `if departement in ['67', '68']` | `(departement == '67') \| (departement == '68')` ou `numpy.isin(departement, array(['67','68']))` |

- **Enums** : utiliser l’enum du module (ex. `naf`) pour les comparaisons ; `apet == naf._XX_XXZ` renvoie un tableau de booléens.
- **Min / max / round** : utiliser `min_`, `max_`, `round_` depuis `model_api`, pas les builtins Python.

Ce document peut servir de suivi pour corriger les formules une par une ou par fichier.
