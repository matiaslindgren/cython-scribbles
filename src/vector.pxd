cdef extern from "vendor/vectorlib/vectorlib_vector.h":
    struct vectorlib_vector:
        double* data
        size_t length

    bint vectorlib_resize(vectorlib_vector* v, size_t new_length)
    bint vectorlib_add(vectorlib_vector* v1, const vectorlib_vector* v2)
    bint vectorlib_sub(vectorlib_vector* v1, const vectorlib_vector* v2)
    bint vectorlib_mul(vectorlib_vector* v1, const vectorlib_vector* v2)


cdef extern from "vendor/vectorlib/vectorlib_pymodule.h":
    ctypedef class vendor_vectorlib.InternalVectorF64 [
            object pymodule_PyVectorF64, check_size error]:
        cdef vectorlib_vector v
