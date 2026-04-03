# cython-scribbles

Small [Cython](https://cython.readthedocs.io/en/stable/index.html) studies

## building

```bash
#!/usr/bin/env bash
python3.15d -m venv .venv && source .venv/bin/activate
```
```bash
#!/usr/bin/env bash
make
```
See Makefile for details.

## modules

### `hello_lib`

Trivial, pure Python hello world example

### `is_prime`

Wraps an external C library dependency

### `hasher`

Extern function defined in Cython, that an external C library dependency expects to be linked into the final shared object

### `vector`

Micro-sized linear algebra library written using the Python C API (without Cython), which is linked into and extended by the Cython module
