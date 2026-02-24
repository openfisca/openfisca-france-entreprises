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
