SHELL := /bin/bash

BUILD_LIB_DIR := out/bld
BUILD_TMP_DIR := out/tmp
BUILD_PATHS := $(BUILD_LIB_DIR) $(BUILD_TMP_DIR)

MODULES := hasher hello_lib is_prime vector

PY_LIBRARY_SUFFIX := $(shell python -c 'from sysconfig import get_config_var as g; print(g("EXT_SUFFIX"))')
BUILD_DEPS := $(shell python get-build-requires.py)

SOURCE_PATHS := $(addsuffix .pyx,$(addprefix src/,$(MODULES)))
DECLARATION_PATHS := $(shell find src -maxdepth 1 -type f -name '*.pxd')
VENDOR_PATHS := $(shell find src/vendor -type f -name '*.c' -o -name '*.h')

GENERATED_SOURCE_PATHS := $(subst .pyx,.c,$(SOURCE_PATHS))
GENERATED_HEADER_PATHS := $(subst .pyx,.h,$(SOURCE_PATHS))
GENERATED_LIBRARY_PATHS := $(subst .pyx,$(PY_LIBRARY_SUFFIX),$(SOURCE_PATHS))
GENERATED_ANNOTATION_PATHS := $(subst .pyx,.html,$(SOURCE_PATHS))
GENERATED_EGG_INFO := src/cython_scribbles.egg-info

PYCACHE_PATHS := $(shell find src tests -type d -name __pycache__)

.PHONY: all
all: install_build_tools test_pyx build_debug dev_install test_py

.PHONY: install_build_tools
install_build_tools:
	pip install $(BUILD_DEPS)

.PHONY: dev_install
dev_install:
	pip install -e .[dev]

.PHONY: clean
clean:
	$(RM) -r out $(GENERATED_SOURCE_PATHS) $(GENERATED_HEADER_PATHS) $(GENERATED_LIBRARY_PATHS) $(GENERATED_ANNOTATION_PATHS) $(GENERATED_EGG_INFO) $(PYCACHE_PATHS)

out $(BUILD_PATHS):
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
format: format_c format_py

.PHONY: format_c
format_c: $(VENDOR_PATHS)
	clang-format --verbose -i $^

.PHONY: format_py
format_py:
	ruff check --fix
	ruff format

.PHONY: test
test: test_pyx test_py

.PHONY: test_pyx
test_pyx: $(shell find src -type f -name '*.pyx') $(DECLARATION_PATHS)
	cython-lint --max-line-length 100 $^

.PHONY: test_py
test_py:
	ruff check
	ruff format --check
	pytest -vv --capture=no tests
