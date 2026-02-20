## 1.1.2 - Unreleased

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
