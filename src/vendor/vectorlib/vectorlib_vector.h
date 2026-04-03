#ifndef INCLUDED_VECTORLIB_VECTOR_H
#define INCLUDED_VECTORLIB_VECTOR_H
#include <assert.h>
#include <stdlib.h>

// never overlap data of two vectors!
struct vectorlib_vector {
  double* restrict data;
  size_t length;
};

static inline void vectorlib_clear(struct vectorlib_vector v[static 1]) {
  assert(v);
  *v = (struct vectorlib_vector){0};
}

static inline int vectorlib_zeros(struct vectorlib_vector v[static 1], size_t length) {
  assert(v);
  if (!length) {
    goto fail;
  }
  if (!(v->data = (double*)calloc(length, sizeof(double)))) {
    goto fail;
  }
  v->length = length;
  return 1;
fail:
  vectorlib_clear(v);
  return 0;
}

static inline void vectorlib_free(struct vectorlib_vector v[static 1]) {
  assert(v);
  if (v->data && v->length) {
    free(v->data);
  }
  vectorlib_clear(v);
}

#define DEFINE_VECTORLIB_BIN_OP(FUNC_NAME, BIN_OP)          \
  static inline int FUNC_NAME(                              \
      struct vectorlib_vector res[restrict static 1],       \
      const struct vectorlib_vector lhs[restrict static 1], \
      const struct vectorlib_vector rhs[restrict static 1]  \
  ) {                                                       \
    assert(res);                                            \
    assert(lhs);                                            \
    assert(rhs);                                            \
    const size_t n = res->length;                           \
    if (n != lhs->length || n != rhs->length) {             \
      return 0;                                             \
    }                                                       \
    for (size_t i = 0; i < n; ++i) {                        \
      res->data[i] = lhs->data[i] BIN_OP rhs->data[i];      \
    }                                                       \
    return 1;                                               \
  }

DEFINE_VECTORLIB_BIN_OP(vectorlib_add, +)
DEFINE_VECTORLIB_BIN_OP(vectorlib_sub, -)
DEFINE_VECTORLIB_BIN_OP(vectorlib_mul, *)

#undef DEFINE_VECTORLIB_BIN_OP

#endif  // INCLUDED_VECTORLIB_VECTOR_H
