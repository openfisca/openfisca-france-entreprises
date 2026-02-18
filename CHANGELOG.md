## 1.1.0 - Unreleased

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
