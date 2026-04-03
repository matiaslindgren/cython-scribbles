cdef extern from "vendor/vectorlib/vectorlib_vector.h":
    struct vectorlib_vector:
        double* data
        size_t length

    bint vectorlib_add(vectorlib_vector* res, vectorlib_vector* lhs, const vectorlib_vector* rhs)
    bint vectorlib_sub(vectorlib_vector* res, vectorlib_vector* lhs, const vectorlib_vector* rhs)
    bint vectorlib_mul(vectorlib_vector* res, vectorlib_vector* lhs, const vectorlib_vector* rhs)


cdef extern from "vendor/vectorlib/vectorlib_pymodule.h":
    ctypedef class vendor_vectorlib.InternalVectorF64 [
            object pymodule_PyVectorF64, check_size error]:
        cdef vectorlib_vector v
