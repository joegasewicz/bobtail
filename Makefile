test:
	pipenv run pytest -vvvv

lint:
	pipenv run pylint bobtail

docs:
	make -C docs html

install:
	pipenv install
	pipenv install --dev

# Tox is only for local development (we use github actions in CI)
tox:
	pipenv run tox
