cdef extern from "vendor/hashlib/hashlib_hasher.h":
    cdef size_t hashlib_hasher_djb2(
            const unsigned char* const s,
            size_t n)
    cdef size_t hashlib_hasher_strings_pyhash(
            const unsigned char* const strings,
            size_t* const lengths,
            size_t n)
