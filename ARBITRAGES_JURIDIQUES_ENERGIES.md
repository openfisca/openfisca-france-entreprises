# Arbitrages juridiques — synchronisation énergies

> Ce document liste les points où **le droit lui-même est ambigu ou contredit par les sources**, et
> qui demandent une décision juridique avant d'être tranchés dans le modèle ou dans le barème. Il
> est distinct des simples corrections de données (traitées directement) et des choix de modélisation
> techniques. Chaque point donne l'enjeu, les options en présence avec leurs sources, l'impact, les
> fichiers concernés, et un espace **Décision** à remplir.
>
> Contexte : le modèle raisonne en **périodes annuelles**. Toute date d'entrée en vigueur infra-annuelle
> (en cours d'année) pose donc un problème structurel : soit on bascule toute l'année sur le tarif
> antérieur ou postérieur, soit on introduit une convention. C'est le fil rouge de plusieurs points ci-dessous.
>
> Voir aussi `SYNC_ENERGIES_REPORT.md` (section « Décisions en attente d'un arbitrage juridique »).

## État d'avancement

| § | Sujet | Décision | Application |
|---|---|---|---|
| 1 | Date TICC | ✅ 1er juillet 2007, réf. LFR 2006 art. 36 III | ✅ référence corrigée (date au 1er janvier par convention annuelle, cf. §2) |
| 2 | TICGN 2014 | ✅ tranché : moyenne mensuelle des tarifs, sans bascule des variables en `MONTH` | ✅ mécanisme en place (`tarif_moyen_annuel`) — reste à poser la date 2014-04-01 |
| 3 | Manutention portuaire | ✅ 1er janvier 2023 | ✅ tarif ramené à 2023-01-01 (0,5 €/MWh) |
| 4 | Intervention incendie/secours | ✅ 12 juillet 2023 | 🔓 débloqué par §2 — la date exacte peut être posée |
| 5 | Abrogations TICPE | ⏸️ à remplir, produit par produit | 🔓 débloqué par §2 — plus d'obstacle technique |
| 5 bis | Extraction de minéraux | ✅ 1er janvier 2023 | ✅ indicateur en 2023 + `formula_2023` scindée |
| 6 | Réfaction corse | ✅ paramètres oui, formules non | ✅ paramètres OF + fichiers barème proposés |
| 7 | PCS/PCI (facteur 1,11) | ⏸️ à remplir | ⏸️ |

### Le verrou infra-annuel est levé

Les points 2, 4 et 5 butaient tous sur le même obstacle : le modèle raisonne en périodes annuelles
et lisait chaque tarif au 1er janvier, de sorte qu'une entrée en vigueur en cours d'année basculait
toute l'année sur un seul tarif. Poser la date exacte revenait donc à introduire une erreur.

Cet obstacle est levé par la branche `refactor/energies-periodes-mensuelles` : plutôt que de basculer
les 153 variables de consommation et les 101 formules en périodes mensuelles — ce qu'interdisaient en
pratique les variables annuelles comme `apet`, `installation_seqe` ou le chiffre d'affaires, illisibles
depuis une formule mensuelle — l'utilitaire `tarif_moyen_annuel` intègre le tarif mois par mois à
l'intérieur des formules annuelles. La consommation étant réputée uniformément répartie, la taxe vaut
`conso * moyenne mensuelle des tarifs`, résultat identique à une bascule mensuelle complète.

**Conséquence pour ces arbitrages** : les dates exactes peuvent désormais être posées telles quelles.
La TICGN au 2014-04-01 donnera 3 mois à l'ancien tarif et 9 au nouveau, au lieu de basculer toute
l'année 2014 ; il en va de même pour l'intervention incendie au 2023-07-12 (§4) et pour les
abrogations TICPE en cours d'année (§5). Ces trois points ne sont plus bloqués que par la décision
juridique elle-même.

⚠️ Ces implémentations supposent la branche `refactor/energies-periodes-mensuelles` fusionnée
(ou d'être réalisées sur cette branche) : le mécanisme n'existe pas sur `sync/energies-no-regret`.

---

## 1. Date de début de la TICC (charbon) — trois dates concurrentes

**Enjeu.** La date de création de la taxe intérieure sur la consommation de charbon (TICC / accise
charbons) n'est pas la même selon la source.

**Options en présence.**
| Date | Portée |
|---|---|
| `2007-01-01` | valeur retenue actuellement par le **modèle** OF |
| `2007-06-01` | date portée par le **barème** IPP |
| `2007-07-01` | date de l'**article Légifrance** que les deux citent |

**Impact.** Décale le début de toute la série TICC ; à trancher sur le texte (LFR 2006 créant la taxe).
La première valeur étant concernée, une date erronée peut aussi provoquer un `ParameterNotFound` si une
formule lit la taxe avant la date retenue.

**Fichiers concernés.** OF : `charbon/ticc.yaml`. Barème : `charbon/ticc` (+ clé orpheline réf. 2015-04-01).

**Décision.** 

C'est bien le 1er juillet 2007 la bonne date. La référence législative est erronée cependant. C'est au III de l'article 36 de la LOI n° 2006-1771 du 30 décembre 2006 de finances rectificative pour 2006 (href : https://www.legifrance.gouv.fr/eli/loi/2006/12/30/2006-1771/jo/texte).

---

## 2. TICGN 2014 — 2014-01-01 (modèle) vs 2014-04-01 (barème)

**Enjeu.** La hausse du tarif normal de TICGN de 2014 est datée du **1ᵉʳ avril 2014** par le barème
(LF 2014 art. 32 IV), mais le modèle la porte au **1ᵉʳ janvier 2014**.

**Options en présence.**
- `2014-01-01` (modèle) : le tarif haussé (1.41 €/MWh) s'applique à toute l'année 2014.
- `2014-04-01` (barème, juridiquement exact) : mais le modèle étant annuel, l'adopter **basculerait
  toute l'année 2014 sur le tarif antérieur** (1.19 €/MWh au lieu de 1.41), silencieusement.

**Impact.** `taux_normal` : 1.19 vs 1.41 sur 2014. Pour `taux_reduit_grandes_consommatrices`, 2014-04-01
serait la **première valeur** → `ParameterNotFoundError` si lue avant avril. Décision de modélisation
autant que juridique : faut-il une convention (prorata, ou date de bascule annuelle conventionnelle) ?

**Fichiers concernés.** OF : `gaz_naturel/ticgn/taux_normal.yaml`, `gaz_naturel/ticgn/taux_reduit_grandes_consommatrices.yaml` (notes déjà posées dans les deux).

**Décision.** Ne peut-on pas adapter les variables de consommation de telle sorte à ce qu'elles soient mensuelles ? Dans openfisca-france (un autre paquet qui s'occupe des ménages, que tu peux inspecter à /home/pzuldp/Documents/projets/openfisca-france/), on utilise je crois set_input = set_input_divide_by_period
    definition_period = MONTH 
dans la définition de beaucoup de choses et il me semble que ça aide.

---

## 3. Manutention portuaire (électricité) — 2023-01-01 (barème) vs 2024-01-01 (modèle)

**Enjeu.** Le tarif réduit d'accise électricité pour la manutention portuaire est daté du
**2023-01-01** au barème et du **2024-01-01** dans le modèle — **et le barème est lui-même incohérent**
sur ce point (cf. SYNC_ENERGIES_REPORT §6.7).

**Impact.** Aujourd'hui numériquement neutre (valeurs identiques de part et d'autre), mais l'écart de
date fausse la première année d'application. À trancher **sur le texte** (L312-48 CIBS et son entrée en
vigueur), pas sur la source secondaire.

**Fichiers concernés.** OF : `electricite/accise/tarifs_reduits/` (manutention portuaire est portée par la
formule `taxe_accise_electricite`, `formula_2023_01_01`). Barème : `electricite/accise/tarifs_reduits/manutention_portuaire.yaml`.

**Décision.** C'est le 1er janvier 2023, d'après le c) du 3° de l'article 37 de l'ordonnance n° 2021-1843 du 22 décembre 2021 portant partie législative du code des impositions sur les biens et services et transposant diverses normes du droit de l'Union européenne (https://www.legifrance.gouv.fr/eli/ordonnance/2021/12/22/2021-1843/jo/texte)

---

## 4. Intervention des véhicules incendie et secours — 2022 (modèle) vs 2023-07-12 (barème)

**Enjeu.** Le tarif réduit d'accise (nul) pour l'intervention des véhicules des services d'incendie et
de secours est daté par le barème du **2023-07-12** (art. 50 de la loi n° 2023-580 du 10 juillet 2023).
Le modèle l'applique pourtant **dès 2022** (`formula_2022_01_01` de `taxe_interieure_consommation_sur_produits_energetiques`).

**Enjeu juridique.** Avant l'entrée en vigueur de cette réfaction (juillet 2023), ces véhicules
relevaient-ils du **tarif normal** ? Si oui, le modèle sous-taxe (à zéro) ces consommations en 2022 et au
premier semestre 2023.

**État actuel du modèle.** Le paramètre importé est **ouvert au 2022-01-01 avec valeur nulle**, ce qui
préserve le comportement existant et évite un `ParameterNotFound`. L'écart de date est documenté dans le
fichier. Numériquement neutre aujourd'hui (le tarif normal appliqué serait non nul, donc l'écart n'est
pas neutre si l'exonération anticipée est indue).

**Fichiers concernés.** OF (nouveau) : `autres_produits_energetiques/accise/tarifs_reduits/intervention_vehicules_incendie_secours.yaml`.

**Décision.** C'est bien le 12 juillet 2023 la bonne date. La référence législative pertinente est l'article 5 du Décret n° 2024-241 du 19 mars 2024 pris pour l'application des articles L. 312-78-1 et L. 312-78-2 du code des impositions sur les biens et services (https://www.legifrance.gouv.fr/eli/decret/2024/3/19/2024-241/jo/texte).

---

## 5. Abrogations TICPE hors réforme CIBS — dates infra-annuelles

**Enjeu.** Plusieurs produits ont été abolis à des **dates en cours d'année**, distinctes de la réforme
CIBS de 2022. Le modèle étant annuel, la clôture pose le même problème de bascule que la TICGN 2014.
Ces clôtures ont été **volontairement NON faites** dans les passes précédentes, en attente d'arbitrage.

**Produits et dates.**
| Produit | Date d'abrogation | Fichier(s) OF |
|---|---|---|
| `gazole_b_10` | 2019 | `.../gazole_b10*` |
| `emulsion_eau_gazole/*` | 2020-07-01 | `.../emulsion_eau_gazole/*` |
| `*/sous_conditions*` | 2020-07-01 | divers `.../sous_conditions*` |
| `gazole/carburants_sous_conditions` | 2021-07-01 | `.../gazole/carburants_sous_conditions_hectolitre.yaml` |
| `fioul_lourd_bts` / `hts` / `point_eclair` | 2003 | `.../fioul_lourd_*` |
| `essence_normale` | 2000 | `.../essence_normale*` |

**Impact.** Pour chaque produit, décider si la clôture se pose au 1ᵉʳ janvier de l'année (convention
annuelle) ou à la date exacte (avec bascule d'année). Concerne surtout les produits marginaux, mais deux
(gazole B10, émulsions) sont réels.

**Décision.** _(à remplir, produit par produit)_

---

## 5 bis. Extraction de minéraux industriels (gazole) — indicateur 2024 (modèle) vs tarif 2023 (barème)

**Enjeu.** Le tarif réduit d'accise gazole pour l'extraction de minéraux industriels commence au
**2023-01-01** au barème (le paramètre OF a été aligné sur cette date). Mais l'**indicateur d'éligibilité**
du modèle, `gazoles_extraction_mineraux_industriels`, n'a qu'une `formula_2024_01_01` : le modèle
n'applique donc le tarif réduit qu'à partir de **2024**. En 2023, un établissement d'extraction est taxé
au **tarif normal** (59,4 €/MWh) au lieu du tarif réduit (3,86).

**Impact.** Sous-application du tarif réduit sur l'année 2023 (écart 55,54 €/MWh sur la consommation
d'extraction). À trancher : l'indicateur doit-il activer en 2023 (conformément au barème et au texte),
ou 2024 reflète-t-il une entrée en vigueur réelle propre à la classification NAF retenue ?

**Fichiers concernés.** OF : indicateur `consommation_energie/autres_produits.py::gazoles_extraction_mineraux_industriels`
(formula_2024) ; paramètre `taux_selon_activite/gazoles_extraction_de_mineraux_industriels.yaml` (désormais 2023-01-01).

**Décision.** De la même manière que pour la manutention portuaire, le e) du 3° de l'article 37 de l'Ordonnance n° 2021-1843 du 22 décembre 2021 portant partie législative du code des impositions sur les biens et services et transposant diverses normes du droit de l'Union européenne spécifie que la date d'entrée en vigueur est bien le 1er janvier 2023.

---

## 6. Réfaction corse — mécanisme réel modélisé nulle part

**Enjeu.** La réfaction corse est une **minoration propre à la Corse**, distincte de la majoration
régionale, prévue à l'**article 265 A bis du code des douanes** puis à l'**article L312-41 du CIBS**.
Elle n'est portée **ni par OpenFisca ni par le barème**.

**Caractéristiques.**
- Montant : **1,0 €/hL**, puis **1,125 €/hL** à compter de 2022.
- Elle se distingue selon le carburant **non par son montant mais par sa date d'entrée en vigueur** :
  - **2002** pour les SP95 et SP98 (indice d'identification **11**) ;
  - **2019** seulement pour le SP95-E10 (indice **11 ter**), créé par l'**article 66 de la loi de
    finances pour 2019**.
- C'est la **seule différence légale connue** entre SP95/98 et SP95-E10 pour la fiscalité — et elle ne
  relève **pas** de la majoration régionale (qui, elle, ne les distingue pas).

**Référence existante.** Le dépôt `openfisca-france-indirect-taxation` la modélise dans
`parameters/imposition_indirecte/produits_energetiques/refraction_corse_ticpe.yaml` — sous le nom **mal
orthographié** « refraction » (le terme juridique exact est **réfaction**).

**Travail à faire.** Reprendre ce mécanisme (en corrigeant l'orthographe), l'ajouter au modèle, et le
**proposer au barème**. Décider comment il s'articule avec la majoration régionale corse déjà reconstruite.

**Décision.** Créer les barèmes (dans barèmes IPP) et les paramètres (dans Openfisca) mais ne pas coder les formules.

---

## 7. Discontinuité PCS/PCI sur le gaz naturel (facteur 1,11)

**Enjeu.** Avant 2022, le gaz est taxé `consommation × taux × 1,11` (conversion PCS/PCI) ; après 2022,
`consommation × taux` **sans** conversion. D'où une discontinuité (ex. 93 573 en 2021 → 84 500 en 2022 à
consommation égale). Incohérence **préexistante**, signalée par le commentaire `***faut vérrifier` du code.

**Enjeu juridique/technique.** La réforme CIBS a-t-elle réellement supprimé la conversion PCS/PCI, ou
le modèle applique-t-il un facteur de trop avant 2022 (ou en manque un après) ? À vérifier sur les textes
et les assiettes légales.

**Fichiers concernés.** OF : `gaz_naturel/…/conversion_pcs_pci`, formules de `taxation_gaz_naturel.py`.

**Décision.** _(à remplir)_

---

## Points connexes (choix de modélisation à confirmer, pas strictement juridiques)

- **Rétablissements du calcul gaz** (chemins post-2022 remis en service) : `gaz_matiere_premiere` OU
  `gaz_huiles_minerales` pour le double usage ; seuil `consommation_par_valeur_ajoutee >= seuil_conso_par_va_legumes`
  (800 Wh/€ VA, LF 2019 art. 67) pour la grande consommatrice. Cf. SYNC_ENERGIES_REPORT (passe CIBS gaz).
- **`taxe_interieure_consommation_gaz_naturel_grande_consommatrice`** : la notion disparaît sous CIBS ; la
  formule 2022 pointe désormais `taux_reduit_seqe` (1.52, identique au tarif TICGN depuis 2016 → résultat inchangé).
- **`seuil_facture_energie_par_va` (0,6744)** : non sourcé, sans équivalent barème, plus lu par aucune formule → candidat à suppression.
