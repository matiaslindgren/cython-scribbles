def test_import_hello_lib():
    import hello_lib  # noqa: F401

    assert hello_lib.__file__.endswith(".so")

    from hello_lib import say_hello_to  # noqa: F401


def test_import_is_prime():
    import is_prime  # noqa: F401

    assert is_prime.__file__.endswith(".so")

    from is_prime import is_prime  # noqa: F401,F811


def test_import_hasher():
    import hasher  # noqa: F401

    assert hasher.__file__.endswith(".so")

    from hasher import djb2  # noqa: F401
    from hasher import strings_pyhash  # noqa: F401


def test_import_vendor_vectorlib():
    import vendor_vectorlib  # noqa: F401

    assert vendor_vectorlib.__file__.endswith(".so")

    from vendor_vectorlib import InternalVectorF64  # noqa: F401


def test_import_vector():
    import vector  # noqa: F401

    from vector import VectorF64  # noqa: F401
