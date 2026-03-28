import cython
from cython.cimports.is_prime import primelib_is_prime


def is_prime(x: cython.int) -> cython.int:
    return primelib_is_prime(x)
