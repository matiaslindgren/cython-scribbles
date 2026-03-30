SHELL := /bin/bash

SRC_DIR := ./src
OUTPUT_DIR := ./out
BUILD_LIB_DIR := $(OUTPUT_DIR)/bld
BUILD_TMP_DIR := $(OUTPUT_DIR)/tmp
BUILD_PATHS := $(BUILD_LIB_DIR) $(BUILD_TMP_DIR)

SOURCE_PATHS := $(shell find $(SRC_DIR) -type f -name '*.pyx')
VENDOR_PATHS := $(shell find $(SRC_DIR)/vendor -type f -name '*.c' -o -name '*.h')

PY_LIBRARY_SUFFIX := $(shell python -c 'from sysconfig import get_config_var as g; print(g("EXT_SUFFIX"))')
GENERATED_SOURCE_PATHS := $(subst .pyx,.c,$(SOURCE_PATHS))
GENERATED_HEADER_PATHS := $(subst .pyx,.h,$(SOURCE_PATHS))
GENERATED_LIB_PATHS := $(subst .pyx,$(PY_LIBRARY_SUFFIX),$(SOURCE_PATHS))
GENERATED_ANNOTATION_PATHS := $(subst .pyx,.html,$(SOURCE_PATHS))
GENERATED_EGG_INFO := $(SRC_DIR)/cython_scribbles.egg-info

BUILD_DEPS := $(shell python get-build-requires.py)

.PHONY: all
all: install_build_tools build_debug dev_install

.PHONY: install_build_tools
install_build_tools:
	pip install $(BUILD_DEPS)

.PHONY: dev_install
dev_install:
	pip install -e .[dev]

.PHONY: clean
clean:
	$(RM) -r $(OUTPUT_DIR) $(GENERATED_SOURCE_PATHS) $(GENERATED_HEADER_PATHS) $(GENERATED_LIB_PATHS) $(GENERATED_ANNOTATION_PATHS) $(GENERATED_EGG_INFO)

$(OUTPUT_DIR) $(BUILD_PATHS):
	mkdir -p $@

.PHONY: build_debug
build_debug: $(BUILD_PATHS)
	python setup.py build_ext \
		--verbose \
		--build-lib=$(BUILD_LIB_DIR) \
		--build-temp=$(BUILD_TMP_DIR) \
		--cython-c-in-temp \
		--cython-gdb

.PHONY: format
format: $(VENDOR_PATHS)
	clang-format --verbose -i $^
	ruff check --fix
	ruff format

.PHONY: test
test:
	ruff check
	ruff format --check
	pytest -vv --capture=no tests
