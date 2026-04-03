#include <Python.h>
#if !(PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION == 15)
  #error "expected Python.h for 3.15"
#endif

#include <assert.h>

#include "vectorlib_pymodule.h"
#include "vectorlib_vector.h"

static void pymodule_PyVectorF64_dealloc(PyObject* v_f64) {
  pymodule_PyVectorF64* self = (pymodule_PyVectorF64*)v_f64;
  assert(self);
  vectorlib_free(&(self->v));
  Py_TYPE(self)->tp_free(self);
}

static int pymodule_PyVectorF64_init(PyObject* v_f64, PyObject* args, PyObject* Py_UNUSED(kwds)) {
  pymodule_PyVectorF64* self = (pymodule_PyVectorF64*)v_f64;
  assert(self);

  Py_ssize_t length = 0;
  if (!PyArg_ParseTuple(args, "n", &length)) {
    return -1;
  }

  if (length <= (Py_ssize_t)0) {
    PyErr_Format(
        PyExc_TypeError,
        "InternalVectorF64 initial length must be a positive integer, not %zd",
        length
    );
    return -1;
  }

  if (!vectorlib_zeros(&(self->v), (size_t)length)) {
    PyErr_Format(PyExc_RuntimeError, "failed allocating InternalVectorF64 of length %zd", length);
    return -1;
  }

  return 0;
}

static PyTypeObject pymodule_PyVectorF64Type = {
    // clang-format off
    .ob_base      = PyVarObject_HEAD_INIT(nullptr, 0)
    .tp_name      = "vendor_vectorlib.InternalVectorF64",
    // clang-format on
    .tp_doc       = PyDoc_STR("low-level 64-bit float vector, do not use this API directly"),
    .tp_basicsize = sizeof(pymodule_PyVectorF64),
    .tp_itemsize  = 0,
    .tp_flags     = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new       = PyType_GenericNew,
    .tp_init      = pymodule_PyVectorF64_init,
    .tp_dealloc   = pymodule_PyVectorF64_dealloc,
};

static int pymodule_exec(PyObject* module) {
  PyTypeObject* vector_f64_type = &pymodule_PyVectorF64Type;
  if (PyType_Ready(vector_f64_type) < 0) {
    return -1;
  }
  if (PyModule_AddObjectRef(module, "InternalVectorF64", (PyObject*)vector_f64_type) < 0) {
    return -1;
  }
  return 0;
}

static PyModuleDef_Slot pymodule_slots[] = {
    {Py_mod_name, "vendor_vectorlib"},
    {Py_mod_doc,  "smol linalg lib" },
    {Py_mod_exec, pymodule_exec     },
    {0,           nullptr           },
};

PyMODEXPORT_FUNC PyModExport_vendor_vectorlib(void) {
  return pymodule_slots;
}
