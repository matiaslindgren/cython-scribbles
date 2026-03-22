SHELL := /bin/bash

OUTPUT_DIR := ./out
BUILD_LIB_DIR := $(OUTPUT_DIR)/bld
BUILD_TMP_DIR := $(OUTPUT_DIR)/tmp
BUILD_PATHS := $(BUILD_LIB_DIR) $(BUILD_TMP_DIR)

MODULE_NAME := cython_scribbles
SOURCE_PATHS := $(wildcard ./*.pyx)
GENERATED_SOURCE_PATHS := $(subst .pyx,.c,$(SOURCE_PATHS))
GENERATED_LIB_PATHS := $(subst .pyx,.cpython-313-darwin.so,$(SOURCE_PATHS))

.PHONY: all
all: build_debug dev_install

setup.py: setup.py.template $(SOURCE_PATHS)
	@printf '# do not edit\n' > $@
	@printf '# generated with `make setup.py` at %s\n' "$$(date -Iseconds)" >> $@
	@python -c 'from pathlib import Path; from string import Template; print(Template(Path("$<").read_text()).substitute(MODULE_NAME="$(MODULE_NAME)", SOURCE_PATHS="$(filter-out $<,$^)"), end="")' >> $@

.PHONY: dev_install
dev_install: setup.py
	pip install -e .[dev]

.PHONY: clean
clean:
	$(RM) -r $(OUTPUT_DIR) $(GENERATED_SOURCE_PATHS) $(GENERATED_LIB_PATHS) cython_scribbles.egg-info setup.py

$(OUTPUT_DIR) $(BUILD_PATHS):
	mkdir -p $@

.PHONY: build_debug
build_debug: setup.py $(BUILD_PATHS)
	python $< build_ext \
		--verbose \
		--build-lib=$(BUILD_LIB_DIR) \
		--build-temp=$(BUILD_TMP_DIR) \
		--cython-c-in-temp \
		--cython-gdb

.PHONY: format
format:
	ruff check --fix
	ruff format

.PHONY: test
test:
	ruff check
	ruff format --check
	pytest -v tests
