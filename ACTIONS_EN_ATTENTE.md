# Actions en attente — synchronisation énergies

> État arrêté au **2026-07-24**, **table des branches remise à jour le 2026-07-31**. Ce fichier liste
> ce qui **ne peut pas être fait depuis l'agent** : actions nécessitant un outil absent, un autre
> dépôt, ou une décision humaine. Le suivi technique reste dans `SYNC_ENERGIES_REPORT.md` (bloc de
> reprise) et `ARBITRAGES_JURIDIQUES_ENERGIES.md`.

## Branches (dépôt OpenFisca-France-Entreprises) — au 2026-07-31

`main` (`5be7c9c`, PR #26) est le tronc : il absorbe `sync/energies-no-regret`,
`fix/regions-post-2016` et `convergence/energies` — **les trois ont été supprimées d'`origin`** — ainsi
que le contenu d'`align/energies-tree`. 205 tests passent.

| branche | état | action |
|---|---|---|
| `align/energies-tree` | superseded (rien d'unique vs `main`) | **à supprimer** |
| `fix/regions-post-2016` | ⊂ `main` | **à supprimer** |
| `add_parameters` | ⊂ `main` | **à supprimer** |
| `refactor/energies-periodes-mensuelles` | 9 commits uniques | rapatriement non mécanique — cf. §3 du rapport |
| `Implementation-SEQE` | 8 commits uniques | chantier distinct |
| `assets/agregats-tic` | 3 commits uniques | chantier distinct |

⚠️ Les branches locales périmées à nettoyer aussi : `sync/energies-no-regret`, `convergence/energies`,
`stage_chieh` (supprimée d'`origin`).

---

## ✅ Fait le 2026-07-27 — propositions barème sécurisées

Les 32 fichiers de proposition sont désormais **commités** dans le dépôt barème, sur la branche
`energies-propositions-openfisca` (commit `eae753da2`, basée sur `origin/energies` à jour), sous
`_propositions_regions_post_2016/` (27) et `_propositions_refaction_corse/` (5). Plus aucun risque de
perte : ils vivent dans l'object store git, indépendamment du worktree. Le dépôt principal reste sur
`master`, intact.

**Reste à faire** (côté humain) :
- **Pousser** la branche : `git -C ../baremes-ipp-yaml push -u origin energies-propositions-openfisca`
  (l'agent ne pousse pas de lui-même sur le dépôt barème ; `gh` est absent de toute façon).
- **Intégrer** les propositions dans l'arbre (`parameters/taxation_indirecte/energies/…`) puis PR vers
  `energies`. Décisions dans chaque README : nouvelles régions contre extension des fichiers existants
  (`bretagne`, `corse`, `paca`, `ile_de_france`), nommage `ile_france` (OF) / `ile_de_france` (barème),
  `ipp_csv_id` INSEE à valider.

---

## 🔧 Impossibles depuis l'agent (outillage)

1. **Ouvrir la PR** de `refactor/energies-periodes-mensuelles` vers `sync/energies-no-regret`.
   `gh` n'est pas installé. Texte complet prêt (titre, base/head, corps) dans le scratchpad de session :
   `PR_periodes_mensuelles.md`. Lien :
   `https://github.com/openfisca/openfisca-france-entreprises/pull/new/refactor/energies-periodes-mensuelles`

2. **Ouvrir l'issue OFF-E.** Elle doit couvrir **deux** ensembles distincts de changements de taxe :
   - **Majorations régionales** (commit `8eb5cfb`) — divergences barème/OF adoptées :
     super `{rhone_alpes 2010, limousin 2010, poitou_charentes 2010/2014/2015}` ;
     gazole `{rhone_alpes 2010, limousin 2010, corse 2010/2014-16, poitou_charentes 2010/2014/2015}`.
     Plusieurs sont probablement des artefacts de grille de dates : à vérifier sur Légifrance.
   - **Moyenne mensuelle des tarifs** (branche `refactor`) — 12 couples (tarif, année) sur 1993, 2010,
     2014, 2020 ; plus TICC 2014 (1 190 → 2 015), TICGN 1993-2000, CSPE 2011-2012, gazole agricole
     2025 (9 560 → 4 810), ED95 2022. Ce sont des corrections, mais elles déplacent des chiffres publiés.

---

## ⚖️ Décisions humaines

3. **Arbitrage §5 — abrogations TICPE**, produit par produit : `gazole_b_10` (2019),
   `emulsion_eau_gazole/*` et `*/sous_conditions*` (2020-07-01), `gazole/carburants_sous_conditions`
   (2021-07-01), `fioul_lourd_bts`/`hts`/`point_eclair` (2003), `essence_normale` (2000).
   **Plus de blocage technique** : la moyenne mensuelle gère les dates en cours d'année.

4. **Arbitrage §7 — PCS/PCI (facteur 1,11)** : le gaz est taxé `conso × taux × 1,11` avant 2022 et
   sans conversion après, d'où une discontinuité. Préexistant, signalé par `***faut vérrifier`.

5. **Confirmer les choix de modélisation** listés en fin de doc d'arbitrages : rétablissements du
   chemin gaz (`gaz_matiere_premiere` OU `gaz_huiles_minerales` ; seuil 800 Wh/€ VA),
   `taxe_interieure_consommation_gaz_naturel_grande_consommatrice` pointant désormais
   `taux_reduit_seqe`, et suppression éventuelle de `seuil_facture_energie_par_va` (0,6744), non
   sourcé et plus lu par aucune formule.

---

## 🔗 Dépendance d'enchaînement

6. **Les arbitrages §2, §4 et §5 ne peuvent pas être implémentés sur `sync/energies-no-regret`** :
   `tarif_moyen_annuel` n'existe que sur la branche `refactor`. Fusionner la PR d'abord, ou réaliser
   ces implémentations sur la branche `refactor`.

---

## 🐛 Anomalies relevées, non corrigées

7. **Codes département incohérents — bug latent.** Certaines formules utilisent `"2A"`/`"2B"`,
   d'autres `"02A"`/`"02B"`. La Corse peut tomber silencieusement sur `default=0` selon la façon dont
   `departement` est renseigné. Rencontré deux fois pendant les vérifications. Mérite une issue.

8. **Défauts du barème à corriger en amont** (vérifiés sur `origin/energies`) :
   - `electricite/accise/tarifs_reduits/production_navires.yaml` : la `documentation` décrit la
     manutention portuaire, pas la production à bord ;
   - `.../carburants/huiles_lourdes/tarifs_reduits/manutention_portuaire.yaml` : valeur datée
     2023-01-01 mais référence datée 2022-01-01, et **pas d'`official_journal_date`** ;
   - `.../carburants/huiles_lourdes/tarifs_reduits/transport_routier_marchandises.yaml` : **pas d'`unit`** ;
   - (préexistants) les 6 tarifs GPL combustible reprennent les `ipp_csv_id` des carburants ;
     `tccfe_coef_max` est partagé par trois fichiers.

9. **Lacune de couverture du barème** : `gaz_de_petrole_liquefies_combustible_travaux_agricoles`
   (0,712) existe côté OF mais **manque au barème**. À proposer.

---

## 📋 Reporté volontairement

10. **Item 6** — restructuration par grade / référence directe au barème. Sa propre branche + PR.
    Suppose encore de trancher le mode de consommation du barème : sous-module git, dépendance
    versionnée, ou paquet `.openfisca/openfisca_baremes_ipp`.

11. **Bouclier tarifaire** — traitement mensuel propre à faire. Il proratise aujourd'hui à la main
    (`Instant((2022, 2, 1))`, `/12`, `*11/12`) et encode un **basculement de régime**, pas un
    changement de tarif : la moyenne de tarif y serait fausse.

12. **`variables_economiques.py` non formaté** (échoue `ruff format --check`). **Préexistant**, hors
    périmètre de ces travaux, mais fera échouer la CI si ce contrôle est appliqué.
