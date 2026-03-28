from cpython.bytes cimport PyBytes_FromStringAndSize
from cpython.mem cimport PyMem_Malloc, PyMem_Free

cdef public size_t public_hasher_cpython_bytes_hash(const char* const s, size_t n):
    return <size_t>hash( PyBytes_FromStringAndSize(s, n))

cdef extern from "vendor/hasher/hasher.h":
    cdef size_t hasher_djb2(const unsigned char* const s, size_t n)
    cdef size_t hasher_strings_pyhash(const unsigned char* const strings, size_t* const lengths, size_t n)

def djb2(const unsigned char[:] s not None):
    if len(s) == 0:
        return 0
    return hasher_djb2(&s[0], len(s))

def strings_pyhash(list[bytes] strings):
    cdef size_t* lengths
    cdef bytes data
    cdef const unsigned char[:] dataview

    if sum(map(len, strings)) == 0:
        return 0

    lengths = <size_t*>PyMem_Malloc(len(strings) * sizeof(size_t))
    if not lengths:
        raise MemoryError(f"failed allocating (size_t*)lengths array for {len(strings)=}")

    try:
        for i, s in enumerate(strings):
            lengths[i] = len(s)
        data = b"".join(strings)
        dataview = data
        return hasher_strings_pyhash(&dataview[0], lengths, len(strings))
    finally:
        PyMem_Free(lengths)
