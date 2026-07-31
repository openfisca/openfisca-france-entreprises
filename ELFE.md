# Tests adossés au modèle Elfe (CGDD) — plan

État au 2026-07-31. **Rien n'est encore porté sur une branche** : ce document
prépare le travail, à ouvrir une fois les branches `energies` fusionnées.

Modèle de référence : la branche `assets/agregats-tic` d'openfisca-france-entreprises
(agrégats 2040-TIC → 94 tests générés + rapport d'audit). Même architecture ici.

---

## 1. La donnée

**Source** : application Shiny du CGDD,
<https://ssm-ecologie.shinyapps.io/Tarification_effective_carbone_et_energie/>.
Le code du modèle Elfe n'est pas publié ; seuls les résultats le sont.

**Licence** : etalab-2.0 (mention explicite en pied de l'application). La donnée est
donc redistribuable dans le dépôt, sous réserve d'attribution — c'est ce qui autorise
à la committer comme `assets/agregats.csv` l'a été.

**Extraction** : l'application n'expose pas de fichier statique ; toute l'interface
est rendue côté serveur. Un client du protocole Shiny (websocket
`/_w_<worker>/__sockjs__/…/websocket`) ouvre une session, positionne les trois
sélecteurs, puis tire le `downloadHandler` `downloadData`, qui renvoie le tableau
courant en `.xlsx`. Script : `scripts/elfe/telechargement.py`.

**Plan d'expérience** : 3 sélecteurs.

| sélecteur | valeurs |
|---|---|
| `choix_1` — périmètre | `Carbone`, `Energie` |
| `choix_2` — dimension | `Régime fiscal`, `Secteur économique`, `Agents`, `Type de produit`, `Instruments`, `Gaz à effet de serre` |
| `choix_3` — millésime | `2014` … `2023`, `2024*` |

132 combinaisons théoriques, **106 réelles** — toutes extraites. Deux absences,
toutes deux structurelles et non accidentelles :

- le périmètre `Energie` ne commence qu'**en 2017** (2014-2016 renvoient un HTTP 500),
  ce qui recoupe la documentation du CGDD → 18 combinaisons ;
- le croisement `Energie × Gaz à effet de serre` **n'existe pas** : ventiler des
  consommations d'énergie par gaz à effet de serre n'a pas de sens, et l'application
  renvoie une erreur sur les huit millésimes → 8 combinaisons.

**Le millésime `2024*` est provisoire, et il faut savoir en quoi.** Son total
d'émissions est *rigoureusement identique* à celui de 2023 (400,22 MtCO2 au
centième), parce que le bilan énergétique n'a pas été actualisé — le CGDD vieillit
la base PEFA. En revanche la ventilation entre régimes et les tarifs, eux, sont
bien mis à jour : 64 paliers distincts en 2024 contre 62 en 2023, dont 21 nouveaux.
Conclusion pour les tests : **2024\* est utilisable côté tarifs, pas côté
quantités**. Comme les tests Tier 1 ne portent que sur le tarif (assiette unitaire),
cela ne les gêne pas ; mais aucune analyse pondérée ne doit traiter 2024 comme une
observation indépendante de 2023.

**Structure d'un tableau** — quatre colonnes, une ligne par palier tarifaire :

| Tarification effective (€/MWh ou €/tCO2) | catégorie | Quantités (TWh ou MtCO2) | Somme cumulée |
|---|---|---|---|
| 60,75 | Gazole - transport routier | 180,895 | 1 579,98 |

La dimension `Instruments` fait exception : neuf colonnes, qui **décomposent** le
tarif effectif — `Taux de taxation`, `Composante carbone`, `Boucliers et aides`,
`Prix des quotas ETS`, `Prix réel des quotas ETS`, `Montant remboursement indirect
ETS`. C'est le tableau le plus utile (cf. §3).

### Pourquoi ces agrégats testent le modèle

Même argument que pour les agrégats 2040-TIC, mais inversé. Là-bas on disposait d'un
couple (quantité, montant) dont le rapport restituait le tarif. Ici le **tarif est
donné directement**, et la quantité sert de pondération.

Chaque ligne est une cellule tarifaire homogène : un couple (produit, régime, tarif),
à l'intérieur duquel l'accise est linéaire. Un test se pose donc en une ligne :
injecter 1 MWh dans la variable de consommation correspondante et attendre le tarif.

Vérification de la lisibilité du signal, sur `Energie × Régime fiscal × 2023` :

| régime | paliers distincts (€/MWh) |
|---|---|
| Gazole - transport routier | 59,400 / 60,480 / 60,750 / 62,640 |
| Essence - transport routier | 75,701 / 76,826 / 77,479 / 77,647 / 78,795 |

Quatre et cinq paliers pour un même régime, chacun portant une quantité propre : ce
n'est pas du bruit d'agrégation, c'est une grille de taux. Deux constats vérifiés,
et une question ouverte qu'il ne faut pas trancher trop vite.

**Vérifié** : le palier bas du gazole routier vaut 59,400, et le tarif de base de la
TICPE gazole au barème vaut **59,40 depuis 2018**
(`taxation_indirecte/produits_energetiques/ticpe/gazole/gazole.yaml`). Les trois
autres paliers s'en déduisent par addition : +1,08, +1,35, +3,24.

**Question ouverte n° 1 — l'unité.** Le barème est en €/hL, la colonne Elfe est
titrée €/MWh, et les deux nombres coïncident. Soit Elfe applique un PCI de 1 MWh/hL
au gazole (le PCI physique vaut ≈ 0,99), soit la coïncidence est fortuite. À
établir avant tout test : c'est la calibration évoquée au §4.

**Question ouverte n° 2 — la grille.** Les écarts additifs (+1,08 / +1,35 / +3,24)
ne se retrouvent pas tels quels dans `major_regionale_ticpe_gazole/`, dont les
valeurs vont de 0 à 4,39. Mais ce répertoire est encore découpé selon les **régions
d'avant 2016** (alsace, aquitaine, auvergne…), donc ses valeurs ne décrivent plus
2023. L'interprétation « modulations régionales » reste la plus plausible, mais elle
n'est pas démontrée par les données seules — et c'est précisément ce qui fait de
`fix/regions-post-2016` un prérequis dur (§6) plutôt qu'un simple confort.

---

## 2. Où ranger la donnée

Sur une branche `assets/elfe-cgdd` d'**openfisca-france-entreprises**, en miroir
exact de `assets/agregats-tic` :

    assets/elfe/
      elfe.csv          tableau long consolidé, toutes dimensions sauf Instruments
                        colonnes : perimetre, dimension, millesime, tarif,
                                   categorie, quantite, quantite_cumulee
      elfe_instruments.csv        la décomposition à neuf colonnes
      facteurs_emission_cgdd.csv  facteurs implicites du CGDD — série externe de
                                  comparaison, **pas** des paramètres (cf. Tier 3)
      SOURCES.md        URL, date d'extraction, licence etalab-2.0, plan d'expérience
    scripts/elfe/
      telechargement.py client Shiny + moissonnage (extraction reproductible)
      donnees.py        lecture, pivot, paliers distincts par régime
      correspondance.py régime Elfe → variable / entrées / paramètre du barème
      audit.py          confrontation au barème, en €/MWh (CLI)
      audit_ecarts.py   décomposition droit / facteur d'émission (CLI, hors CI)
      generer_tests.py  génération des tests YAML (CLI)
      arbitrages/       cas en échec volontaire, hors CI

Le fait que `facteurs_emission_cgdd.csv` soit rangé dans `assets/` et non dans
`parameters/` n'est pas cosmétique : c'est ce qui matérialise que ces facteurs sont
une observation externe, et non une règle que le modèle applique.

Un seul CSV consolidé plutôt que 114 `.xlsx` : ~12 000 lignes, du même ordre que les
851 lignes d'`agregats.csv`, et diffable. Les `.xlsx` bruts restent hors dépôt —
`telechargement.py` les régénère.

**Réserve sur le dépôt d'accueil — à arbitrer.** `assets/agregats-tic` est sur
openfisca-france-entreprises, et c'est là que vivent les variables d'accise : c'est
le choix par défaut. Mais Elfe couvre aussi les ménages, et pas marginalement — la
dimension `Agents` leur attribue **105,7 MtCO2 sur 400,2 en 2023, soit 26 %** du
champ carbone, ce qui relève d'openfisca-france-indirect-taxation.

Ce qui tranche, à mon sens : le **tarif est indépendant de l'agent**. La dimension
`Agents` ne ventile que des quantités, pas des taux. Comme les tests Tier 1 portent
sur le tarif à assiette unitaire, ils sont indifférents au partage ménages /
entreprises. Je propose donc de tout héberger sur OFFE, et de ne considérer OFFIT
que si l'on veut plus tard des tests *pondérés* (masses de recettes), qui eux
exigeraient les deux calculateurs.

---

## 3. Ce qui est testable, et ce qui ne l'est pas

C'est le point structurant. Le tarif effectif Elfe est une **somme d'instruments** :

    tarif effectif = taux de taxation (accise)
                   + composante carbone
                   + prix des quotas ETS
                   − boucliers et aides

Notre calculateur ne couvre que l'accise et les boucliers. Confronter le tarif
effectif *total* au résultat du modèle serait donc systématiquement faux. D'où
quatre familles, par ordre de solidité décroissante :

### Tier 1 — `Energie × Régime fiscal` (direct)

Pour les régimes purement accise (pas d'ETS : transport routier, fioul domestique,
GPL combustible…), le tarif en €/MWh **est** le tarif d'accise. Test : 1 MWh dans la
variable de consommation, attendu = tarif Elfe.

**Volume mesuré** : 62 régimes distincts sur le périmètre Énergie, 8 millésimes
(2017-2024). En comptant les paliers distincts par régime, tous millésimes
confondus, on sépare nettement deux populations :

| paliers distincts / 8 millésimes | lecture | nombre de régimes |
|---|---|---|
| ≤ 8 (≈ un par an) | taux stable dans l'année → **testable** | **34** |
| 9 à 14 | modulation régionale ou pas infra-annuel | 22 |
| 25-26 (charbon, gaz grande conso) | variation du prix ETS | 6 |

Les 34 premiers sont la cible immédiate du Tier 1 : ~270 cas générés, du même ordre
que les 94 cas des agrégats 2040-TIC.

Les six derniers confirment le besoin du Tier 2 : « Charbon - Double usage » affiche
25 paliers alors que le double usage est *exonéré d'accise*. Ce qui varie n'est donc
pas le taux mais le prix des quotas — d'où l'obligation de passer par la colonne
`Taux de taxation` de la dimension `Instruments` pour ces régimes-là, jamais par le
tarif effectif total.

### Tier 2 — `Instruments` (décomposition) — **plus solide que prévu**

C'est finalement le pivot du dispositif, pas un repli. Trois résultats vérifiés.

**a) L'identité comptable est exacte.** Sur les 759 lignes des onze tableaux
`Instruments` du périmètre carbone :

    tarification effective = taux de taxation + boucliers et aides + prix des quotas ETS

759/759 lignes justes, écart maximal 1,1 · 10⁻¹³ — du bruit de flottant, rien
d'autre. Deux pièges de lecture : `Boucliers et aides` est **déjà porté en négatif**
(l'identité est additive, pas soustractive), et `Composante carbone` n'entre **pas**
dans l'identité — c'est un montant reporté à titre indicatif, qui peut d'ailleurs
excéder le taux de taxation net.

**b) La décomposition se raccroche aux régimes.** Le tableau `Instruments` ne porte
aucun libellé de régime : 75 lignes contre 121 côté `Régime fiscal`, car il regroupe
les cellules partageant une même décomposition. L'appariement sur le couple
(tarif, quantité) ne rend que 40 %. Mais **l'appariement sur le seul tarif effectif
rend 100 %**, et sans ambiguïté : vérifié sur 2022 et 2023, chaque palier tarifaire
renvoie à une décomposition et une seule. La jointure est donc sûre.

**c) Conséquence.** On sait isoler la part accise **pour tout régime**, y compris
ceux exposés à l'ETS — les six régimes charbon/gaz à 25 paliers cessent d'être un
angle mort. Le Tier 2 englobe le Tier 1 plutôt qu'il ne le complète, et la seule
chose qui reste bloquante est la conversion d'unités (§4), plus les facteurs
d'émission si l'on veut exploiter le périmètre carbone.

**d) Confirmé sur les deux périmètres.** L'identité et la jointure ont été rejouées
sur `Energie × Instruments` : **708/708 lignes exactes**, et jointure sur le tarif à
**100 %** sans ambiguïté (2022 et 2023). Seule différence de structure : côté
énergie il n'y a pas de colonne `Montant remboursement indirect ETS` — sept colonnes
au lieu de neuf. Le Tier 2 est donc acquis des deux côtés.

### Tier 3 — périmètre `Carbone` : **pas un test, une réconciliation**

Arbitré : on veut un jeu de facteurs d'émission, mais **fixé indépendamment**. Les
facteurs du CGDD ne sont pas la référence ; ils sont l'un des termes qui expliquent
l'écart entre notre modèle et le leur.

Cela change complètement le statut de la moitié carbone du fichier, et il faut être
strict là-dessus.

**a) Nos facteurs sont à créer, et de zéro.** Vérifié : aucun facteur d'émission
n'existe nulle part — ni dans baremes-ipp-yaml, ni dans les deux dépôts openfisca.
Le seul objet approchant est `reforms/taxe_carbone.py` d'OFFIT, qui est une réforme
contrefactuelle, pas un jeu de contenus carbone. À sourcer indépendamment (Base
Carbone de l'ADEME, CITEPA, ou les contenus retenus pour la construction de la
composante carbone en LF 2014), et à porter dans l'arbre de paramètres normal, avec
ses propres références.

**b) Les facteurs du CGDD sont un actif de comparaison, jamais un paramètre — et ils
se lisent dans les quantités, pas dans les tarifs.**

C'est le résultat le plus net du chantier, et il simplifie tout. Inutile de passer
par un rapport de tarifs : les quantités carbone sont en MtCO2, les quantités
énergie en TWh, et

    MtCO2 / TWh  =  tCO2 / MWh

exactement. Le facteur d'émission implicite du CGDD s'obtient donc, pour chaque
régime et chaque année, en divisant simplement la quantité du tableau carbone par
celle du tableau énergie. Aucune dépendance à la décomposition des instruments,
donc aucune pollution par l'ETS ou les boucliers, et **ça marche aussi pour les
régimes à tarif nul** — que le rapport de tarifs laissait indéterminés.

Résultat mesuré sur les 42 régimes communs aux deux périmètres, 2017-2024 :

| stabilité du facteur | régimes | lecture |
|---|---|---|
| cv = 0,0000 (constant au bit près) | 14 | contenu carbone physique pur |
| cv < 0,5 % | 27 au total | quasi-constant |
| cv ≥ 0,5 % | 15 | effet de structure |

Les valeurs constantes sont physiquement reconnaissables : fioul lourd 0,2808,
kérosène 0,2639, GPL 0,1908, autres produits pétroliers 0,2974 tCO2/MWh.

**Et les régimes qui dérivent sont exactement ceux qu'on attendait** : essence
(0,30 %), gazole routier (0,36 %), E10 (0,47 %) — les carburants **incorporant des
biocarburants**, dont le taux d'incorporation monte d'année en année. Ce n'est pas
du bruit, c'est un effet de composition réel, et il est identifié.

Fichier : `assets/elfe/facteurs_emission_cgdd.csv`, **hors de l'arbre de
paramètres**, avec mention explicite qu'il s'agit d'une série externe.

**c) Conséquence sur la CI, et c'est le point important.** Aucun test en €/tCO2 ne
doit entrer en intégration continue. Un écart en €/tCO2 peut venir du taux d'accise
*ou* du facteur d'émission, et notre facteur est légitimement différent du leur —
un échec ne serait donc pas un bug. Mettre ces tests en CI reviendrait à ériger les
facteurs du CGDD en vérité, ce qui est exactement ce qu'on ne veut pas.

La règle qui en découle :

> **CI = €/MWh uniquement** (Tier 1 et 2). Ça teste le droit, c'est strict, ça casse
> si le modèle se trompe.
> **€/tCO2 = rapport d'audit hors CI.** Ça explique un écart, ça ne juge personne.

### Tier 3 bis — décomposition de l'écart entre les deux modèles

C'est le livrable que la décision du §Tier 3 rend possible, et il est plus
intéressant qu'un test.

Le tarif effectif carbone d'un régime est un quotient :

    T_carbone = T_energie / F        (F = facteur d'émission, tCO2/MWh)

L'écart entre notre modèle et Elfe se décompose donc **exactement** et de façon
additive en logarithmes :

    log T_c^nous − log T_c^elfe  =  [ log T_e^nous − log T_e^elfe ]   ← composante « droit »
                                  − [ log F^nous  − log F^elfe  ]   ← composante « facteur »

Deux termes, deux natures. Le premier est un désaccord sur le **droit** : taux
d'accise, exonération, modulation — il est arbitrable contre le texte, et c'est
précisément ce que les tests Tier 1/2 verrouillent par ailleurs. Le second est un
désaccord sur la **physique** : contenu carbone du produit — il n'est pas
arbitrable contre le droit, il relève du choix de source, et il est légitime qu'il
subsiste.

Sortie attendue : un tableau régime × année à quatre colonnes (écart total, part
droit, part facteur, quantité), trié par contribution à l'écart agrégé. C'est ce qui
permet de dire « notre tarification effective diffère de X €/tCO2 de celle du CGDD,
dont Y points de droit et Z points de facteur d'émission » — une phrase qu'on ne
peut pas écrire aujourd'hui.

Script : `scripts/elfe/audit_ecarts.py`, hors CI.

**Contrôle préalable — fait, et il conditionne la lecture.** La question était de
savoir si le F implicite du CGDD est stable à régime donné. Réponse mesurée (cf.
Tier 3 b) : constant au bit près pour 14 régimes, sous 0,5 % de coefficient de
variation pour 27 sur 42, et les dérives résiduelles sont concentrées sur les
carburants incorporant des biocarburants.

Conséquence directe sur la décomposition : pour les régimes à F constant, le terme
« facteur » est un vrai désaccord de contenu carbone, et se lit tel quel. Pour
l'essence, le gazole routier et l'E10, il mélange le désaccord de contenu et
l'**effet d'incorporation** des biocarburants. Sur ces trois régimes — qui pèsent
lourd en volume — il faut donc soit neutraliser l'incorporation, soit présenter le
terme « facteur » comme composite et le dire. À trancher au moment d'écrire
`audit_ecarts.py`, et à documenter dans `SOURCES.md`.

### Tier 4 — identités et couverture (pas de modèle en jeu)

Reprend la section « identités comptables » d'`AGREGATS_TIC.md` :

- la quantité totale doit être identique entre les six dimensions, pour un même
  couple (périmètre, millésime) — contrôle d'intégrité de l'extraction.
  **Déjà vérifié** sur le périmètre carbone : les cinq dimensions donnent le même
  total, au centième, sur les onze millésimes (475,98 MtCO2 en 2014 … 400,22 en
  2023). L'extraction est donc fidèle, et ce contrôle a vocation à rester dans la
  CI comme garde-fou de la donnée ;
- l'ensemble des paliers distincts d'un régime doit **coïncider avec l'ensemble**
  des taux du barème pour ce régime (égalité d'ensembles, pas comparaison point à
  point). C'est le test fort sur les modulations régionales, et il ne dépend
  d'aucune variable du modèle — seulement du barème.

---

## 4. Le point dur : les moyennes annuelles

Elfe publie des tarifs **agrégés sur l'année**. Quand un taux change en cours
d'année, le palier Elfe est une moyenne pondérée par les consommations, pas une
valeur de barème.

C'est exactement le constat n° 6 d'`AGREGATS_TIC.md` (le pas du 1er février sur
l'électricité, lu au 1er janvier), mais aggravé : là où la déclaration 2040-TIC
donnait deux cases distinctes, Elfe donne un seul nombre intermédiaire, non
inversible sans connaître la pondération infra-annuelle.

Conduite à tenir, à arbitrer :

- **par défaut**, n'émettre en test que les régimes dont le taux est constant sur
  l'année (détectable : le palier tombe exactement sur une valeur du barème) ;
- consigner les autres dans le rapport d'audit comme « moyenne infra-annuelle,
  non testable en l'état », plutôt que de les figer en attendus ;
- ne pas chercher à modéliser la pondération : on introduirait une hypothèse qui
  n'est pas dans le barème.

Second point dur, plus tractable : la **conversion d'unités** (question ouverte n° 1
du §1). Elfe affiche des €/MWh, le barème porte des €/hL ou €/100 kg pour les
produits pétroliers. Le rapport `tarif Elfe ÷ tarif barème`, calculé régime par
régime sur les régimes à taux stable, restitue le PCI implicite retenu par le CGDD.

C'est un livrable à part entière, et sans doute le premier à produire : il existe
déjà une branche `param/taux_conversion_euro_par_mwh_a_euro_par_hectolitre` sur
openfisca-france-indirect-taxation, que ces données permettent de **confronter à une
source externe publique**. Ce gain-là ne dépend d'aucune des fusions du §6 — c'est
le seul morceau du chantier qui peut démarrer tout de suite.

Tant que ce rapport n'est pas établi, aucun test Tier 1 n'est écrivable : on ne sait
pas dans quelle unité comparer.

---

## 5. Familles de tests générées

Sur le modèle d'`agregats/`, jamais éditées à la main :

    openfisca_france_entreprises/tests/taxes/taxes_energies/elfe/
      test_regimes_energie.yaml       1 MWh → accise = tarif Elfe (Tier 1)
      test_exonerations_elfe.yaml     régimes à 0 €/MWh → accise nulle
      test_modulations_regionales.yaml  égalité d'ensembles des paliers (Tier 4)

Règle reprise telle quelle : **une cellule dont le tarif ne concorde pas avec le
barème n'est pas émise en test**. Elle part au rapport d'audit. Figer le désaccord
en attendu le rendrait invisible ; le laisser en échec casserait la CI.

---

## 6. Séquencement — ce qu'il faut fusionner d'abord

Tu l'as dit, le calculateur n'est pas prêt. Dans l'ordre :

1. **Les branches energies** — `align/energies-tree`,
   `refactor/energies-periodes-mensuelles`, `energies_migration` (OFFIT).
   Tant que l'arbre des paramètres bouge, `correspondance.py` est intenable.
2. **`fix/regions-post-2016`** — prérequis dur du Tier 4 : sans la grille régionale,
   les quatre paliers du gazole n'ont rien à quoi se comparer.
3. **Les arbitrages 1 à 7 d'`AGREGATS_TIC.md`**, en particulier le n° 6 (pas du
   1er février) : il conditionne le §4 ci-dessus.
4. **Facteurs d'émission** (Tier 3) — arbitré : on les veut, fixés indépendamment.
   Ce chantier est désormais **parallèle**, pas séquentiel : nos facteurs se
   sourcent (ADEME / CITEPA / LF 2014) sans rien attendre de l'arbre des accises,
   et l'extraction des facteurs implicites du CGDD ne dépend que de la donnée déjà
   en main. Il peut démarrer en même temps que le point 1.

### Ce qui peut démarrer tout de suite

Deux chantiers ne dépendent d'aucune fusion :

- la **calibration des unités** (§4) — et elle est bloquante pour tout le reste, donc
  c'est la première chose à faire ;
- les **facteurs d'émission**, dans les deux sens : constituer les nôtres, et
  extraire ceux du CGDD depuis `assets/`.

Tout le reste — `correspondance.py`, les tests générés, la décomposition d'écarts —
attend les points 1 à 3.

Ce n'est qu'ensuite que `correspondance.py` — la table de ~100 régimes Elfe vers
les variables — vaut la peine d'être écrite : c'est le gros du travail, et il est
entièrement dépendant de l'arbre de paramètres final.

---

## 7. Ce qui est déjà fait

- Client Shiny fonctionnel et moissonnage des 114 combinaisons (`.xlsx` bruts).
- Confirmation que la donnée porte bien le signal recherché (paliers régionaux).
- Confirmation que le périmètre carbone est bloqué faute de facteurs d'émission.

Reste à faire avant d'ouvrir la branche : consolidation en CSV long, `SOURCES.md`,
et la table de correspondance — cette dernière après les fusions du §6.
