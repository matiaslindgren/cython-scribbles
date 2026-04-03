from types import ModuleType
from pathlib import Path
from sysconfig import get_config_var


def assert_is_extension(module: ModuleType) -> None:
    so_suffix = get_config_var("EXT_SUFFIX")
    assert Path(module.__file__).name == f"{module.__name__}{so_suffix}"


def test_import_hello_lib():
    import hello_lib  # noqa: F401

    assert_is_extension(hello_lib)

    from hello_lib import say_hello_to  # noqa: F401


def test_import_is_prime():
    import is_prime  # noqa: F401

    assert_is_extension(is_prime)

    from is_prime import is_prime  # noqa: F401,F811


def test_import_hasher():
    import hasher  # noqa: F401

    assert_is_extension(hasher)

    from hasher import djb2  # noqa: F401
    from hasher import strings_pyhash  # noqa: F401


def test_import_vendor_vectorlib():
    import vendor_vectorlib  # noqa: F401

    assert_is_extension(vendor_vectorlib)

    from vendor_vectorlib import InternalVectorF64  # noqa: F401


def test_import_vector():
    import vector  # noqa: F401

    assert_is_extension(vector)

    from vector import VectorF64  # noqa: F401
