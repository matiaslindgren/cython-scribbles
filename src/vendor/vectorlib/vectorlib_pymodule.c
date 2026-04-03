#include <Python.h>
#if !(PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION == 14)
  #error "expected Python.h 3.14"
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

static int
pymodule_PyVectorF64_init(PyObject* self_obj, PyObject* args, PyObject* Py_UNUSED(kwds)) {
  assert(self_obj);
  assert(args);

  pymodule_PyVectorF64* self = (pymodule_PyVectorF64*)self_obj;
  PyObject* arg              = nullptr;
  size_t length              = 0;

  if (!PyArg_ParseTuple(args, "O", &arg)) {
    goto return_error;
  }

  if (PyLong_CheckExact(arg)) {
    length = PyLong_AsSize_t(arg);
    if (!length || (PyErr_Occurred() && (length == (size_t)-1))) {
      PyErr_Format(
          PyExc_ValueError,
          "InternalVectorF64 initial count of zeros must be a positive integer, not %S",
          arg
      );
      goto return_error;
    }
  } else if (PyList_CheckExact(arg)) {
    Py_ssize_t arg_length = PyList_Size(arg);
    if (PyErr_Occurred()) {
      goto return_error;
    }
    if (arg_length <= 0) {
      PyErr_Format(
          PyExc_ValueError,
          "InternalVectorF64 initial list[float] arg (length=%zd) must not be empty",
          arg_length
      );
      goto return_error;
    }
    length = (size_t)arg_length;
  } else {
    PyErr_Format(
        PyExc_TypeError,
        "invalid arg='%S' to InternalVectorF64.__init__, should be: int | list[float]",
        arg
    );
    goto return_error;
  }

  if (!vectorlib_zeros(&(self->v), length)) {
    PyErr_Format(PyExc_RuntimeError, "failed allocating InternalVectorF64 of length %zu", length);
    goto return_error;
  }

  if (PyList_Check(arg)) {
    for (size_t i = 0; i < length; ++i) {
      PyObject* py_value = PyList_GET_ITEM(arg, (Py_ssize_t)i);
      double value       = PyFloat_AsDouble(py_value);
      if (PyErr_Occurred() && (value == -1.0)) {
        goto return_error;
      }
      (self->v).data[i] = value;
    }
  }

  return 0;

return_error:
  return -1;
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

static PyModuleDef_Slot pymodule_vectorlib_slots[] = {
    {Py_mod_exec,                  pymodule_exec                             },
    {Py_mod_multiple_interpreters, Py_MOD_MULTIPLE_INTERPRETERS_NOT_SUPPORTED},
    {0,                            nullptr                                   },
};

static PyModuleDef pymodule_vectorlib = {
    .m_base  = PyModuleDef_HEAD_INIT,
    .m_name  = "vendor_vectorlib",
    .m_doc   = "smol linalg lib",
    .m_size  = 0,
    .m_slots = pymodule_vectorlib_slots,
};

PyMODINIT_FUNC PyInit_vendor_vectorlib(void) {
  return PyModuleDef_Init(&pymodule_vectorlib);
}
