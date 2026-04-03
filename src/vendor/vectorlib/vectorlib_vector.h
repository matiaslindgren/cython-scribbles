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

static inline int vectorlib_resize(struct vectorlib_vector v[static 1], size_t new_length) {
  assert(v);
  assert(v->data);
  assert(v->length);
  assert(new_length);
  if (!(v->data = (double*)realloc(v->data, sizeof(double) * new_length))) {
    return 0;
  }
  v->length = new_length;
  return 1;
}

#define DEFINE_VECTORLIB_BIN_OP(FUNC_NAME, BIN_OP)        \
  static inline int FUNC_NAME(                            \
      struct vectorlib_vector v1[restrict static 1],      \
      const struct vectorlib_vector v2[restrict static 1] \
  ) {                                                     \
    assert(v1);                                           \
    assert(v2);                                           \
    if (v1->length != v2->length) {                       \
      return 0;                                           \
    }                                                     \
    for (size_t i = 0; i < v1->length; ++i) {             \
      v1->data[i] BIN_OP v2->data[i];                     \
    }                                                     \
    return 1;                                             \
  }

DEFINE_VECTORLIB_BIN_OP(vectorlib_add, +=)
DEFINE_VECTORLIB_BIN_OP(vectorlib_sub, -=)
DEFINE_VECTORLIB_BIN_OP(vectorlib_mul, *=)

#undef DEFINE_VECTORLIB_BINOP

#endif  // INCLUDED_VECTORLIB_VECTOR_H
