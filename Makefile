# Makefile for the Navigating Data Errors tutorial.

# Summary and context path of this makefile.
SUMMARY := This the main Makefile of the project intended to aid in all basic development tasks.
PYTHON := $(shell which python)
SHELL := /bin/bash

# Paths to the parent directory of this makefile and the repo root directory.
MY_DIR_PATH := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
ROOT_DIR_PATH := $(realpath $(MY_DIR_PATH))
VENV_DIR := venv

# Include common make functions.
include $(ROOT_DIR_PATH)/dev/makefiles/show-help.mk

$(VENV_DIR)/touchfile:
	test -d $(VENV_DIR) || python -m venv $(VENV_DIR) --prompt "(navigating-data-errors)"
	touch $(VENV_DIR)/touchfile

.PHONY: shell
## Load an instance of the shell with the appropriate virtual environment.
shell: $(VENV_DIR)/touchfile
	@exec bash --init-file <(echo "source $(VENV_DIR)/bin/activate")

.PHONY: setup
## Install the all the dependencies.
setup: pyproject.toml
	pip install wheel
	pip install -e .
	pip install notebook

.PHONY: format
## Run the black formatter on all Python files.
format: nde
	@echo "Running formatter..."
	@$(PYTHON) -m black --line-length 120 nde

.PHONY: jupyter
## Start a Jupyter notebook server.
jupyter:
	@$(PYTHON) -m jupyter lab