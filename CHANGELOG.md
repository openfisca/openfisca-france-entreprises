## 2.0.0 - [#32](https://github.com/openfisca/openfisca-france-entreprises/pull/32)

* Breaking change.
* Impacted periods: from 01/01/1986.
* Impacted areas:
  - `variables/consommation_energie/autres_produits`
  - `variables/consommation_energie/charbon`
  - `variables/consommation_energie/electricite`
  - `variables/consommation_energie/energies`
  - `variables/consommation_energie/gaz_naturel`
  - `variables/taxes/formula_helpers`
  - `variables/taxes/taxation_energies/taxation_autres_produits_energetiques`
  - `variables/taxes/taxation_energies/taxation_charbon`
  - `variables/taxes/taxation_energies/taxation_electricite`
  - `variables/taxes/taxation_energies/taxation_gaz_naturel`
  - `variables/taxes/taxation_energies/taxation_tiruert`
  - `variables/taxes/taxation_energies/tccfe/tccfe`
  - `variables/taxes/taxation_energies/tdcfe/tdcfe`
  - `variables/boulier_tarifaire`
  - `variables/variables_economiques`
* Details:
  - Les 106 variables de quantite d'energie -- consommations et assiettes -- passent de
    `definition_period = YEAR` a `MONTH`, avec `set_input = set_input_divide_by_period`. La taxe
    de l'annee devient la somme des taxes mensuelles : chaque mois porte sa quantite et son tarif.
  - **Rupture d'API** : lire `assiette_ticc`, `assiette_ticgn`, `assiette_taxe_electricite` ou
    l'une des consommations sur une periode annuelle leve desormais une exception. Utiliser
    `options=[ADD]`, ou interroger un mois.
  - Le comportement anterieur est preserve pour qui fournit des quantites annuelles :
    `set_input_divide_by_period` les repartit sur les douze mois, et la somme redonne
    `quantite * moyenne des tarifs`, soit exactement la valeur d'avant la bascule. C'est ce dont
    les agregats Elfe ont besoin, eux qui publient des tarifs deja moyennes.
  - Motif abandonne : l'hypothese de consommation uniforme sur l'annee, que portait
    `tarif_moyen_annuel`. Les declarations 2040-TIC la contredisent -- elles ne moyennent jamais,
    elles segregent les tarifs en cases distinctes, chaque case portant la quantite taxee a son
    propre tarif. Voir le constat 8 d'`AGREGATS_TIC.md`.
  - Trois regimes restent volontairement annuels, leurs bornes mordant sur le cumul de l'annee et
    non sur chaque mois : le seuil d'exoneration et l'abattement de la TICGN d'avant 2008, le
    plafond de 1 GWh du tarif reduit des centres de stockage de donnees, et le bouclier tarifaire,
    qui encode un basculement de regime et non un changement de tarif.
  - TCCFE et TDCFE restent annuelles : leur coefficient communal ou departemental n'est pas
    mensualise. La TCCFE est de toute facon incorporee a l'accise au 01/01/2023.
  - Correction de fond : neuf formules de la TICPE renvoyaient une liste d'un seul element, ce qui
    faisait stocker a OpenFisca un tableau de forme (1, n) au lieu de (n,). Invisible avec un seul
    etablissement, faux avec plusieurs.
  - `tarif_moyen_annuel` cede la place a `accise_annuelle` et `tarif_du_mois`. Il ne subsiste que
    pour le regime a seuil de la TICGN d'avant 2008, ou il calcule vraiment une moyenne annuelle.
  - 29 cas de test recoivent une `relative_error_margin` de 1e-6. Une quantite annuelle est stockee
    au douzieme en float32 par `set_input_divide_by_period`, et la somme des douze mois ne restitue
    pas la quantite annuelle au bit pres : l'ecart observe est d'au plus 3,1e-7 en relatif, soit six
    ordres de grandeur sous le plus petit pas tarifaire du bareme (0,01 EUR/MWh).
  - 18 assertions portant sur une assiette passent en periode mensuelle, sans qu'aucun nombre ne
    change : la composition d'une assiette est lineaire.
  - Aucun test ne change de verdict : 296 verts et 17 rouges avant comme apres. Les 17 rouges sont
    les desaccords assumes des agregats 2040-TIC, inchanges.

## 1.1.7 - [#31](https://github.com/openfisca/openfisca-france-entreprises/pull/31)

* Tax and benefit system evolution.
* Impacted periods: from 01/01/1993.
* Impacted areas:
  - `variables/taxes/formula_helpers`
  - `variables/taxes/taxation_energies/taxation_autres_produits_energetiques`
  - `variables/taxes/taxation_energies/taxation_charbon`
  - `variables/taxes/taxation_energies/taxation_electricite`
  - `variables/taxes/taxation_energies/taxation_gaz_naturel`
  - `parameters/energies`
* Details:
  - Moyenne mensuelle des tarifs : de nombreux tarifs entrent en vigueur en cours d'annee alors que
    le modele raisonne en periodes annuelles. Les lire au 1er janvier appliquait l'ancien tarif, ou
    le nouveau, a toute l'annee. Les 230 lectures concernees passent par `tarif_moyen_annuel`.
  - Nouveau comportement quand une ligne de tarif reduit disparait en cours d'annee : le repli est
    le tarif normal, et non zero. Une abrogation seche sans article successeur reste repliee sur
    zero.
  - GPL sous condition d'emploi : indices 30 bis, 31 bis et 33 bis retires du tableau B de l'article
    265 du code des douanes au 01/07/2020 (article 60 I 1 de la LF 2020), sans successeur. Ces
    consommations relevent des indices generaux a 20,71 EUR/100 kg.
  - Gazole non routier : la cloture du 01/07/2021 etait erronee, l'article 265 octies A et B
    maintenant le tarif de 18,82 EUR/hL. Elle passe au 01/01/2022, avec le reste du tableau B.
  - TICGN des entreprises grandes consommatrices : le tarif reduit naissant au 01/04/2014, la
    lecture se replie avant cette date sur le tarif normal, qui vaut aussi 1,19 EUR/MWh.
  - TICC : taxe creee au 01/07/2007 par le III de l'article 36 de la LFR 2006, et non au
    01/01/2007. Janvier a juin 2007 ne portent pas de taxe.
  - Manutention portuaire : la formule lisait le tarif reduit TICFE au-dela du 01/01/2022, alors que
    la TICFE disparait avec la bascule CIBS et que le tarif reduit d'accise n'entre en vigueur qu'au
    01/01/2023. Tarif normal sur 2022, tarif reduit d'accise a partir de 2023.
  - CSPE : le changement de tarif de 2011 est date du 01/07/2011 et non du 31/07/2011.
  - Les parametres `parameters/energies` sont desormais identiques octet pour octet a ceux du bareme
    IPP sur les 321 chemins communs.

## 1.1.6 - [#19](https://github.com/openfisca/openfisca-france-entreprises/pull/19)

* Technical improvement: TDCFE coefficient as vectorized parameter (same approach as TCCFE in #18).
* Impacted areas: variables/taxes/taxation_energies/tdcfe, parameters/energies/electricite/tcfe/tdcfe.
* Details:
  - Add parameter `tcfe.tdcfe.coefficient` (YAML) by department code, 2011–2021, only change dates
  - Single `taux_tdcfe` formula reading `tcfe.tdcfe.coefficient[departement]` at period; remove 11 variables `tdcfe_coefficient_multiplicateur_normal_20XX` and 11 files `taux_2011.py` … `taux_2021.py`
  - Tests: `test_tdcfe_taux.yaml` asserts `taux_tdcfe` for 2012, 2015, 2021

## 1.1.5

* Technical improvement: standardise OpenFisca-Core imports to `model_api`.
* Impacted areas: variables (bilan, compte_resultat, consommation_energie, taxes), CONTRIBUTING.
* Details:
  - Replace `from openfisca_core.periods import YEAR` + `from openfisca_core.variables import Variable` with `from openfisca_core.model_api import Variable, YEAR` across the codebase
  - Keep `from openfisca_core.periods import Instant` only where needed (boulier_tarifaire, taxation_charbon); `Instant` is not re-exported by model_api
  - Merge existing model_api imports with YEAR/Variable/select/where/Instant where applicable (variables_economiques, boulier_tarifaire, taxation_charbon, tdcfe, tccfe)
  - CONTRIBUTING: add "Code conventions → Imports from OpenFisca-Core" (prefer model_api; other core imports rare and justified)

## 1.1.4

* Code quality: fix E501 line length violations.
* Impacted areas: code formatting, linting compliance.
* Details:
  - Fix all E501 (line too long) violations to comply with 120 character limit
  - Reformatted long docstrings, comments, and expressions in taxation modules
  - Updated pyproject.toml line-length setting to 120
  - All tests pass, no functional changes

## 1.1.3

* Technical improvement: use latest openfisca-core and remove monkey patches.
* Impacted areas: dependency, Python version support.
* Details:
  - Bump openfisca-core to >=44 (uses int16 for enum indices; NAF overflow workaround no longer needed)
  - Remove enum index overflow monkey patch from package __init__
  - requires-python set to >=3.10 (openfisca-core 44 drops 3.9)
  - test_ticgn: add absolute_error_margin: 1 for Test 1986 (float precision with core 44)

## 1.1.2

* Move hardcoded parameters to OpenFisca YAML (audit steps 1–4).
* Impacted areas: energies (SEQE, TICFE electro-intensité, TDCFE/TCCFE kVA), impôts sur les sociétés.
* Details:
  - Add parameters: energies.seuils_seqe (intensité production/VA, part facture énergie/CA, part taxe/VA); energies.electricite.ticfe.electro_intensive.seuils (tranches électro-intensité, intensité échanges pays tiers, hyper); impots_societes.prelevement_exceptionnel_hydrocarbures (seuil CA, taux).
  - Formulas use parameters instead of literals in taxation_charbon, taxation_autres_produits_energetiques, taxation_gaz_naturel, taxation_electricite, caracteristiques_etablissement, consommation_energie.electricite, impots_societes, tdcfe, tccfe.
  - TDCFE/TCCFE use TICFE categorie_fiscale_petite_et_moyenne_entreprise (36 kVA) and categorie_fiscale_haut_puissance (250 kVA); 36 kVA parameter extended to 2011 for TCFE formulas.

## 1.1.1

* Repository cleanup.
* Impacted areas: repository structure, CI/CD, examples.
* Details:
  - Remove all openfisca-template leftover files (example variables, reforms, tests, parameters)
  - Fix test-api.sh to use openfisca_france_entreprises instead of openfisca_country_template
  - Update open_api_config to use real variables/parameters
  - Update situation_examples to use real variables (apet, postal_code)

## 1.1.0

* Tooling and formula vectorization.
* Impacted periods: all.
* Impacted areas: build, dev tooling, energy variables, TICFE/TDCFE/TCCFE, TICPE regional majorations.
* Details:
  - Migration to uv, pyproject.toml: ruff (config aligned with openfisca-nouvelle-caledonie), isort, yamllint; remove flake8, pylint, autopep8, pyupgrade
  - Bump openfisca-core to >=43.3.8,<44
  - Vectorized formulas (OpenFisca vectorial computing): electricité, gaz naturel, charbon, autres produits énergétiques, caractéristiques établissement; taux TDCFE/TCCFE (select); majorations régionales TICPE (département avec select + _dep_in)
  - Tests: run only `openfisca_france_entreprises/tests` so parameter YAMLs are not collected
  - docs/VECTORISATION_FORMULAS.md: conventions and guide

## 1.0.0 - [#1](https://github.com/pzuldp/openfisca-france-firms/pull/1)

* Tax and benefit system evolution.
* Impacted periods: all.
* Impacted areas: all
* Details:
  - Adaptation du template avec la création des entités UniteLegale et Etablissement
  - Création du bilan et de ses variables
  - Création du compte de résultat et de ses variables
  - Création des TICC et TICGN
  - Premiers tests

## 0.0.1 - [#0](https://github.com/openfisca/country-template/pull/0)

* Tax and benefit system evolution.
* Impacted periods: all.
* Impacted areas:
  - `benefits`.
  - `demographics`.
  - `housing`.
  - `income`.
  - `stats`.
  - `taxes`.
* Details:
  - Import model from template
