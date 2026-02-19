all: test

uninstall:
	uv pip uninstall openfisca_france_entreprises || true

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;
	find . -type d -name '__pycache__' -exec rm -r {} +

deps:
	@# Dependencies are managed via uv sync, but keep this target for compatibility
	uv sync

install:
	@# Install openfisca_france_entreprises for development.
	@# `make install` installs the editable version of openfisca_france_entreprises.
	@# This allows contributors to test as they code.
	uv sync

build: clean
	@# Install openfisca_france_entreprises for deployment and publishing.
	@# `make build` allows us to be sure tests are run against the packaged version
	@# of openfisca_france_entreprises, the same we put in the hands of users and reusers.
	uv sync
	uv build
	uv pip uninstall --yes openfisca_france_entreprises 2>/dev/null || true
	find dist -name "*.whl" -exec uv pip install --force-reinstall {}[dev] \;

format:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	uv run ruff format `git ls-files | grep "\.py$$"`
	uv run isort `git ls-files | grep "\.py$$"`

check-syntax-errors:
	@# Check Python syntax errors.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	@uv run python -m py_compile `git ls-files | grep "\.py$$"` 2>&1 || (echo "Syntax errors found" && exit 1)

check-style: lint

lint:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	uv run isort --check `git ls-files | grep "\.py$$"`
	uv run ruff check `git ls-files | grep "\.py$$"`
	uv run yamllint `git ls-files | grep "\.yaml$$"`

test: clean
	@# Path must be openfisca_france_entreprises/tests only (not the whole package), so parameter YAMLs are not collected as tests.
	uv run openfisca test -c openfisca_france_entreprises openfisca_france_entreprises/tests

serve-local: build
	uv run openfisca serve --country-package openfisca_france_entreprises
