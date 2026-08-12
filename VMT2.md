# Voies et moyens tome II : les dépenses fiscales, PLF 2001 à 2026

État au 2026-08-12. Branche `assets/vmt2-depenses-fiscales`, partant de `main`.

Troisième jeu de données réelles adossé au modèle, après les agrégats 2040-TIC
(`assets/agregats-tic`) et la comparaison au modèle Elfe (`assets/elfe-cgdd`).
Il apporte ce que les deux autres ne donnent pas : le **coût budgétaire officiel
de chaque régime dérogatoire**, exonération par exonération et tarif réduit par
tarif réduit, sur vingt-six millésimes — soit les années fiscales 1999 à 2026.

## La source

L'annexe *Voies et moyens tome II* au projet de loi de finances recense chaque
année l'ensemble des dépenses fiscales et les chiffre. Les PDF sont lus en
**lecture seule** dans le fonds documentaire IPP, sous
`Z:/2-Documentation/Finances publiques/LF/` ; leur chemin exact par millésime
est dans `scripts/vmt2/commun.py` (`SOURCES`). Rien n'y est jamais écrit.

Il n'existe pas de version en données ouvertes exploitable : le seul jeu publié
([PLF 2023 sur data.economie.gouv.fr](https://data.economie.gouv.fr/explore/dataset/plf2023_voies_et_moyens_t2_liste_des_depenses_fiscales/))
renvoie `total_count: 0` et sa ressource CSV pèse 109 octets. Le PDF est la source.

Le corpus couvre le PLF 2001 au PLF 2026 sans trou, **sauf le PLF 2000**, dont
seul le tome 1 figure au fonds. Trois mises en page se succèdent, une par
parseur : régime A (2001-2008, numéros espacés « 80 01 01 »), régime B
(2009-2019, lignes de tableau) et régime C (2020-2026, fiches encadrées).

L'annexe par mission est lue selon deux extractions concurrentes, `-layout` et
`-raw`, la mieux chiffrée l'emportant : au PLF 2026 la première débite le tableau
en colonnes verticales désynchronisées, où le numéro d'une mesure voisine le
libellé d'une autre et le montant d'une troisième.

## Quatre pièges, à connaître avant d'utiliser la table

**1. Chaque document porte trois années, et les révise.** Un tome II donne la
réalisation N-2, la prévision N-1 et la prévision N. La même année fiscale est
donc décrite par trois millésimes successifs, et l'écart est loin d'être
cosmétique : le tarif réduit du gazole non routier (800201) pour 2021 est prévu
à 600 M€ au PLF 2021 et réalisé à 1 115 M€ au PLF 2023, soit +86 %.

La clé de la table est donc le triplet `(numero, annee, plf)`. **Pour construire
une série, filtrer `statut == 'realisation'`** ; les deux autres statuts mesurent
l'incertitude de prévision, pas le coût.

**2. Les identifiants bougent, et parfois éclatent.** La revue des taxes
intérieures de consommation de 2020 a renuméroté sept dépenses énergie
(800103→800220, 800114→840101, 800219→830203, …) et surtout **éclaté** quatre
d'entre elles, la 800210 devenant 800210 + 830201 + 840201. D'où la chute
apparente de 903 M€ à 8 M€ sur la 800210 entre le PLF 2020 et le PLF 2021 : ce
n'est pas une révision, c'est le gaz et les charbons qui en sont sortis.
`assets/vmt2/crosswalk.csv` porte ces mouvements ; ne pas chaîner une série
énergie à travers 2021 sans le consulter.

**3. Le PLF 2001 chiffre en millions de francs.** Tous les millésimes suivants
sont en millions d'euros. La colonne `unite` le dit pour chaque ligne, `montant`
reprend la valeur telle qu'imprimée, et `montant_meur` porte la conversion à la
parité irrévocable de 6,55957 F pour 1 €. La conversion est exacte au sens
juridique mais transforme un entier en décimal : les 1 400 MF de la 800101 en
1999 valent 213,4 M€. **Toujours agréger sur `montant_meur`, jamais sur
`montant`.**

**4. Toutes les fiches ne sont pas des dépenses fiscales.** De 2010 à 2019, le
document imprime après les chapitres une annexe « mesures considérées comme des
modalités de calcul de l'impôt » : mêmes fiches, mêmes chiffrages, mais mesures
déclassées, hors périmètre et hors totaux publiés. Les confondre gonfle l'impôt
sur les sociétés 2008 de 12,5 Md€ à cause de la seule 320103. La colonne
`perimetre` les distingue ; **filtrer sur `depense_fiscale`** sauf raison
contraire — les 38 à 45 mesures déclassées par millésime restent utiles, la
800115 (exonération pour l'extraction et la production de gaz naturel) est de
celles-là.

## Ce que produit l'extraction

    assets/vmt2/chiffrages.csv               37 182 lignes : (plf, numero, annee)
    assets/vmt2/fiches.csv                   12 394 lignes : (plf, numero)
    assets/vmt2/crosswalk.csv                mouvements d'identifiants déclarés
    assets/vmt2/mouvements.csv               entrées/sorties, expliquées ou non
    assets/vmt2/controle_cout_par_impot.csv  somme extraite vs total publié
    assets/vmt2/revisions.csv                prévision initiale vs réalisation
    assets/vmt2/mesures_sans_fiche.csv       mesures listées en annexe sans fiche

Les deux premières tables se joignent sur `(plf, numero)` : une fiche porte
trois chiffrages, et répéter ses métadonnées sur chacun quintuplerait le volume
versionné pour la même information.

`chiffrages.csv` porte le montant en M€ (`montant`), son statut de chiffrage
(`chiffrage` : `chiffre`, `nc` pour non chiffrable, `epsilon` pour moins de
0,5 M€, `sans_objet` pour un tiret, `absent` pour une cellule vide) et la valeur
brute telle qu'imprimée (`montant_brut`). `fiches.csv` porte les métadonnées :
`libelle`, `finalite`, `mission`, `beneficiaires`, `methode` (méthode de
chiffrage), **`fiabilite`** (qualité du chiffrage déclarée par la DLF),
`norme` (norme fiscale de référence), `reference` (fondement juridique),
`creation`, `modification`, `fin_fait_generateur`, `fin_incidence`,
`observations` et `nombre_beneficiaires` (ces deux-là propres au régime A).

La `fiabilite` est renseignée sur 8 436 des 11 988 couples (millésime, dépense
fiscale) : 3 608 « ordre de grandeur », 2 345 « Très bonne », 1 914 « Bonne »,
plus 568 fiches du régime A qui écrivent « bon » et « très bon » au masculin.
Le vocabulaire n'est pas harmonisé ici : c'est celui du document. Sur l'accise
sur les énergies au PLF 2025, 28 des 39 dépenses sont « Bonne » ou « Très bonne ».
`changement_methode` signale les fiches où le document prévient d'un changement
de méthode de chiffrage — donc les ruptures de série imputables à la mesure du
coût plutôt qu'à l'évolution du dispositif.

## Comment c'est vérifié

L'exhaustivité n'est pas supposée : elle est comptée indépendamment du parseur,
puis les valeurs sont confrontées à une seconde source.

| Contrôle | Portée | Résultat |
|---|---|---|
| Nombre de fiches = nombre d'ancres du document | 2001-2026 | 26/26 millésimes, 0 anomalie de structure |
| Nombre de dépenses = décompte annoncé en introduction | 2001-2005 | **5/5** millésimes exacts |
| Montant de la fiche = montant de l'annexe mission-programme | 2022-2026 | **2 342/2 342** concordants |
| Somme par impôt = total publié en sous-partie II | 2009-2026 | **82/82** postes-années exacts à l'euro sur l'année de réalisation |

Le deuxième contrôle est extérieur au parseur : les tomes de 2001 à 2005 écrivent
en toutes lettres « Le présent fascicule recense 452 dépenses fiscales », et les
cinq comptes tombent juste (408, 414, 418, 422, 452). Les millésimes suivants ont
cessé de publier le chiffre. Le décompte du PLF 2015 ressort quant à lui à 453,
chiffre publié par la DLF pour ce millésime.

Le quatrième contrôle **n'est pas exact et ne doit jamais être présenté comme
tel** hors de l'année de réalisation : les mesures `nc` entrent dans le total
publié sans valeur sommable, les `ε` sont comptées 0, et le nombre de `nc`
augmente mécaniquement sur les années de prévision. Sur l'année de réalisation,
en revanche, l'accord est total — 82 postes-années sur 82, à l'euro.

Ces deux derniers contrôles ne sont pas décoratifs : c'est le recoupement par
l'annexe du PLF 2026 qui a révélé que l'appariement des montants aux années
échouait quand la grille serre les années à gauche et étale les montants. Huit
fiches de 2026 y perdaient une colonne, et trois postes-années de 2021 en
sortaient faux. Les montants sont désormais appariés **par ordre de lecture**
quand il y a autant de valeurs que d'années, la proximité de colonne n'étant
gardée que pour les grilles à cellule vide.

Le suivi des identifiants s'appuie uniquement sur ce que le document publie
(renumérotations, classements, déclassements, créations, suppressions) plus les
éclatements de 2021, transcrits en constante sourcée dans
`scripts/vmt2/crosswalk.py`. **Aucun appariement n'est déduit d'une ressemblance
de libellé.** Les entrées et sorties qu'aucune table ne justifie sont écrites
`inexplique` dans `mouvements.csv` pour arbitrage humain. Sur la transition
critique 2020→2021 en énergie, 26 des 28 mouvements sont expliqués ; restent la
sortie de la 800108 et celle de la 800217.

Le PLF 2026 en ajoute quatre, et ils tombent en plein dans le périmètre modélisé
par OFF-E : l'entrée de la `820210` est expliquée par une création, mais les
sorties des `800210`, `800211` et `840202` — les tarifs réduits pour les
installations grandes consommatrices d'énergie, ETS et fuite de carbone — ne le
sont par aucune table. À élucider avant de chaîner une série sur ces trois
mesures.

La couverture dépend entièrement de ce que le document publie :

| Régime | Mouvements expliqués |
|---|---|
| A, 2002-2008 | **0 / 391** |
| B, 2009-2019 | 228 / 457 |
| C, 2020-2026 | 127 / 285 |

Le zéro du régime A n'est pas un défaut d'extraction : la sous-partie
« Évolution depuis le précédent PLF » n'apparaît qu'au PLF 2009, et avant elle
aucune table ne décrit les entrées et sorties. Le piège est que le mot
« Création » figure bien dans ces documents — comme **catégorie d'objectifs**
(« Encourager la création »), suivie de dépenses qui n'ont rien de nouvelles.
Les lire comme des créations fabriquerait des liens que le document n'affirme
pas ; le parseur s'en abstient explicitement. **Une série qui traverse 2001-2008
doit donc être vérifiée à la main sur les identifiants.**

## Utilisation

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m scripts.vmt2.cli extraire
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m scripts.vmt2.cli crosswalk

Sans argument, les deux commandes couvrent tout le corpus ; `--de` et `--a` ne
servent qu'à le restreindre.

**`PYTHONIOENCODING=utf-8` n'est pas facultatif sous Windows.** La console est en
`cp1252`, et le seul affichage d'un montant « ε » fait tomber la commande en
`UnicodeEncodeError` — après tout le travail et avant l'écriture des fichiers. La
même précaution vaut pour la suite de tests du dépôt, avec `PYTHONUTF8=1`.

Le texte des PDF est extrait par `pdftotext` et mis en cache dans `.cache/vmt2/`
(gitignoré), reconstruit seulement s'il manque — en deux versions, `-layout` pour
les fiches et `-raw` pour l'annexe. `pdftotext` (poppler, fourni par MiKTeX sur
le poste de travail) est donc requis pour un premier passage ; ensuite le cache
suffit.

## Pour la suite

Le tome II du PLF 2000 reste introuvable, et le trou est probablement à la
source. L'ancien fonds performance-publique survit sur budget.gouv.fr sous
`/sites/performance_publique/files/farandole/ressources/archives/<année>/index-d.htm`,
remontant à 1996 — mais ces pages ne portent pas les Voies et moyens, qui sont un
« bleu budgétaire » et ne s'atteignent que par un lien vers un hôte aujourd'hui
mort (`www4.minefi.gouv.fr/budget/plf2001/sommaire.htm` pour 2001,
`www.minefi.gouv.fr/budget/Bleus/` pour 2000). C'est cette page qui listait les
`vm12001.pdf` / `vm22001.pdf` dont le fonds IPP porte la copie.

Un indice concordant : les onze fichiers `vm*` du fonds ont tous été récupérés
dans le même lot, le 1er décembre 2024 à 12:10:55, et `vm22000.pdf` est le seul
manquant alors que `vm12000.pdf` est là. Le téléchargement d'alors a buté sur le
même mur.

Pour trancher, il faut interroger la Wayback Machine sur
`minefi.gouv.fr/budget/Bleus/` autour de 1999-2001, ou lancer une requête CDX sur
`minefi.gouv.fr*` filtrée sur `vm2*.pdf`. À défaut, l'Assemblée nationale
(PLF 2000 = document n° 1805 et ses annexes) et le dossier législatif
`senat.fr/dossier-legislatif/pjlf2000.html` sont les deux autres pistes.

Reste à trancher la forme des tests OFF-E. Une dépense fiscale est un
**contrefactuel** — la recette perdue par rapport à la norme fiscale de
référence, explicitée dans chaque fiche (colonne `norme`) — et non une recette
observée. La confronter au modèle suppose de simuler deux fois, au tarif
dérogatoire puis au tarif de référence, et de comparer l'écart : ce n'est pas la
mécanique des tests 2040-TIC, où l'agrégat est directement le montant dû.

Un signal utile pour commencer, sur le bouclier tarifaire : entre la prévision
et le réalisé 2022, la 820201 passe de 250 à 56 M€, la 820203 de 1 245 à 314 et
la 820204 de 230 à 21. L'accise ramenée au minimum européen écrase mécaniquement
la valeur des tarifs réduits ; un modèle qui reproduit ces trois effondrements
sur la bonne année est fortement contraint.
