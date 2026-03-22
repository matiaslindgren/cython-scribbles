# do not edit
# generated with `make setup.py` at 2026-03-22T16:47:28-04:00
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cython_scribbles",
    ext_modules=cythonize([pyx for pyx in "empty.pyx hello_lib.pyx".split(" ")]),
)
