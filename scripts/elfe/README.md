# Outillage d'extraction Elfe

Reconstitue `assets/elfe/` depuis l'application de visualisation du CGDD.
Voir [`../../ELFE.md`](../../ELFE.md) pour le plan d'ensemble et
[`../../assets/elfe/SOURCES.md`](../../assets/elfe/SOURCES.md) pour la source.

## Enchaînement

    python scripts/elfe/harvest.py       # 106 .xlsx  (~45 min, réseau)
    python scripts/elfe/consolidate.py   # -> elfe.csv, elfe_instruments.csv
    python scripts/elfe/facteurs.py      # -> facteurs_emission_cgdd.csv

Dépendances : `requests`, `websocket-client`, `pandas`, `openpyxl`.

## ⚠️ Chemins à reprendre

Ces scripts ont été écrits contre une arborescence de travail temporaire, pas
contre celle du dépôt. Ils résolvent leurs chemins relativement à leur propre
emplacement (`os.path.dirname(__file__)`) et écrivent dans `elfe_raw/` et
`elfe_consolide/` **à côté d'eux-mêmes**, au lieu de `assets/elfe/`.

À reprendre avant tout usage : faire pointer les sorties sur `assets/elfe/` et
les `.xlsx` bruts sur un répertoire ignoré par git. Rien d'autre n'est à changer —
la logique d'extraction est fonctionnelle et a produit les fichiers versionnés.

## Notes de protocole

`shiny_client.py` parle le protocole Shiny en websocket. Deux points non
évidents, trouvés à l'usage :

- l'endpoint `/_w_<worker>/__sockjs__/n=1/<srv>/<sess>/websocket` rend des trames
  **JSON brutes**, sans encapsulation SockJS : on envoie `{"method":"init",...}`
  directement, pas un tableau de chaînes ;
- le `downloadHandler` renvoie **500** tant que le graphique n'a pas été rendu.
  Il faut fournir les `.clientdata_output_graphique_*` puis attendre l'arrivée de
  la valeur `graphique` avant de tirer le fichier — c'est ce que fait
  `wait_for_graph()`.

Les combinaisons `Energie` avant 2017 et `Energie × Gaz à effet de serre`
renvoient un 500 permanent : elles n'existent pas, l'échec est normal.
