from setuptools import setup, Extension
from Cython.Build import cythonize
from pathlib import Path


def sources(*paths: str) -> list[Path]:
    return [Path("./src") / p for p in paths]


ext_modules = [
    # trivial example in pure python
    Extension(
        "hello_lib",
        sources=sources("hello_lib.py"),
    ),
    # still pure python but linking to cmath and using a 3rd party pure C lib
    Extension(
        "is_prime",
        sources=sources("is_prime.py", "vendor/primelib/primelib_prime.c"),
        libraries=["m"],
    ),
    # somewhat messier: pyrex that uses 3rd party pure C libs, but the pure C lib expects to link to a Cython generated public (extern) function we define in Cython
    Extension(
        "hasher",
        sources=sources("hasher.pyx", "vendor/hashlib/hashlib_hasher.c"),
    ),
]

setup(
    name="cython_scribbles",
    ext_modules=cythonize(
        ext_modules,
        annotate=True,
    ),
)
