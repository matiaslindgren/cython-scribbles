cdef extern from "vendor/primelib/primelib_prime.h":
    cdef bint primelib_is_prime(int x)
