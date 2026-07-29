> 📌 **Jalon du 2026-07-29 — mise à plat des exonérations intégrée au barème** : les 3 propositions
> ont été mergées (fast-forward, additif) sur la branche `energies` du dépôt barème ; la **mise à plat
> des 6 exonérations d'accise** est **intégrée et poussée** (`origin/energies` → `818ef584d`, MR IPP
> #498). Régions post-2016 et réfaction corse **restent en proposition** (`_propositions_*/`, à
> restructurer en unité avant intégration). Couverture OF↔barème : **218/228 = 95,6 %** (détail ci-dessous).

# ✅ JALON 2026-07-29 — état OF ↔ barème `energies` (BIY)

## Ce qui a été fait
- **Merge** (fast-forward, purement additif) des 3 propositions sur la branche `energies` du dépôt barème.
- **Mise à plat des exonérations d'accise intégrée + poussée** (`818ef584d`) : les 6 exonérations que
  le CIBS définit **sans distinction de grade** (navigation intérieure/maritime/aérienne, doubles usages,
  fabrication de minéraux, secteurs aéronautique/naval — art. L. 312-54 à 58 et 66 à 69) passent de
  **42 fichiers par grade à 6 fichiers à plat** sous `accise/tarifs_reduits/`, catégorie fiscale portée
  en métadonnée. Valeurs toutes nulles → agrégat identique. Les 6 `ipp_csv_id` correspondent 1:1 à ceux
  déjà posés côté OF (`13e6124`) : **la principale divergence structurelle est résolue des deux côtés**.
- **Audit de cohérence** (16 activités par grade) : 6 « blanket » mises à plat ; 9 réellement
  différenciées par carburant (taxi, transports guidé/collectif/routier, agricoles, extraction,
  manutention, montagnes, travaux statiques) → **conservées par grade**, à juste titre.
- **Intervention incendie/secours** (art. 50 loi 2023-580) : **laissée par grade** — hors tableau CIBS,
  codée seulement essences+gazoles ; sa mise à plat suppose de confirmer d'abord qu'elle vaut pour
  toutes les catégories fiscales (documenté dans `accise/tarifs_reduits/index.yaml`).

## Couverture OF ↔ barème `energies` (au `818ef584d`)
| | valeur |
|---|---|
| ids OF distincts | 222 |
| ids barème distincts | 228 |
| **appariés** | **218 — soit 95,6 % du barème** |
| OF-only | 4 |
| barème-only | 10 |

**OF-only (4)** — tous attendus : `plafond_tcfe` (pas d'équivalent barème) ;
`refaction_corse_ticpe_{sp95_sp98,sp95_e10,super_plombe}` (le barème garde la réfaction en proposition —
ces 3 s'apparieront à son intégration).

**Barème-only (10)** :
- *Résidu par conception (2)* : `accise_essences_secours`, `accise_gazoles_secours` — OF modélise
  l'intervention **à plat** (un seul paramètre), donc pas d'appariement par id (symétrique du choix ci-dessus).
- *À importer côté OF (8)* : `accise_electricite_ports`, `accise_electricite_renouvelable_autoconsommee`,
  `accise_majoration_zni`, `max_accise_essences_drom`, `max_accise_gazoles_drom`,
  `ticpe_gazole_carburant_conditions_fioul_domestique`, `ticpe_melange_propane_butane_autre`,
  `ticpe_melange_propane_butane_conditions`.

## Reste à faire
1. **Régions post-2016 + réfaction corse** (proposition → intégration) : restructurer selon la convention
   barème — fichier €/hL **clos à `null` en 2022** + fichier €/MWh séparé, **ne pas mêler les unités dans
   un même fichier** ; trancher les renommages (centre→centre_val_loire, pays_loire→pays_la_loire, étendre
   les régions au périmètre inchangé plutôt que dupliquer) et la clôture des régions pré-2016.
2. **Importer les 8 paramètres barème-only** côté OF → couverture ~99 %.
3. L'intégration de la réfaction côté barème appariera les 3 ids OF-only.

---

> 📌 **Reprise du lundi 2026-07-27** : voir `ACTIONS_EN_ATTENTE.md` pour tout ce qui demande une
> action humaine (PR à ouvrir, issue OFF-E, propositions barème **non commitées** dans le worktree,
> arbitrages §5 et §7). Côté agent, l'item 2 (TIRUERT) a été terminé le 2026-07-24 : `sync/energies-no-regret`
> est à `fca4534`, 205 tests passent. La branche `refactor/energies-periodes-mensuelles` (`3a9dcb6`)
> attend sa PR ; les arbitrages §2, §4 et §5 en dépendent.

# ⏸️ REPRISE AU 2026-07-23 — à lire en premier

Tout est **commité et poussé** sur `sync/energies-no-regret` (jusqu'à `289900e`). Arbre de travail
propre. Reprendre ici ; le bloc du 2026-07-22 ci-dessous reste valable pour le contexte.

## Fait et poussé depuis le 2026-07-22
- **Électricité — tarifs réduits à zéro** paramétrés (`b6f5d4e`).
- **Autres produits — exonérations sectorielles** paramétrées + tarif incendie/secours + date
  extraction alignée + **majorations régionales pré-2016 en valeurs absolues** (`8eb5cfb`).
- **Doc arbitrages** `ARBITRAGES_JURIDIQUES_ENERGIES.md` créée (`476d8bb`), plusieurs décisions remplies.
- **Majorations régionales post-2016 en absolu** (`dc30f29`) puis **fusion depuis_2017/depuis_2022**
  en un palier unique, `formula_2022` supprimées (`378afc5`). Tout est neutre en taxe (base_nationale
  soustraite par les formules), sauf les divergences pré-2016 signalées ci-dessous.
- **Arbitrages appliqués** (`289900e`) : référence TICC corrigée (LFR 2006 art. 36 III) ; manutention
  portuaire électricité ramenée à 2023-01-01 (0,5 €/MWh, au lieu de 2024).

Correspondance avec le plan utilisateur : **item 1 ✅, item 3 ✅ (palier pré-2016 + post-2016), item 5
✅ (conversion + fusion + fichiers barème générés), item 4 partiel** (#1, #3 faits).

## Artéfacts hors dépôt OF
- **Fichiers barème à remonter** (régions post-2016, valeurs absolues, `ipp_csv_id` INSEE proposés) :
  `../baremes-ipp-yaml-energies/_propositions_regions_post_2016/` (+ README). **Non commités** (worktree
  détaché) — les déplacer vers une branche du dépôt barème pour en faire une PR avant que le worktree
  ne soit supprimé.
- **Worktree barème** : recréer avec `git worktree add --detach ../baremes-ipp-yaml-energies origin/energies`
  (⚠️ `origin/energies`, PAS `energies` local qui est périmé — cf. mémoire du projet).

## Issue OFF-E à ouvrir
Changements de taxe dus à l'adoption des valeurs absolues du barème (majoration régionale, cellules
divergentes à faire vérifier sur Légifrance) : super {rhone_alpes 2010, limousin 2010, poitou_charentes
2010/2014/2015} ; gazole {rhone_alpes 2010, limousin 2010, corse 2010/2014-16, poitou_charentes
2010/2014/2015}. Détail dans le message du commit `8eb5cfb`. Bug latent connexe : format de code
département incohérent (`2A` vs `02A`) entre formules → la Corse peut tomber sur `default=0`.

## PROCHAINE ACTION — reprendre ici (fin item 4, puis item 2)
1. ~~**#6 Réfaction corse**~~ ✅ **fait** (`0dfb241`) : paramètres OF sous
   `autres_produits_energetiques/refaction_corse/` (SP95/98 depuis 2002, SP95-E10 depuis 2019, plombé
   clôturé en 2022), sans formule ; fichiers barème proposés dans
   `../baremes-ipp-yaml-energies/_propositions_refaction_corse/`.
2. ~~**#5 bis Extraction**~~ ✅ **fait** (`0dfb241`) : indicateur passé à `formula_2023` et
   `formula_2023` scindée dans `taxe_interieure_consommation_sur_produits_energetiques`. Vérifié :
   59 400 € en 2022 (tarif normal), 3 860 € à partir de 2023.
3. **#4 Intervention** (2023-07-12) et **#2 TICGN 2014**, **#5 abrogations TICPE** : purement
   infra-annuels. Décision d'architecture en attente — **passage des variables de conso en `MONTH` +
   `set_input_divide_by_period`** : correct mais c'est un chantier à part (sa propre branche/PR), voir
   la question posée dans la doc arbitrages #2. Recommandation : rester en **convention annuelle** pour
   la synchro ; traiter le mensuel comme projet dédié ultérieur.
4. Ensuite **item 2 (TIRUERT)** : modélisation (données déjà importées) ; **item 6 (restructuration par
   grade / référence directe)** réservé à une autre branche+PR.

---

# ⏸️ REPRISE AU 2026-07-22

Ce bloc remplace l'état décrit plus bas, qui date du 17 juillet et n'est conservé que pour
l'historique des décisions. **Tout ce qui suit est à jour et suffit pour reprendre sur une
autre machine** : aucune information nécessaire ne réside ailleurs que dans les dépôts.

## Dépôts et branches

| dépôt | branche | état |
|---|---|---|
| `openfisca-france-entreprises` | `sync/energies-no-regret` | travail de synchronisation, **poussée** |
| `openfisca-france-entreprises` | `assets/agregats-tic` | agrégats fiscaux TIC pour un collègue, **poussée** |
| `baremes-ipp-yaml` | `energies` | corrections amont, **poussée** |

Le barème est la source de vérité (chaque valeur adossée à une référence Légifrance).
Racine énergies du barème : `parameters/taxation_indirecte/energies`.

⚠️ **Un worktree git local avait été créé** (`../baremes-ipp-yaml-energies`, détaché sur
`energies`) pour lire le barème pendant que la copie principale servait à d'autres travaux.
**Il n'existe pas sur une autre machine.** Pour le recréer si besoin :
`git worktree add --detach ../baremes-ipp-yaml-energies energies`. Sinon, lire simplement
le barème depuis sa copie principale, branche `energies`.

Troisième dépôt utile : `openfisca-france-indirect-taxation`, branche `energies_migration`.
Il modélise la **réfaction corse** (fichier mal nommé `refraction_corse_ticpe.yaml` : le terme
juridique exact est *réfaction*) et documente dans `ENERGIES_MIGRATION_NOTES.md` une
réconciliation barème/OFFIT qui recoupe ces travaux.

## Objectif final

À terme, OpenFisca doit **appeler directement le barème** plutôt que recopier ses paramètres.
L'arbre actuel ne peut pas être branché tel quel dessus : voir « Ce qui bloque la référence
directe » plus bas.

## Décisions permanentes

1. Architecture **hybride** : noms plats côté OpenFisca, mais découpage avant/après réforme
   CIBS du barème (clôture `null` au 2022-01-01, lecture de `accise/` ensuite).
2. **Élaguer OpenFisca et le repeupler depuis le barème** plutôt que maintenir des paramètres
   propres non vérifiables.
3. Corriger les défauts du barème **dans les deux dépôts**, pas seulement en aval.
4. **Préférer la duplication des formules à la factorisation** : une formule doit se lire comme
   un instantané du droit à sa date.
5. Tarifs réduits à zéro : **les paramétrer** depuis le barème plutôt que coder `return 0`.

## Travaux terminés

Côté barème (branche `energies`) : suppression du découpage territorial `metropole`/`drom` en
premier nœud ; correction de l'unité `currency_per_hectoliter` sur onze tarifs gaz et charbon
exprimés en euros par MWh ; identifiants des six paramètres TIRUERT qui partageaient tous
`ticgn_taux` ; libellés du tarif réduit charbons SEQE recopiés de son voisin indirect.

Côté OpenFisca (branche `sync/energies-no-regret`, dans l'ordre) : corrections « sans regret » ;
élagage des doublons et du code mort ; réforme CIBS pour le gaz et le charbon, puis pour la TICPE
et les électro-intensifs, puis scission `accise/` de l'électricité ; clôture de la TGAP en 2019 et
import des paramètres TIRUERT en données seules ; fusion des deux arbres de majoration régionale
super et reconstruction de la Corse ; indexation des tarifs TCFE et incorporation des taxes locales
à l'accise ; abrogation du tarif concurrence internationale en 2024 ; attribution de 33 `ipp_csv_id`
repris du barème ; paramétrage des tarifs réduits charbon puis gaz naturel.

Défauts vivants corrigés en cours de route, dont aucun n'était détecté par les tests : un appel mort
`etablissement("", period)` qui cassait tout le calcul charbon ; un appel à une classe commentée qui
cassait le chemin gaz après 2022 ; le tarif concurrence internationale, abrogé en 2024, encore
appliqué au gaz, soit un dixième du montant dû ; les tarifs TCFE figés depuis 2011, sous-estimant
TCCFE et TDCFE de 2019 à 2022 ; le tarif agricole gaz carburant appliqué à l'assiette combustible.

## PROCHAINE ACTION — reprendre ici

Passe **C1b**, paramétrage des tarifs réduits à zéro. Charbon et gaz sont faits. Restent :

**Électricité (4 tarifs, analyse déjà faite).** Le barème porte quatre tarifs à zéro sous
`electricite/accise/tarifs_reduits` : `doubles_usages`, `fabrication_mineraux`,
`production_biens_intensive`, `production_navires`. Les quatre variables d'activité existent côté
OpenFisca sous d'autres noms : `electricite_double_usage`,
`electricite_fabrication_produits_mineraux_non_metalliques`,
`electricite_production_biens_electro_intensive`, `electricite_production_a_bord`.
Il restait à localiser la formule CIBS de `taxe_accise_electricite` (classe ligne 370 de
`taxation_electricite.py`) et à y remplacer la branche `condition_exoneration` renvoyant zéro par
une branche par activité lisant son tarif, sur le modèle de ce qui a été fait pour le charbon.

**Autres produits énergétiques (44 tarifs).** Le plus gros morceau, non entamé.
`taxation_autres_produits_energetiques.py` fait 3 054 lignes et vingt formules ; quatre branches y
renvoient zéro. À évaluer avant de se lancer.

Méthode éprouvée sur charbon et gaz : importer les fichiers du barème dans
`<produit>/accise/tarifs_reduits/`, écrire les `index.yaml`, remplacer la condition unique par une
branche par activité, puis **vérifier par calcul effectif** que chaque exonération donne toujours
zéro de part et d'autre des dates charnières — les tests seuls ne suffisent pas, ils n'ont détecté
aucun des cinq défauts vivants ci-dessus.

## Ce qui bloque la référence directe

- OpenFisca stocke les majorations régionales en **écart** (barème moins 1,77 pour le super, moins
  1,15 pour le gazole) là où le barème stocke des valeurs absolues.
- Les dates TICPE sont normalisées côté OpenFisca (`AAAA-01-11` → `AAAA-01-01`), et des marqueurs
  `1993-01-01: null` y sont ajoutés.
- **98 paramètres OpenFisca n'ont pas d'`ipp_csv_id`**, seule clé de jointure stable. Dont les
  52 régions postérieures à 2016 et les seuils propres à la modélisation, qui n'ont pas
  d'équivalent au barème et demandent soit des identifiants inventés, soit un ajout au barème.
- Reste à décider **comment** OpenFisca consommerait le barème : sous-module git, dépendance
  versionnée, ou paquet `.openfisca/openfisca_baremes_ipp` déjà présent dans le dépôt barème.

## Décisions en attente d'un arbitrage juridique

- `manutention_portuaire` électricité : barème au 2023-01-01, OpenFisca au 2024-01-01, le barème
  étant lui-même incohérent sur ce point.
- TICGN 2014 : le barème date du 2014-04-01, mais le modèle raisonne en périodes annuelles ;
  adopter cette date basculerait toute l'année 2014 sur le tarif antérieur.
- TICC : trois dates concurrentes, 2007-01-01 côté modèle, 2007-06-01 côté barème, 2007-07-01 dans
  l'article Légifrance que les deux citent.
- Abrogations TICPE hors CIBS (2019, 2020, 2021) : même question infra-annuelle.
- **Réfaction corse** : mécanisme réel modélisé nulle part, ni dans OpenFisca ni dans le barème.

## Défauts du barème connus et non corrigés

Six tarifs réduits GPL combustible reprennent les identifiants de leurs équivalents carburants ;
`tccfe_coef_max` est partagé par trois fichiers, dont les deux DROM.

---

> ## ⏸️ Historique — état au 2026-07-17
> **Phase terminée :** comparaison + reporting des 5 domaines (§0–§5 ci-dessous). Aucun fichier modifié à ce jour.
> **Décisions prises (via l'utilisateur) :**
> 1. Architecture cible = **Hybride** : garder les noms plats OF, mais adopter le découpage propre pré-2022/post-2022 des barèmes (ajouter les `null` de clôture au 2022-01-01, lire `accise/` après 2022). → passe *structurelle* ultérieure.
> 2. Cette passe = **corrections « sans regret » uniquement**, puis revue par l'utilisateur avant d'aller plus loin.
> 3. Tarifs réduits à 0 (navigation, aéronautique, doubles usages, fabrication minéraux) = **paramétrer** depuis les barèmes (au lieu du `return 0` en dur). → passe structurelle/formules.
> 4. Bug d'unité `currency_per_hectoliter` (€/MWh gaz+charbon) = **corriger dans OF ET dans la copie locale des barèmes**.
>
> **PROCHAINE ACTION (reprendre ici) :** exécuter la passe « sans regret » = uniquement :
> corrections de valeurs (§2a), dates non-CIBS (§2b : ticgn 2014, ethanol_diesel_ed95, gazoles_extraction),
> ajout des indexations **positives** manquantes (§2c hors terminaisons null), `ipp_csv_id` (§2e),
> unités (§3/§4, y c. hectolitre→mwh dans les deux dépôts + `ticc` currency→currency_per_mwh), descriptions copiées (§2g).
> **À NE PAS faire dans cette passe (→ passe suivante, après revue) :** tout `null` de clôture
> (CIBS 2022, TGAP abolie 2019, tarif indirect-SEQE abrogé 2024, bouclier `majoration_tccfe_maximum`),
> les suppressions de doublons/fantômes liées aux formules (`taux_reduit_legumes`, `transport_collectif_personnes`,
> arbre `super_e10`, `instant_electrite`, `ifp`), les sous-systèmes manquants (TIRUERT, régions post-2016),
> et toute édition de `variables/**/*.py`.
>
> ### ✅ Fait depuis : réorganisation territoriale côté barèmes (commit `422057df7`, branche `energies`)
> Le découpage `metropole/` + `drom/` en premier nœud sous `autres_produits_energetiques` a été supprimé.
> Motifs : axe non parallèle (metropole = tarifs applicables, drom = simples **plafonds** encadrant des tarifs
> fixés par la région, art. L312-38 CIBS) ; déséquilibre (2 params sous `drom/` vs 173 sous `metropole/`) ;
> nœud DROM juridiquement plafonné (L312-10, hors TIRUERT) ; incohérent avec la convention maison
> (métropole implicite, outre-mer en qualificatif de feuille).
> **Nouvelle arborescence :** les enfants de `metropole/` remontent d'un niveau ; les 2 plafonds DROM sont
> sous `accise/carburants/plafonds_drom/`. 265 paramètres avant et après, aucune valeur ni `ipp_csv_id` modifié.
> `tables/taxation-indirecte.yaml` mis à jour. Arbre vérifié : parse OK + chargement OpenFisca OK.
> ⚠️ **Les chemins barèmes n'ont plus de préfixe `metropole/`** — en tenir compte dans tout le reste de ce rapport.
>
> **1re étape concrète au redémarrage :** valeurs barèmes **déjà relevées** (7/11) :
> - `tdcfe/coefficient_multiplicateur_maximum` : 2011=4, 2016=4.25, 2021=4.25, 2022=null (`ipp_csv_id: tdcfe_coef_max`, `unit: /1`)
> - `tdcfe/coefficient_multiplicateur_minimum` : 2011=2, 2016=2, 2021=4.25, 2022=null (`ipp_csv_id: tdcfe_coef_min`)
> - `accise/carburants/huiles_moyennes/carbureacteurs` : 2022=**42.131**, 2023=59.481, 2024=76.826
> - `accise/carburants/huiles_lourdes/tarifs_reduits/taxi` : 2022=30.02, 2023=**30.2**
> - `accise/carburants/tarifs_particuliers/ethanol_diesel_ed95` : 2022-01-01=12.157, **2022-08-18**=12.119
> - `accise/carburants/huiles_lourdes/tarifs_reduits/extraction_mineraux` : **2023-01-01**=3.86 (seule valeur)
> - `accise/carburants/huiles_lourdes/tarifs_reduits/agricoles_forestiers` : 2022=3.86, 2024=6.71, 2025-01-01=9.56, **2025-02-16=3.86**
>
> ### ✅ Passe « sans regret » exécutée (OF, non commitée — en attente de revue)
> 30 fichiers de paramètres + 2 fichiers de tests modifiés. **164/164 tests passent**, aucun nouveau warning yamllint
> (les erreurs CRLF `new-lines` sont pré-existantes sur tout le checkout Windows, y compris fichiers non touchés).
> Côté barèmes : 3 commits sur `energies` (réorganisation territoriale, unités hectolitre→mwh, collision d'id bouclier).
>
> ### ✅ Passe CIBS gaz + charbon (commit à venir) — et 3 bugs latents découverts
> Les paramètres pré-réforme gaz et charbon sont désormais clôturés au 2022-01-01 et les formules
> lisent l'accise après cette date. Vérifié par calcul effectif sur 2019→2025 (et non seulement par
> les tests) : gaz 84500 (2022) / 163700 (2024) / **171600 (2025, valeur 17.16 auparavant absente
> de tout OF)** ; charbon 73100 constant de part et d'autre de la réforme.
>
> **3 bugs latents pré-existants découverts et corrigés** (le chemin gaz post-2022 et TOUT le chemin
> charbon étaient non fonctionnels, sans qu'aucun test ne le détecte) :
> 1. `consommation_energie/autres_produits.py` : ligne morte `etablissement("", period)` → cassait
>    l'intégralité du calcul charbon, à toutes les années.
> 2. `taxation_gaz_naturel.py` : appel à `consommation_gaz_usage_non_combustible`, classe commentée
>    dans `consommation_energie/gaz_naturel.py` → cassait tout le chemin gaz post-2022. Rétabli
>    conformément à l'intention documentée (`gaz_matiere_premiere` OU `gaz_huiles_minerales`).
> 3. `taxation_gaz_naturel.py` : appel à `intensite_energetique` (variable inexistante), comparée au
>    seuil non sourcé `seuil_facture_energie_par_va` (0.6744). Aligné sur le test légal des formules
>    2019/2020 : `consommation_par_valeur_ajoutee >= seuil_conso_par_va_legumes` (800 Wh/€ VA, LF 2019 art. 67).
>
> **⚠️ À faire confirmer** (choix de modélisation pris pour rétablir le calcul, à valider) :
> - le rétablissement (2) et (3) ci-dessus ;
> - `taxe_interieure_consommation_gaz_naturel_grande_consommatrice` : la notion TICGN de « grande
>   consommatrice » disparaît sous CIBS ; la formule 2022 pointe désormais sur `taux_reduit_seqe`
>   (1.52), valeur identique à celle du tarif TICGN depuis 2016, donc résultat inchangé ;
> - **discontinuité PCS/PCI** : avant 2022 le gaz est taxé `conso × taux × 1.11`, après 2022
>   `conso × taux` sans conversion (d'où 93573 en 2021 → 84500 en 2022). Incohérence pré-existante,
>   signalée par le `***faut vérrifier` du code. Non modifiée ici.
> - `seuil_facture_energie_par_va` (0.6744) n'est désormais plus lu par aucune formule : candidat à suppression.
>
> ### ✅ Passe CIBS TICPE + électro-intensifs
> **TICPE** : les 28 paramètres dont le barème constate la disparition au 1er janvier 2022 sont
> clôturés. Vérifié au préalable par graphe d'appel : aucun n'est lu par une formule postérieure à
> 2022 (les formules basculaient déjà correctement sur l'accise), seuls les paramètres restaient
> ouverts indéfiniment.
> **Électro-intensifs électricité** : les deux régimes se recouvraient. Les 7 fichiers de l'ère CIBS
> (`activite_industrielle/`, `concurrence_internationale/`) étaient datés du 2016-01-01 alors que leur
> propre référence est l'ordonnance CIBS de 2022 ; ils sont redatés au 2022-01-01. Les 7 paramètres
> antérieurs (`electro_intensive/taux_*`, `hyperelectro_intensive`, `risque_de_fuite_de_carbone/taux_*`)
> sont clôturés au 2022-01-01. Vérifié : à 2021 les variables pré-réforme calculent toujours
> (75000, 5000, 55000) ; à 2023 elles échouent désormais explicitement au lieu d'appliquer un tarif
> abrogé, ce qui est le comportement recherché.
>
> **Clôtures TICPE volontairement NON faites** (motif juridique distinct de la réforme CIBS, et même
> subtilité infra-annuelle que la TICGN 2014) : produits abolis à d'autres dates — `gazole_b_10` (2019),
> `emulsion_eau_gazole/*`, `*/sous_conditions*` (2020-07-01), `gazole/carburants_sous_conditions` (2021-07-01),
> `fioul_lourd_bts`/`hts`/`point_eclair` (2003), `essence_normale` (2000).
>
> ### ✅ Scission accise/ côté électricité — FAITE
> `electricite/accise/{tarifs_normaux,tarifs_reduits}/` est créé. Les paramètres purement CIBS sont
> **déplacés** (`git mv`, historique conservé) : les deux tarifs normaux ménages et PME, l'alimentation
> à quai, le transport collectif routier, les deux tarifs aéronefs 2025 et les deux dossiers
> électro-intensifs. Les paramètres **fusionnés** sont scindés : `ticfe/{taux_normal, aerodromes,
> data_center, transport_guide}` sont clôturés au 2022-01-01 et leurs tarifs d'accise créés en face.
> Les seuils et catégories restent sous `ticfe/` : ce ne sont pas des tarifs mais des critères de
> modélisation sans équivalent au barème, valables de part et d'autre de la réforme.
>
> Deux variables n'avaient **aucune** formule postérieure à 2022 (`taxe_electricite_exploitation_aerodrome`,
> formule 2019 seule ; `taxe_electricite_transport_guide`, formule 2016 seule) : la clôture les aurait
> cassées en 2023. Une `formula_2022_01_01` leur est ajoutée. De même `electro_intensite`, qui n'avait
> qu'une formule non datée et lisait donc `ticfe.taux_normal` jusqu'en 2025.
> `intensite_energetique_valeur_ajoutee` et `electro_intensite` lisent désormais
> `accise.tarifs_normaux.haute_puissance`, conformément au L312-44 qui retient le tarif normal haute
> puissance — c'était le principal risque de dérive visé par cette passe.
>
> Vérifié par calcul de part et d'autre de la bascule : tarif normal 225000, aérodromes 75000,
> transport guidé 5000, data center 120000, électro-intensité 0.225 — continus en 2021, 2022, 2023 et
> 2025. La scission est neutre en résultat, ce qui était l'objectif.
>
> **Effet voulu des clôtures** : appelées après 2022, les variables d'avant réforme
> (`taxe_interieure_consommation_gaz_naturel`, `taxe_electricite_installations_industrielles_*`,
> `taxe_electricite_risque_de_fuite_de_carbone`) lèvent désormais `ParameterNotFound` au lieu
> d'appliquer un tarif abrogé. Aucune n'est atteinte depuis les variables de tête, dont le calcul
> reste continu.
> **Échecs préexistants, sans rapport avec ces passes** (aucun des fichiers concernés n'est touché par
> la branche) : `taxe_electricite` et les taxes communale et départementale échouent faute de code
> commune ou département, les coefficients étant indexés sur 35 325 communes et 103 départements ;
> `taxe_contribution_service_public_electricite` lit la CSPE, déjà close en 2016 avant ces travaux.
>
> ### ⛔ Reste à faire côté électricité — le cas manutention portuaire
> OpenFisca fusionne dans un seul fichier `ticfe/` les séries d'avant et d'après réforme, là où le
> barème les sépare (`ticfe/` clôturé, `accise/` rouvert). Sont concernés les paramètres encore lus
> après 2022 : `taux_normal` (22.5), `aerodromes` (7.5), `data_center` (12), `transport_guide` (0.5),
> `transport_collectif_personnes` (0.5), `alimentation_a_quai` (0.5), `manutention_portuaire`.
> **Impact numérique nul aujourd'hui** — les valeurs sont identiques de part et d'autre de la réforme.
> L'enjeu est la dérive future : si un tarif d'accise est indexé par arrêté, OpenFisca continuerait de
> lire la valeur TICFE périmée (c'est exactement le mécanisme qui avait fait manquer 17.16 sur le gaz).
> À traiter avec `intensite_energetique_valeur_ajoutee`, qui doit lire le tarif normal haute puissance
> de l'accise (L312-44) et lit encore `ticfe.taux_normal`.
> Cas à arbitrer juridiquement : `manutention_portuaire`, daté 2024-01-01 dans OpenFisca et 2023-01-01
> dans le barème — mais le barème est lui-même incohérent sur ce point (cf. §6.7), à trancher sur le texte.
>
> ### ✅ Passe TGAP + TIRUERT — et une correction du diagnostic initial
> **⚠️ Rectification.** Ce rapport affirmait plus bas (§2d) que la TGAP non terminée était un
> « bug à fort impact » et qu'OpenFisca « continue de prélever une taxe morte ». **C'est faux.**
> Vérification faite, **aucune formule ne lit les paramètres `tgap_carburants`** : `grep` ne trouve
> `tgap` dans aucun fichier `.py` ni aucun test, la seule occurrence hors du dossier de paramètres
> étant l'entrée d'ordre dans `index.yaml`. Ce sont des données orphelines. Il n'y avait donc pas
> de sur-taxation. L'affirmation venait du rapport de comparaison initial, qui avait supposé un
> usage sans le vérifier. §2d est à lire avec cette rectification.
>
> La donnée restait néanmoins fausse : les 7 fichiers `tgap_carburants/*` portaient 0.079 au
> 2019-01-01 (valeur recopiée du taux cible TIRUERT essences) là où le barème constate l'abrogation.
> Ils sont désormais clôturés à cette date.
>
> **TIRUERT importée en données seules** (6 paramètres + index). La modélisation n'est pas faite,
> pour deux raisons de fond consignées dans l'index importé : le redevable de la TIRUERT est celui
> qui met le carburant à la consommation, soit un fournisseur ou un distributeur, alors que le
> modèle représente les établissements comme des consommateurs ; et le calcul exige la proportion
> d'énergie renouvelable des carburants du redevable, dont le modèle n'a aucune variable d'entrée.
> Décisions à prendre avant toute implémentation.
>
> Côté barème, les 6 fichiers TIRUERT partageaient l'identifiant `ticgn_taux`, celui de la TICGN :
> un même identifiant pour sept paramètres de deux taxes sans rapport. Corrigé en
> `tiruert_{tarif,taux}_{essences,gazoles,carbureacteurs}`. `tarifs_carbureacteurs` déclarait en
> outre `unit: /1` sur des forfaits en euros : corrigé en `currency_per_mwh`.
>
> ### ✅ Fusion des deux arbres `major_regionale_ticpe_super_*` et reconstruction de la Corse
> OpenFisca portait deux arbres parallèles, `_95_98` et `_e10`, dont 47 fichiers sur 49 étaient
> identiques au octet près et dont les 22 `ipp_csv_id` étaient dupliqués deux à deux. Ils sont fusionnés
> en un seul `major_regionale_ticpe_super/`, conforme au barème. **Plus aucun `ipp_csv_id` dupliqué dans
> l'arbre énergies d'OpenFisca**, contre 22 auparavant.
>
> **La majoration régionale ne distingue pas le SP95/98 du SP95-E10.** Trois éléments concordants :
> le dépôt openfisca-france-indirect-taxation la modélise par un paramètre unique explicitement intitulé
> « SP95, SP98 et SP95 E10 », documenté comme couvrant les indices d'identification 11 et 11 ter ensemble ;
> le barème n'a qu'un seul arbre ; et les valeurs impliquées par l'arbre `_e10` comprenaient une majoration
> absolue négative, juridiquement impossible.
>
> **Convention d'écart établie puis vérifiée** : `OpenFisca = barème − 1.77`, exactement, sur l'Alsace
> (1.4→−0.37, 1.77→0, 2.5→0.73), la Bretagne (1.1→−0.67) et PACA (0.98→−0.79) ; l'écart passe à 2.77 en
> 2013 puis revient à 1.77 en 2014, ce qui reflète une variation nationale d'accise. Les valeurs de
> `depuis_2022` valent celles de `depuis_2017` multipliées par 1.125, conversion d'unité vérifiée sur
> l'ensemble des régions (0.73→0.821, 1.75→1.969).
>
> **Corse reconstruite** à partir du barème et de cette convention : −1.77 en 2007, −0.76 en 2009,
> −1.77 en 2010, −2.77 en 2013, −1.77 en 2014, soit exactement les valeurs absolues du barème
> (0, 1.01, 0, 0, 0). Les valeurs antérieures étaient inférieures d'exactement 1.00 en 2007 et 2009,
> montant de la réfaction corse d'avant 2022, et plaçaient la Corse au plafond national à partir de 2011
> alors que le barème l'y maintient à zéro jusqu'en 2017.
>
> **Corrigé au passage** : `depuis_2022/corse.yaml` et `depuis_2022/nouvelle_aquitaine.yaml` portaient la
> clé 2017-01-01 dans un dossier « depuis 2022 » ; Nouvelle-Aquitaine portait en outre 0.73 au lieu de
> 0.821, valeur non convertie.
>
> **Mise en garde sur une conclusion trop rapide** : `depuis_2022/corse = −1.125` avait d'abord été pris
> pour la réfaction post-2022, dont le montant est aussi 1.125. C'est en réalité −1.00 × 1.125, la
> conversion appliquée à toutes les régions. Coïncidence numérique ; la valeur était correcte.
>
> ### ⛔ La réfaction corse n'est modélisée nulle part — à traiter
> C'est une minoration propre à la Corse, distincte de la majoration régionale, prévue à l'article
> 265 A bis du code des douanes puis à l'article L312-41 du CIBS. Montant de 1.0, puis 1.125 à compter
> de 2022. Elle se distingue selon le carburant **non par son montant mais par sa date d'entrée en
> vigueur** : 2002 pour les SP95 et SP98 (indice 11), 2019 seulement pour le SP95-E10 (indice 11 ter),
> créé par l'article 66 de la loi de finances pour 2019. C'est la seule différence légale connue entre
> ces deux carburants — et elle ne relève pas de la majoration régionale.
> Ni OpenFisca ni le barème ne la portent. Le dépôt openfisca-france-indirect-taxation la modélise, dans
> `parameters/imposition_indirecte/produits_energetiques/refraction_corse_ticpe.yaml`, sous le nom mal
> orthographié « refraction » — le terme juridique exact est **réfaction**. À reprendre, en corrigeant
> l'orthographe, et à proposer au barème.
>
> ### ⛔ Reporté à la passe suivante — dont 3 découvertes de cette passe
> 1. **`gazoles_extraction_de_mineraux_industriels` : date 2022→2023 impossible en paramètre seul.**
>    `taxation_autres_produits_energetiques.py::formula_2022_01_01` lit ce tarif dès 2022 → `ParameterNotFoundError`.
>    Correction couplée : déplacer la valeur au 2023-01-01 **et** scinder une `formula_2023_01_01`. Noté dans le fichier.
> 2. **TICGN 2014-01-01 vs 2014-04-01 : décision de modélisation, pas une correction.** Le barème dit 2014-04-01
>    (LF 2014 art. 32 IV). Mais OF raisonne en périodes ANNUELLES : adopter 2014-04-01 bascule toute l'année 2014
>    sur le tarif antérieur (1.19 au lieu de 1.41) — silencieusement, car aucun test ne le couvre pour `taux_normal`.
>    Pour `taux_reduit_grandes_consommatrices` c'est la 1re valeur → `ParameterNotFoundError`. Arbitrage requis. Noté dans les 2 fichiers.
> 3. **TDCFE : terminaison 2023-01-01 (OF) vs 2022-01-01 (barème)** — laissée à 2023, relève de la politique de clôture CIBS.
> 4. Tous les `null` de clôture : CIBS 2022 (~60 fichiers), TGAP abolie 2019, tarif indirect-SEQE abrogé 2024,
>    bouclier `majoration_tccfe_maximum` 2023-02-01.
> 5. Élagage des doublons OF (cf. [[prune-of-populate-from-baremes]]) : `taux_reduit_legumes`,
>    `transport_collectif_personnes`, arbre `major_regionale_ticpe_super_e10` (46/48 copies), `instant_electrite`, `ifp`.
>    Ces doublons restent visibles comme `ipp_csv_id` dupliqués (`ticfe_transport`, `maj_ticpe_super_*`).
> 6. Sous-systèmes manquants : TIRUERT (bloquant pour la TGAP), régions post-2016 à remonter vers les barèmes.
> 7. Dates electro-intensifs 2016→2022 (7 fichiers) : couplé à la politique CIBS.
> 8. Normalisation systématique des dates TICPE côté OF (`YYYY-01-11` → `YYYY-01-01`, ~20 fichiers) : à trancher.
>    `white_spirit` porte désormais la vraie date barème 1994-01-11 à côté de 2000-01-01 (incohérence assumée, cf. ce point).
>
> ### 🔎 Bugs de métadonnées restants **côté barèmes** (non corrigés, à décider)
> `ipp_csv_id` dupliqués : les 6 `taxes_incitatives_carburants/*` portent tous `ticgn_taux` ;
> les 6 tarifs réduits GPL combustible recopient les id des carburants ; `tccfe/*_drom` recopient `tccfe_coef_max`.
>
> **Repo barèmes :** `C:/Users/p.dutronc/Documents/projets/baremes-ipp-yaml`, branche `energies`. Racine énergies : `parameters/taxation_indirecte/energies`.

# Synchronisation `parameters/energies` ↔ barèmes IPP `taxation_indirecte/energies`

Branche barèmes de référence : `energies` (propre, à jour avec `origin/energies`).
Date du rapport : 2026-07-17. Source de vérité = barèmes IPP (vérifiable via URL Légifrance),
sauf erreurs identifiées ci-dessous.

Volumétrie : barèmes = 265 fichiers de paramètres (hors index) ; OF = 314.
Les deux arbres couvrent la même législation mais avec des **architectures divergentes**.

---

## 0. Synthèse : la divergence est structurelle, pas seulement de valeurs

Trois différences d'architecture expliquent l'essentiel des écarts. Aucune n'est une simple
faute de frappe : ce sont des choix de modélisation à trancher.

1. **Découpage territoire / usage / activité.** Les barèmes séparent `metropole/` vs `drom/`,
   puis `carburants/` vs `combustibles/`, puis une arborescence `accise/.../tarifs_reduits/<activité>`.
   OF aplatit tout (pas de split territorial ; noms fusionnés produit+activité, ex.
   `taux_selon_activite/gazoles_transport_routier_de_marchandises.yaml`).

2. **Réforme CIBS 2022 (accise sur les énergies).** Les barèmes **clôturent** chaque paramètre
   d'avant-réforme par `value: null` au 2022-01-01 et **rouvrent** la valeur sous `accise/`.
   OF **n'ajoute jamais** ce `null` de clôture : les paramètres TICGN/TICC/TICPE/TICFE/TCFE
   restent « vivants » indéfiniment et **font doublon** avec les valeurs `accise/`. C'est la
   divergence la plus lourde et la plus systématique (≈ 60 fichiers concernés).

3. **Conditions d'éligibilité = prose côté barèmes, paramètres côté OF.** Les barèmes ne
   paramètrent que des *taux* ; les seuils (SEQE 3 %/0,5 %, intensité électrique, kWh/€ VA…)
   restent en prose dans les `documentation:`. OF a dû créer des paramètres (`seuils_seqe/*`,
   `ticfe/electro_intensive/seuils/*`, `conversion_pcs_pci`, etc.) pour rendre ces conditions
   calculables. **Ces paramètres OF sont légitimes et n'ont pas d'équivalent barèmes.**

---

## 1. Sous-systèmes entièrement présents d'un seul côté

| Sous-système | Côté | Nature | Décision |
|---|---|---|---|
| **TIRUERT / TIRIB** (`taxes_incitatives_carburants/`, 6 params) | barèmes seul | Taxe incitative EnR transports, art. 266 quindecies. **Remplace la TGAP carburants au 2019-01-01.** | À ajouter à OF (sinon la TGAP OF est fausse post-2019, cf. §3) |
| **Régions post-réforme 2016** (`major_regionale_*/depuis_2017/`, `depuis_2022/`, 78 fichiers) | OF seul | 13 régions fusionnées (auvergne_rhone_alpes, grand_est…). Les barèmes n'ont quasi aucune donnée post-2016. | OF a des données que les barèmes n'ont pas → à conserver, remonter vers barèmes |
| **Coefficients TCCFE/TDCFE par collectivité** (`tcfe/tccfe/coefficient.yaml` 35 325 communes, `tdcfe/coefficient.yaml` 103 départements) | OF seul | Données réelles par collectivité ; les barèmes ne publient que l'enveloppe min/max légale. | À conserver dans OF |
| **`seuils_seqe/`, `ticfe/electro_intensive/seuils/`, seuils divers** | OF seul | Seuils d'éligibilité inventés par OF (légitimes, cf. §0.3). | À conserver ; corriger unités/dates (cf. §4) |
| **DROM accise, `renouvelable_autoconsommee`, tarifs réduits 0 (navigation/aéronautique/doubles usages/fabrication minéraux)** | barèmes seul | Tarifs réduits CIBS, valeur 0 (exonérations) sauf plafonds DROM (essences 79.826, gazoles 14.62). OF les code « en dur » (`return 0`) dans les formules. | Décision : paramétrer ou garder en dur |

---

## 2. Erreurs confirmées **dans OF** (à corriger — barèmes a raison)

### 2a. Valeurs fausses (impact économique direct)
| Fichier OF | Date | OF a | Devrait être | Source |
|---|---|---|---|---|
| `autres_produits_energetiques/accise/carburants/carbureacteurs.yaml` | 2022-01-01 | 76.826 | **42.131** | copié du taux essences ; 2023/2024 OK |
| `gaz_naturel/ticgn/taux_normal.yaml` | 1986-01-01 | 9.15 | **9.5** | transposition de chiffres |
| `.../super/super_plombe.yaml` | 1999 | 415.5 | **415.6** | typo |
| `.../emulsion_eau_gazole/autres_hectolitre.yaml` | 2000 | 198.95 | **196.95** | typo |
| `tcfe/tdcfe/coefficient_multiplicateur_{maximum,minimum}.yaml` | 2011+ | copies de TCCFE (8 / 8.5) | max 4→4.25, min 2→2→4.25 | min==max est impossible ; contredit par `tdcfe/coefficient.yaml` |
| `bouclier_tarifaire/majoration_tccfe_maximum.yaml` | 2023-02-01 | 10 `#null originalement` | **null** | surcharge abolie (le fichier _minimum garde null → incohérence interne) |

### 2b. Dates fausses (le `values:` contredit son propre `reference:`/`official_journal_date:`)
- `ticgn/taux_normal.yaml` & `ticgn/taux_reduit_grandes_consommatrices.yaml` : valeur au **2014-01-01**, réf. au 2014-04-01 → décaler à 2014-04-01.
- Les 7 fichiers `ticfe/electro_intensive/{activite_industrielle,concurrence_internationale}/*` : valeurs datées **2016-01-01** alors que la réf. (Ordonnance 2021-1843, art. L312-65 CIBS) est de **2022-01-01**. La série pré-2022 existe déjà ailleurs → double déclaration.
- `tariffs_particuliers/ethanol_diesel_ed95.yaml` : 12.119 daté 2024-01-01, devrait être **2022-08-18** (LFR 2022 art. 9).
- `taux_selon_activite/gazoles_extraction_de_mineraux_industriels.yaml` : 3.86 daté 2022-01-01, devrait être **2023-01-01** (le fichier frère `manutention_portuaire` est correctement daté 2023).

### 2c. Valeurs manquantes (indexations récentes non ingérées ; `last_value_still_valid_on` OF = 2024-08-01, périmé)
- `accise/taux_normal_combustible.yaml` (gaz) : manque **16.37 @2024-01-01** et **17.16 @2025-01-01** (17.16 absent de tout OF).
- `electricite` `tarifs_normaux/{menages,pme}` : manque l'indexation **2025-02-01** (33.7 / 26.23).
- `gaz_naturel/taux_reduit_concurrence_internationale` & `charbon/taux_reduit_concurrence_internationale` : manque **null @2024-01-01** (tarif indirect-SEQE abrogé LF2024) → OF applique un tarif réduit supprimé.
- `taux_selon_activite/gazoles_travaux_agricoles.yaml` : manque le retour à **3.86 @2025-02-16**.
- `taux_selon_activite/gazoles_transport_de_personnes_par_taxi.yaml` : manque **30.2 @2023-01-01**.
- `.../white_spirit_utilise_comme_combustible.yaml` : manque toute la tranche **1994-1999** (42.85).
- `.../gazole/carburants_sous_conditions_hectolitre.yaml` : manque les pics **2020-07-01 (37.68)** et **2020-08-01 (18.82)**.

### 2d. TGAP non terminée (bug à fort impact)
Les 7 `tgap_carburants/*.yaml` mettent `2019-01-01: 0.079` au lieu de `null`. La TGAP carburants
a été **abrogée au 2019-01-01** (remplacée par TIRUERT). OF continue de prélever une taxe morte
indéfiniment. Le `0.079` est d'ailleurs le taux-cible TIRUERT essences 2019, collé par erreur.

### 2e. Métadonnées : `ipp_csv_id` copiés/faux (corromptent tout export CSV par id)
- `charbon/ticc.yaml` : `ticgn_taux` → doit être `ticc_taux` (collision avec le gaz).
- `tcfe/taux_{non_professionnel,professionnel_*}.yaml` : `cspe` (×3) → `tcfe_*`.
- `tcfe/{tccfe,tdcfe}/coefficient_multiplicateur_*.yaml` : `tddce_coef_max` (×4, typo + collision) → `t{cc,dc}fe_coef_{min,max}`.
- `ticfe/taux_normal_36*.yaml` : `ticfe` (×2, générique).
- `ticfe/concurrence_internationale/electro_intensive_13_virgule_5.yaml` & `transport_collectif_personnes.yaml` : ids dupliqués de leurs voisins.
- `charbon/ticc.yaml` : réf. 2007-01-01 pointe la LF 2003 (la TICC est créée par la LFR 2006).

### 2f. Doublons / fichiers fantômes OF
- `ticgn/taux_reduit_legumes.yaml` == `ticgn/taux_reduit_deshydratation.yaml` (même valeur, date, provision).
- `ticfe/transport_collectif_personnes.yaml` == `ticfe/transport_guide.yaml` (octet pour octet ; l'identité « routier » n'est portée que par le nom de fichier).
- `major_regionale_ticpe_super_e10/` == `major_regionale_ticpe_super_95_98/` sauf Corse (46/48 fichiers = copies pures). Le droit ne distingue pas SP95/98 et E10 pour la majoration régionale (sauf cas Corse).
- `instant_electrite` (bas de `taxation_charbon.py`) : artefact de debug (nom typo, `Instant((2023,2,1))` en dur, lit un paramètre électricité). À supprimer.
- `taxation_gaz_naturel.py` : `taxe_interieure_consommation_gaz_naturel_ifp` lit `parameters(...).taxation_energies.natural_gas` (le seul usage de tout le dossier `parameters/taxation_energies/` — un fichier anglophone isolé `natural_gas.yaml`).

### 2g. Descriptions copiées-collées (mauvais texte, valeur parfois OK)
`electricite/ticfe/` : `electricite_fournie_aux_navires` (décrit un data-center), `alimentation_a_quai`
(décrit un aérodrome), `seuil_consommation_par_va_52_23z` (NAF 52.23Z = aérodromes, pas data-centers ;
la réf. pointe l'article data-center). `accise/travaux_agricoles_forestaires.yaml` (gaz) : description
vide + nom mal orthographié (`forestaires`) → indistinguable de la variante carburant.

---

## 3. Erreurs suspectées **dans les barèmes** (à remonter à l'IPP ; ne pas copier tel quel)

1. **`currency_per_hectoliter` sur des tarifs en €/MWh** — bug systématique (≈ 11 fichiers gaz + charbon).
   Corrélation diagnostique : tout fichier accise gaz/charbon à valeur **non nulle** porte `hectolitre`,
   tout fichier à valeur 0 porte `currency_per_mwh` → bug de générateur. Le vrai unité est `currency_per_mwh`.
   (Le sous-arbre pétrole, lui, est correct.)
2. **CTA gaz `unit: currency_per_mwh` sur un pourcentage** — `cta/{transport,distribution}` sont des taux
   (0,157 = 15,7 %). **OF a raison ici (`/1`)** — seul endroit où OF est plus correct que la source.
3. `ipp_csv_id` copiés/non uniques côté barèmes aussi : `bouclier_tarifaire/menages` (= entreprises),
   `tccfe/*_drom` (= métropole), les 6 `taxes_incitatives_carburants/*` (= `ticgn_taux`), les 6 LPG
   combustible (= carburant).
4. Labels copiés : `charbon/.../intensive_energie_SEQE` porte les labels « indirect » ;
   `major_regionale_ticpe_gazole/corse.yaml` `short_label: Basse Normandie` (OF a hérité du bug).
5. Clés orphelines : `ticc.yaml` réf. 2015-04-01 (valeur 2015-01-01) ; `ticgn/taux_reduit_risque_fuite_carbone`
   valeur 2015 sans réf. ; hrefs cassés (`emulsion sous_conditions` réf. 2002 : digit en trop).
6. Date de début TICC : barèmes `2007-06-01`, OF `2007-01-01`, l'article Légifrance cité par les deux = `2007-07-01`. **Trois dates → arbitrage juridique requis.**

---

## 4. Paramètres OF légitimes mais à nettoyer (unités/dates/métadonnées)

- Seuils `%` de VA marqués `kWh_per_euro_VA` (`electro_intensite_*`, doivent être `percent`) ;
  seuils kWh/€ stockés en MWh/€ avec unité kWh (incohérence valeur/unité).
- `seuils_seqe/*`, `ticfe/electro_intensive/seuils/*` datés `2000-01-01` (sentinelle, pas date légale) ;
  le test SEQE 3 %/0,5 % est une création CIBS (2022).
- Clé `reference :` avec espace avant `:` (parsée comme clé `reference ` → réf. perdue) dans plusieurs
  fichiers `electro_intensive/taux_*` et `risque_de_fuite_de_carbone/taux_*`.
- Unité générique `currency` partout dans `ticpe/` et `accise/` OF (le vrai unité — hectolitre / 100 kg /
  100 m³ — n'est plus lisible par machine, seulement dans la description).
- Valeurs post-2022 laissées en **commentaires YAML morts** dans plusieurs fichiers `ticpe/`.
- TODO développeur laissé dans `description:` (`ticgn/seuil_conso_par_va_legumes`, `taux_reduit_legumes`).
- `ticgn/seuil_facture_energie_par_va.yaml` = 0.6744 : **non sourcé**, aucun équivalent barèmes → à vérifier.

---

## 5. Impact sur les formules (Python)

Les formules OF appellent des chemins de paramètres qui **n'existent pas dans les barèmes** :
`energies.charbon.taux_reduit_seqe`, `energies.seuils_seqe.*`, `energies.gaz_naturel.ticgn.conversion_pcs_pci`,
`energies.gaz_naturel.accise.taux_normal_combustible`, etc. Toute restructuration vers l'arbre barèmes
casserait ces appels. Points chauds relevés :
- `taxation_charbon.py` : 7 tarifs réduits codés en dur `return 0` (correspondent aux 7 fichiers
  `tarifs_reduits/*` valeur 0 des barèmes) ; variables `_seqe`/`_concurrence_internationale` avec seul
  `formula_2007_01_01` lisant des paramètres qui commencent en 2022 → `ParameterNotFound` si appelées
  hors du chemin actuel.
- `taxation_gaz_naturel.py` : dépend de `assiette_ticgn` qui renvoie `None`/`return None` mal placé après
  2022 (code mort à nettoyer), et de `conversion_pcs_pci` (hypothèse PCS marquée `***à vérifier`).
- La bascule 2022 (`taxe_gaz_naturel` → `taxe_accise_gaz_naturel`) suppose que les paramètres accise
  existent ET que les paramètres TICGN s'arrêtent — or OF n'a pas mis les `null`, donc les deux séries
  coexistent.

---

## 6. Séquencement proposé (après décisions)

1. **Corrections « sans regret »** (indépendantes de l'architecture) : §2a valeurs fausses, §2e ids,
   §2f doublons/fantômes, §2c indexations manquantes, §2d TGAP, §2g descriptions. Barèmes = arbitre.
2. **Politique CIBS 2022** (§0.2) : décider `null`-de-clôture + lecture des `accise/` post-2022,
   puis propager aux ~60 fichiers et aux formules de bascule.
3. **Sous-systèmes manquants** (§1) : TIRUERT (bloquant pour la TGAP), remontée des régions post-2016.
4. **Métadonnées / unités** (§3, §4) : appliquer les bonnes unités (ne pas copier le bug hectolitre),
   remonter `ipp_csv_id`/`reference`/`last_value_still_valid_on` des barèmes vers OF.
5. **Formules** (§5) : mettre à jour les chemins de paramètres, nettoyer le code mort, revérifier les tests
   `tests/taxes/taxes_energies/*`.
