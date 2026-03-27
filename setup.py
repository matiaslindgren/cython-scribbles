from setuptools import setup, Extension
from Cython.Build import cythonize
from pathlib import Path


def sources(*paths: str) -> list[Path]:
    return [Path("./src") / p for p in paths]


ext_modules = [
    Extension(
        "empty",
        sources=sources("empty.pyx"),
    ),
    Extension(
        "is_prime",
        sources=sources("is_prime.pyx", "vendor/prime/prime.c"),
        libraries=["m"],
    ),
    Extension(
        "hello_lib",
        sources=sources("hello_lib.pyx"),
    ),
]

setup(
    name="cython_scribbles",
    ext_modules=cythonize(
        ext_modules,
        annotate=True,
    ),
)
