# Actions en attente — synchronisation énergies

> État arrêté au **2026-08-12**. Ce fichier liste ce qui **ne peut pas être fait depuis l'agent** :
> actions nécessitant un outil absent, un autre dépôt, ou une décision humaine. Le suivi technique
> reste dans `SYNC_ENERGIES_REPORT.md` (bloc de reprise en tête) et
> `ARBITRAGES_JURIDIQUES_ENERGIES.md`.

## Branches — au 2026-08-12

`main` (`b3cfa50`) est le tronc. `feat/periodes-mensuelles` porte 9 commits au-dessus, **205 tests
verts**, rebasée sur `main` et *fast-forwardable* : c'est le travail énergies à fusionner.

| branche | état vs `main` | action |
|---|---|---|
| `feat/periodes-mensuelles` | 9 commits, verte | **ouvrir la PR** — cf. §1 |
| `origin/add_parameters` | ⊂ `main` | **à supprimer** |
| `origin/fix/regions-post-2016` | ⊂ `main` | **à supprimer** |
| `origin/align/energies-tree` | superseded (rien d'unique) | **à supprimer** |
| `origin/refactor/energies-periodes-mensuelles` | superseded — son intention a été **ré-appliquée** sur `main`, cf. §1 | **à supprimer** |
| `origin/Implementation-SEQE` | commits uniques | chantier distinct |
| `origin/assets/agregats-tic` | commits uniques | chantier distinct |
| `origin/assets/elfe-cgdd` | commits uniques | chantier distinct |

Branches locales périmées (⊂ `main`, fusionnées par les PR #28, #29 et #30) : `chore/hygiene-symlink`,
`docs/arbitrages-energies`, `feat/tarif-moyen-annuel`.

## État côté barème

| MR IPP | objet | état |
|---|---|---|
| !659 | GNR : clôture au 2022-01-01 et non au 2021-07-01 | **fusionnée** |
| !660 | TICC : création au 2007-07-01, référence à l'article 36 III | **ouverte** |
| !661 | Hygiène de métadonnées : unités, ids, descriptions, références | **ouverte** |

⚠️ Les paramètres d'OF-E reprennent déjà le contenu de !660 et !661. **La convergence annoncée
(321 chemins communs identiques octet pour octet) suppose que ces deux MR soient fusionnées.** Si la
revue les amende, OF-E demande un commit de suivi. Le point le plus exposé est le renommage de deux
`ipp_csv_id` dans !661, qui change deux noms de séries à l'export CSV / DBnomics.

---

## 🔧 Impossibles depuis l'agent (outillage)

1. **Ouvrir la PR de `feat/periodes-mensuelles` vers `main`.** `gh` n'est pas installé ; l'URL est
   imprimée par GitHub au push. **Ne pas écraser les commits** (*merge commit*, pas *squash*) : les
   neuf messages portent le raisonnement juridique de chaque arbitrage, ses sources et les chiffres
   déplacés. C'est la provenance de tout l'exercice.
   À signaler dans le corps de la PR : le message du premier commit (`1eec057`) porte encore
   « NE PAS FUSIONNER EN L'ÉTAT — la suite de tests est rouge » et « branche locale, non poussée ».
   Les deux sont **périmés** depuis huit commits ; les réécrire imposerait un nouveau *force-push*.

2. **Ouvrir l'issue OF-E** sur les chiffres publiés déplacés. Deux ensembles :
   - **Majorations régionales** (commit `8eb5cfb`) — divergences barème/OF adoptées :
     super `{rhone_alpes 2010, limousin 2010, poitou_charentes 2010/2014/2015}` ;
     gazole `{rhone_alpes 2010, limousin 2010, corse 2010/2014-16, poitou_charentes 2010/2014/2015}`.
     Plusieurs sont probablement des artefacts de grille de dates : à vérifier sur Légifrance.
   - **Moyenne mensuelle des tarifs** — le tableau complet, avec décomposition de chaque écart, est
     en §B du bloc de reprise de `SYNC_ENERGIES_REPORT.md` : CSPE 2012 (9 000 → 9 750),
     `taxe_electricite` 2012 (18 090 → 18 840), TICPE 2020 (1 037 420 → 1 022 571,6875),
     TICC 2007 (1 190 → 595), CSPE 2011 (8,125 → 8,25, non testée).

3. **Régénérer les identifiants PISTE de `legisdata`.** Ils renvoient `invalid_client` : l'API
   Légifrance est inutilisable en l'état. Le cache `sources/legifrance/265_*.md` qu'invoque le §5 des
   arbitrages n'est pas non plus dans le dépôt. **Aucune décision énergies n'est donc reproductible
   depuis les sources primaires via legisdata** ; les vérifications du 2026-08-12 ont été faites sur
   les versions consolidées de Légifrance en direct.

---

## ⚖️ Décisions humaines

4. ~~**Arbitrage §7 — PCS/PCI (facteur 1,11)**~~ — **tranché le 2026-08-13**. Les données
   déclarées changent de nature en même temps que la loi : quand le texte exprime le tarif en
   PCS, l'assiette est en PCS ; quand il l'exprime en PCI, elle est en PCI. Il n'y a donc jamais
   deux unités à réconcilier, et la conversion n'a pas lieu d'être. Le facteur est retiré des
   trois sites qui l'appliquaient ; le paramètre reste au barème, le coefficient physique
   existant. Les agrégats confirment : la case `_911237` déclare 8,4300 tout rond, et le rapport
   modèle/déclaration valait 1,11 exactement, sans résidu, sur les quatre millésimes. Voir le
   constat n° 9 d'`AGREGATS_TIC.md`. La discontinuité qu'on croyait voir en 2022 disparaît par
   la même occasion : il n'y en avait jamais eu, le facteur était simplement en trop avant.

5. **Confirmer les choix de modélisation** listés en fin de doc d'arbitrages : rétablissements du
   chemin gaz (`gaz_matiere_premiere` OU `gaz_huiles_minerales` ; seuil 800 Wh/€ VA),
   `taxe_interieure_consommation_gaz_naturel_grande_consommatrice` pointant désormais
   `taux_reduit_seqe`, et suppression éventuelle de `seuil_facture_energie_par_va` (0,6744) — non
   sourcé et **confirmé lu par aucune formule** (il ne subsiste que dans un commentaire).

6. **Compléter les sept tarifs de `taux_selon_activite/`.** Ils étaient des ébauches sans description
   ni `metadata` ; !661 leur donne description et unité, mais il leur manque un `ipp_csv_id` — un
   choix de nommage — et une référence — un travail de sourçage.

7. **Quatre descriptions vides restantes au barème**, hors périmètre de !661 :
   `minoration_corse` et les trois `categorie_fiscale_*`. Ces derniers placent en outre `reference`
   et `unit` **au niveau racine et non sous `metadata`**, si bien que leur unité n'est pas là où un
   consommateur la cherche ; l'un porte un commentaire `#cette parametre est pas utilisée`.

---

## 🐛 Anomalies relevées, non corrigées

8. **Codes département incohérents — bug latent.** Certaines formules utilisent `"2A"`/`"2B"`,
   d'autres `"02A"`/`"02B"`. La Corse peut tomber silencieusement sur `default=0` selon la façon dont
   `departement` est renseigné. Rencontré deux fois pendant les vérifications. Mérite une issue.

9. **`variables_economiques.py` non formaté** (échoue `ruff format --check`, vérifié le 2026-08-12).
   **Préexistant**, hors périmètre de ces travaux, mais fera échouer la CI si ce contrôle est appliqué.

---

## 📋 Reporté volontairement

10. **Item 6 — comment OF-E consomme le barème.** Sous-module git, dépendance versionnée, ou paquet
    `.openfisca/openfisca_baremes_ipp`. **Note de décision complète en §C du bloc de reprise de
    `SYNC_ENERGIES_REPORT.md`** : ce qui est démontré par l'expérience de bascule, les trois
    contraintes (deux sources et non une, liens symboliques pénibles sous Windows, nécessité
    d'épingler une version) et les trois mécanismes comparés. Sa propre branche + PR.

11. **Bouclier tarifaire** — traitement mensuel propre à faire. Il proratise aujourd'hui à la main
    (`Instant((2022, 2, 1))`, `/12`, `*11/12`) et encode un **basculement de régime**, pas un
    changement de tarif : la moyenne de tarif y serait fausse.

---

## ✅ Clos depuis le 2026-07-31

- **Rapatriement de `refactor/energies-periodes-mensuelles`** — fait par ré-application sur l'arbre
  de `main` : helper `tarif_moyen_annuel` porté, 230 lectures enveloppées, arbitrages §2 et §5 posés.
- **Arbitrage §2** (TICGN au 2014-04-01), **§3** (manutention portuaire) et **§5** (abrogations
  TICPE) — implémentés, avec repli sur le tarif normal là où une ligne de tarif réduit disparaît
  sans successeur.
- **§1** (date de création de la TICC) — tranché au 2007-07-01, porté des deux côtés.
- **Défauts de métadonnées du barème** (ancien point 8) — traités par !661. La lacune supposée des
  six `ipp_csv_id` de GPL combustible **n'existait pas** : le sous-arbre n'en comptait qu'une, sur
  `tccfe_coef_max`.
- **Lacune de couverture supposée** (ancien point 9) :
  `gaz_de_petrole_liquefies_combustible_travaux_agricoles` (0,712) **est présent** au barème.
- **Propositions barème sécurisées** (`_propositions_regions_post_2016/`,
  `_propositions_refaction_corse/`) — intégrées : réfaction corse et régions post-2016 sont sur
  `master` du barème.
- **Dépendance d'enchaînement sur `sync/energies-no-regret`** — sans objet, la branche n'existe plus
  et `tarif_moyen_annuel` est sur `main`.
