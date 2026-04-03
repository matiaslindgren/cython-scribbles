from setuptools import setup, Extension
from Cython.Build import cythonize
from pathlib import Path


def sources(*paths: str) -> list[Path]:
    return [Path("./src") / p for p in paths]


extra_compile_args = ["-std=c23"]

ext_modules = [
    Extension(
        "vendor_vectorlib",
        sources=sources(
            "vendor/vectorlib/vectorlib_vector.c",
            "vendor/vectorlib/vectorlib_pymodule.c",
        ),
        extra_compile_args=extra_compile_args,
    ),
]

cython_modules = [
    Extension(
        "hello_lib",
        sources=sources("hello_lib.py"),
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        "is_prime",
        sources=sources("is_prime.py", "vendor/primelib/primelib_prime.c"),
        extra_compile_args=extra_compile_args,
        libraries=["m"],
    ),
    Extension(
        "hasher",
        sources=sources("hasher.pyx", "vendor/hashlib/hashlib_hasher.c"),
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        "vector",
        sources=sources(
            "vector.py",
        ),
        extra_compile_args=extra_compile_args,
    ),
]

ext_modules.extend(
    cythonize(
        cython_modules,
        annotate=True,
    )
)

setup(
    name="cython_scribbles",
    ext_modules=ext_modules,
)
