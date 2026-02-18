all: test

uninstall:
	pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;
	find . -type d -name '__pycache__' -exec rm -r {} +

deps:
	pip install --upgrade pip build twine

install: deps
	@# Install openfisca_france_entreprises for development.
	@# `make install` installs the editable version of openfisca_france_entreprises.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade

build: clean deps
	@# Install openfisca_france_entreprises for deployment and publishing.
	@# `make build` allows us to be sure tests are run against the packaged version
	@# of openfisca_france_entreprises, the same we put in the hands of users and reusers.
	python -m build
	pip uninstall --yes openfisca_france_entreprises 2>/dev/null || true
	find dist -name "*.whl" -exec pip install --force-reinstall {}[dev] \;

format:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	ruff format `git ls-files | grep "\.py$$"`
	isort `git ls-files | grep "\.py$$"`

lint:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	isort --check `git ls-files | grep "\.py$$"`
	ruff check `git ls-files | grep "\.py$$"`
	yamllint `git ls-files | grep "\.yaml$$"`

test: clean
	@# Path must be openfisca_france_entreprises/tests only (not the whole package), so parameter YAMLs are not collected as tests.
	openfisca test -c openfisca_france_entreprises openfisca_france_entreprises/tests

serve-local: build
	openfisca serve --country-package openfisca_france_entreprises
