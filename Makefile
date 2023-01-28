isort = pdm run isort .
black = pdm run black .
###############
# Environment #
###############
.PHONY: pkg
pkg: ;
	# Install system package dependencies

.PHONY: pkg_dev
pkg_dev:
	# Install development tools
	pip3 install pdm -U --user

.PHONY: venv
venv: pkg
	# Setup the virtual environment
	pdm install

.PHONY: dev_env
dev_env: pkg pkg_dev venv
	# Setup the whole development setup: package dependencies, dev tools and venv

.PHONY: clean
clean:
	# Clean up
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	find . -type d -name "*egg-info" | xargs rm -fr
	rm -rf *dist-info/ *egg-info/ linux/ *.xml dist/ .coverage .pytest_cache .mypy_cache htmlcov/ site/

.PHONY: clean-venv
clean-venv:
	# Clean up only the virtual environment
	pdm env remove in-project

#########
# Build #
#########
.PHONY: wheel
wheel:
	# Build the App wheel
	pdm build

################
# Test Targets #
################
.PHONY: test
test:
	@echo "--------------"
	@echo "- 🧪 Test 🧪 -"
	@echo "--------------"
	@pdm run pytest

################
# Code Quality #
################
.PHONY: format
format:
	@echo "-------------------"
	@echo "- 🎨 Formating 🎨 -"
	@echo "-------------------"

	$(isort)
	$(black)

	@echo ""

.PHONY: lint
lint:
	@echo "-----------------"
	@echo "- 🚨 Linting 🚨 -"
	@echo "-----------------"

	pdm run pylint -j 4 -f colorized src/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

	@echo ""

#######
# Run #
#######
.PHONY: run
run:
	pdm run demo

