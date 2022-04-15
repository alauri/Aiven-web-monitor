RM=rm
PIP=pip
MYPY=mypy

POETRY=poetry

PYTEST=pytest -s -vv


all: help

help:
	@echo "install              - Install production dependencies."
	@echo " install-dev         - Install all dependencies."
	@echo "update               - Update dependencies and write lock file."
	@echo "test                 - Run UnitTests."
	@echo " test-all            - Run all tests (it might take a while)."
	@echo "doc                  - Build doc locally (HTML format)."
	@echo "lint                 - Run codecheckes."
	@echo " lint-dev            - Run tests checkes."
	@echo " lint-all            - Run all checkes."
	@echo "clean                - Delete temporary files."
	@echo "reset                - Remove installed dependencies."


# Setup environment
install:
	$(POETRY) install --no-dev


install-dev:
	$(POETRY) install


update:
	$(POETRY) update


# Manage local environment
.PHONY: doc
doc:
	$(RM) -rf doc/build
	$(POETRY) run sphinx-build ./doc/source ./doc/build


lint:
	$(POETRY) run black moniven
	$(POETRY) run isort moniven
	$(POETRY) run flake8 moniven
	$(POETRY) run $(MYPY) --install-types --non-interactive moniven


lint-dev:
	$(POETRY) run black tests
	$(POETRY) run isort tests
	$(POETRY) run flake8 tests
	$(POETRY) run $(MYPY) --install-types --non-interactive tests


lint-all:
	$(MAKE) lint
	$(MAKE) lint-dev


test:
	$(POETRY) run $(PYTEST) -m unit


test-all:
	$(POETRY) run $(PYTEST)


clean:
	find . -type d -name "*egg*"|xargs -n 500 $(RM) -rf
	find . -type d -name "__pycache__"|xargs -n 500 $(RM) -rf
	find . -type d -name ".*_cache"|xargs -n 500 $(RM) -rf
	find . -type f -name "*.pyc" -delete
	$(RM) -rf dist site htmlcov doc/build .tox .*_cache .covarage


reset:
	$(MAKE) clean
	$(POETRY) run $(PIP) freeze > req.txt
	$(POETRY) run $(PIP) uninstall -y -r req.txt
	$(RM) req.txt
