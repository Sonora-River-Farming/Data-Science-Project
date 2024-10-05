#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = sonora_river_farming
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python3.12

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 modules
	isort --check --diff --profile black modules
	black --check --config pyproject.toml modules

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml modules




## Set up python interpreter environment
#.PHONY: create_environment
#create_environment:
#	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
#	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	
.PHONY: create_environment
create_environment:
	@bash -c "if [ -z `which $(PYTHON_INTERPRETER)` ]; then echo 'Python interpreter $(PYTHON_INTERPRETER) not found!'; exit 1; fi; \
	virtualenv venv && \
	echo '>>> New virtualenv created in venv. Activate with:'; \
	echo 'source venv/bin/activate'"


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make Dataset
.PHONY: data
#data: requirements
data:
#$(PYTHON_INTERPRETER) modules/dataset.py --url https://files.conagua.gob.mx/aguasnacionales/TODOS%20LOS%20MONITOREOS.xlsb --file water_quality_raw_data.xlsb
	$(PYTHON_INTERPRETER) modules/dataset.py

## Download Data
.PHONY: download
download:
	$(PYTHON_INTERPRETER) modules/dataset_modules/downloader.py download --url "<URL>" --info "<INFO>" --input-path "<INPUT_PATH>"

## Process Data
.PHONY: process
process:
	PYTHONPATH="$(PWD)/modules" $(PYTHON_INTERPRETER) -m dataset_modules.processor

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
