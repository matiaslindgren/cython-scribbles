cdef extern from "vendor/hasher/hasher.h":
    cdef size_t hasher_djb2(unsigned char* s, size_t n)

def djb2(unsigned char* s):
    return hasher_djb2(s, len(s))

