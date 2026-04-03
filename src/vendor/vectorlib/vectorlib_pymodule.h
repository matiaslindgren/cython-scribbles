#ifndef INCLUDED_VECTORLIB_PYMODULE_H
#define INCLUDED_VECTORLIB_PYMODULE_H
#include <Python.h>

#include "vectorlib_vector.h"

typedef struct {
  // clang-format off
  PyObject_HEAD
  struct vectorlib_vector v;
  // clang-format on
} pymodule_PyVectorF64;

#endif  // INCLUDED_VECTORLIB_PYMODULE_H
