"""Exploitation des agrégats de la déclaration 2040-TIC.

Le fichier `assets/agregats.csv` agrège, à l'année et sur l'ensemble des
redevables, les cases de la déclaration 2040-TIC déposée par les fournisseurs
d'énergie. Chaque case correspond à une cellule tarifaire homogène : un couple
(produit, régime, tarif). Comme l'accise est linéaire à l'intérieur d'une
cellule, le rapport `montant / quantité` d'une case restitue exactement le tarif
légal, et l'agrégat est un cas de test valide pour le modèle.

Modules :

- `donnees`        : lecture du CSV, appariement quantité/montant, tarifs implicites
- `correspondance` : table de correspondance cases 2040-TIC → variables du modèle
- `audit`          : confrontation des tarifs implicites au barème (CLI)
- `generer_tests`  : génération des tests YAML OpenFisca (CLI)
"""
