# Voies et moyens tome II : les dépenses fiscales, PLF 2009 à 2025

État au 2026-08-12. Branche `assets/vmt2-depenses-fiscales`, partant de `main`.

Troisième jeu de données réelles adossé au modèle, après les agrégats 2040-TIC
(`assets/agregats-tic`) et la comparaison au modèle Elfe (`assets/elfe-cgdd`).
Il apporte ce que les deux autres ne donnent pas : le **coût budgétaire officiel
de chaque régime dérogatoire**, exonération par exonération et tarif réduit par
tarif réduit, sur dix-sept millésimes.

## La source

L'annexe *Voies et moyens tome II* au projet de loi de finances recense chaque
année l'ensemble des dépenses fiscales et les chiffre. Les PDF sont lus en
**lecture seule** dans le fonds documentaire IPP, sous
`Z:/2-Documentation/Finances publiques/LF/` ; leur chemin exact par millésime
est dans `scripts/vmt2/commun.py` (`SOURCES`). Rien n'y est jamais écrit.

Il n'existe pas de version en données ouvertes exploitable : le seul jeu publié
([PLF 2023 sur data.economie.gouv.fr](https://data.economie.gouv.fr/explore/dataset/plf2023_voies_et_moyens_t2_liste_des_depenses_fiscales/))
renvoie `total_count: 0` et sa ressource CSV pèse 109 octets. Le PDF est la source.

Le fonds contient aussi les millésimes 2001 à 2008. Ils ne sont pas traités ici :
leur mise en page est différente (numéros espacés « 80 01 01 », colonnes
« Résultat estimé / Evaluation ») et aucune table de renumérotation n'y figure,
ce qui rendrait tout suivi d'identifiant empirique. À décider séparément.

## Trois pièges, à connaître avant d'utiliser la table

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

**3. Toutes les fiches ne sont pas des dépenses fiscales.** De 2010 à 2019, le
document imprime après les chapitres une annexe « mesures considérées comme des
modalités de calcul de l'impôt » : mêmes fiches, mêmes chiffrages, mais mesures
déclassées, hors périmètre et hors totaux publiés. Les confondre gonfle l'impôt
sur les sociétés 2008 de 12,5 Md€ à cause de la seule 320103. La colonne
`perimetre` les distingue ; **filtrer sur `depense_fiscale`** sauf raison
contraire — les 38 à 45 mesures déclassées par millésime restent utiles, la
800115 (exonération pour l'extraction et la production de gaz naturel) est de
celles-là.

## Ce que produit l'extraction

    assets/vmt2/chiffrages.csv               25 206 lignes : (plf, numero, annee)
    assets/vmt2/fiches.csv                    8 402 lignes : (plf, numero)
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
`creation`, `modification`, `fin_fait_generateur`, `fin_incidence`.

La `fiabilite` est renseignée sur 6 931 des 7 996 couples (millésime, dépense) :
2 940 « Ordre de grandeur », 2 157 « Très bonne », 1 834 « Bonne ». Sur l'accise
sur les énergies au PLF 2025, 28 des 39 dépenses sont « Bonne » ou « Très bonne ».
`changement_methode` signale les fiches où le document prévient d'un changement
de méthode de chiffrage — donc les ruptures de série imputables à la mesure du
coût plutôt qu'à l'évolution du dispositif.

## Comment c'est vérifié

L'exhaustivité n'est pas supposée : elle est comptée indépendamment du parseur,
puis les valeurs sont confrontées à une seconde source.

| Contrôle | Portée | Résultat |
|---|---|---|
| Nombre de fiches = nombre d'ancres du document | 2009-2025 | 17/17 millésimes, 0 anomalie de structure |
| Montant de la fiche = montant de l'annexe mission-programme | 2022-2025 | 1 877/1 877 concordants |
| Somme par impôt = total publié en sous-partie II | 2009-2025 | **75/78** postes-années exacts à l'euro sur l'année de réalisation |

Le décompte des dépenses fiscales du PLF 2015 ressort à 453, chiffre publié par
la DLF pour ce millésime.

Le troisième contrôle **n'est pas exact et ne doit jamais être présenté comme
tel** hors de l'année de réalisation : les mesures `nc` entrent dans le total
publié sans valeur sommable, les `ε` sont comptées 0, et le nombre de `nc`
augmente mécaniquement sur les années de prévision. Le résultat le dit
clairement : 75/78 exacts sur la réalisation, 27/78 sur la prévision N-1,
20/78 sur la prévision N. Les trois écarts résiduels sur l'année de réalisation
sont tous au PLF 2021 (IS +761 M€, TVA +21 M€, TICC +1 M€) et restent à
élucider.

Le suivi des identifiants s'appuie uniquement sur ce que le document publie
(renumérotations, classements, déclassements, créations, suppressions) plus les
éclatements de 2021, transcrits en constante sourcée dans
`scripts/vmt2/crosswalk.py`. **Aucun appariement n'est déduit d'une ressemblance
de libellé.** Les entrées et sorties qu'aucune table ne justifie sont écrites
`inexplique` dans `mouvements.csv` pour arbitrage humain : 307 mouvements
expliqués sur 617. Sur la transition critique 2020→2021 en énergie, 26 des 28
mouvements sont expliqués ; restent la sortie de la 800108 et celle de la 800217.

## Utilisation

    .venv/Scripts/python.exe -m scripts.vmt2.cli extraire --de 2009 --a 2025
    .venv/Scripts/python.exe -m scripts.vmt2.cli crosswalk

Le texte des PDF est extrait par `pdftotext -layout` et mis en cache dans
`.cache/vmt2/` (gitignoré), reconstruit seulement s'il manque. `pdftotext`
(poppler, fourni par MiKTeX sur le poste de travail) est donc requis pour un
premier passage ; ensuite le cache suffit.

## Pour la suite

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
