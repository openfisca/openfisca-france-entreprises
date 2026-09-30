# Actions en attente

> État au **2026-09-30**. Ce fichier est la seule liste tenue à jour de ce qui reste à faire sur le
> chantier énergies. Les confrontations aux données réelles ont chacune leur document :
> `AGREGATS_TIC.md` (déclarations 2040-TIC), `ELFE.md` et `VMT2.md` sur leurs branches respectives.
>
> Les anciens `SYNC_ENERGIES_REPORT.md` (journal de synchronisation avec le barème, juillet-août
> 2026) et `ARBITRAGES_JURIDIQUES_ENERGIES.md` (huit arbitrages, tous tranchés, un seul resté sans
> application : anomalie n° 2) ont été retirés. Leur contenu est clos, et consultable dans
> l'historique git (`git show 5297c30:<fichier>`).

## Branches

`main` est en 1.1.7 (PR #31 fusionnée le 2026-08-17).

| branche | vs `main` | état | action |
|---|---|---|---|
| `assets/agregats-tic` | +26 | **PR #32**, 2.0.0, CI verte, sans revue depuis le 2026-08-17 | faire revoir et fusionner (*merge commit*, pas *squash* : les messages portent la provenance juridique) |
| `assets/elfe-cgdd` | +8 / −13 | poussée, sans PR | rattraper `main` après #32 |
| `assets/vmt2-depenses-fiscales` | +7 / −13 | poussée, sans PR | idem |
| `origin/Implementation-SEQE` | +8 / −66 | chantier d'Arthur Bidel, arrêté le 2026-07-22 | à coordonner : il embarque un ancien commit d'agrégats (`b6203bb`) |
| `origin/refactor/energies-periodes-mensuelles` | +9 / −44 | superseded, son intention a été ré-appliquée | **à supprimer** |
| `feat/periodes-mensuelles` (locale) | amont supprimé | fusionnée | **à supprimer** |

## Côté barème

Contre `master` `fe2cdff89` : 397 chemins communs, **0 écart de valeur**, 45 fichiers qui ne
diffèrent que par les métadonnées (nettoyage Unicode du 2026-09-21). Miroir trivial, en conservant
les deux `electricite/tcfe/*/coefficient.yaml`, propres à OF-E. Les MR !659, !660 et !661 sont
fusionnées.

Branches du barème qui **déplaceront des chiffres** ici une fois fusionnées :

- `bouclier_tarifs_reduits` — le bouclier couvrait aussi les tarifs réduits (L. 312-48, L. 312-64,
  L. 312-65). Aucune MR ouverte. Effet attendu sur les agrégats : voir la suite n° 1 d'`AGREGATS_TIC.md`.
- La pile `energies_accise_*` — tarifs datés dans le futur (accise 2026-08, GNR 2027-2030,
  électricité 2027-02).

Corrections à faire remonter au barème, puis à reprendre ici :

- **Réfaction corse, SP95-E10** : l'indice 11 ter n'entre dans la réfaction qu'au **2019-07-01**
  (LEGIARTI000037988891), les deux dépôts le datent du 2019-01-01.
- **`coefficients_conversion/*`** datés du 2023-01-01, alors que la TIRUERT les lit depuis 2019 : OF-E
  se replie explicitement sur la première valeur.
- **Intervention des véhicules d'incendie et de secours** : voir l'anomalie n° 2 ci-dessous. Sa
  `documentation`, identique dans les deux dépôts, renvoie encore à `SYNC_ENERGIES_REPORT.md`.

## 🐛 Défauts du modèle, non corrigés

1. **Le modèle ne tourne pas à plus d'un établissement.** `if` et `max` Python appliqués à des
   tableaux dans `variables_economiques.py` (l. 29, 48, 70, 98) et dans `taxation_gaz_naturel.py`
   (`assiette_ticgn`). Tous les tests étant mono-établissement, la suite ne le voit pas. Bloquant
   pour toute simulation sur données d'entreprises. Ajouter un test à plusieurs établissements
   hétérogènes avant de corriger.
2. **Intervention des véhicules d'incendie et de secours : l'arbitrage n'est pas appliqué.** Il a
   été tranché au **2023-07-12** (art. 50 de la loi 2023-580 ; décret 2024-241 art. 5), mais le
   paramètre ouvre toujours à zéro au 2022-01-01, dans les deux dépôts. Le modèle exonère donc
   2022 et le premier semestre 2023 au lieu d'appliquer le tarif normal.
3. **`risque_de_fuite_carbone_eta`** n'applique que la liste 2019/708 (2021-2030) et vaut `False`
   avant 2019 : la liste 2015-2020 manque.
4. **Bouclier tarifaire, traitement mensuel inachevé.** 2022, 2023 et 2025 lisent un instant forcé
   et proratisent à la main (`Instant((2022, 2, 1))`, `/12`, `*11/12`). Seul 2024 est scindé
   (constat n° 10 d'`AGREGATS_TIC.md`).
5. **Paramètres en dur dans les formules** : issue #17.

## ⚖️ Décisions humaines

6. **Comment OF-E consomme le barème.** Démontré le 2026-08-12 : remplacer l'arbre d'OF-E par celui
   du barème fait passer toute la suite, **à condition** d'y ajouter les deux fichiers de
   coefficients TCFE, que le barème range hors de `parameters/` (dans `donnees_locales_tcfe/`).
   Contraintes : deux sources et non une ; pas de lien symbolique (Windows) ; une version épinglée
   et relevée délibérément. Mécanismes en lice : sous-module git, dépendance versionnée, paquet
   `openfisca_baremes_ipp`, ou **greffe dans le code** — `__init__.py` charge l'arbre du barème et le
   rattache comme nœud `energies`, avec les deux fichiers TCFE. La greffe règle à la fois la question
   des deux sources et celle des liens symboliques. L'écart actuel, réduit aux métadonnées, en fait
   le bon moment.
7. **Choix de modélisation du gaz à confirmer** : le double usage passe par `gaz_matiere_premiere`
   OU `gaz_huiles_minerales`, avec un seuil de 800 Wh/€ de VA pour la grande consommatrice ; et
   `taxe_interieure_consommation_gaz_naturel_grande_consommatrice` pointe `taux_reduit_seqe` depuis
   2022.
8. **Les sept tarifs de `autres_produits_energetiques/accise/taux_selon_activite/`** n'ont ni
   `ipp_csv_id` ni référence : il faut un choix de nommage et un travail de sourçage.
9. **`Implementation-SEQE`** : rebaser, reprendre ou abandonner, avec Arthur Bidel.

## 🔧 Hors de portée de l'agent

10. **Ouvrir l'issue sur les chiffres publiés déplacés** par la moyenne mensuelle (mesurés le
    2026-08-12, avant la bascule en périodes mensuelles de la 2.0.0, qui a pu les déplacer à nouveau) :

    | série | avant | après | cause |
    |---|---|---|---|
    | CSPE 2012 (assiette 1 000) | 9 000 | 9 750 | 9 €/MWh jusqu'au 30 juin, 10,5 ensuite |
    | `taxe_electricite` 2012 | 18 090 | 18 840 | idem, par report |
    | TICPE 2020 | 1 037 420 | 1 022 571,6875 | GPL +7,215 ; émulsions −5,165 et −18,470 ; gazole sous conditions +1,5717 |
    | TICC 2007 | 1 190 | 595 | taxe créée au 1er juillet |
    | CSPE 2011 (non testée) | 8,125 | 8,25 | date au 2011-07-01 et non au 2011-07-31 |

11. **Fermer l'issue #4** (PCS/PCI), tranchée le 2026-08-13 : constat n° 9 d'`AGREGATS_TIC.md`.

## ✅ Clos depuis le 2026-08-12

- PR #31 (périodes mensuelles) fusionnée ; MR barème !660 et !661 fusionnées.
- Identifiants PISTE de `legisdata` rétablis : les arbitrages se vérifient de nouveau au texte.
- PCS/PCI : facteur 1,11 retiré (constat n° 9).
- Codes département : les sept sites acceptent `2A`/`2B` et `02A`/`02B`.
- `variables_economiques.py` formaté, la CI passe.
- `seuil_facture_energie_par_va` (0,6744) est sourcé (article L. 312-62 du CIBS) et conservé.
- Descriptions des trois `categorie_fiscale_*` remplies.
- Majorations régionales, TIRUERT (tarif en €/hL, assiette en volume) et réfaction corse (close au
  2022-01-01, article 265 quinquies) : convergés avec le barème le 2026-08-16.
