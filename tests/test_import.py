def test_import_hello_lib():
    import hello_lib  # noqa: F401
    from hello_lib import say_hello_to  # noqa: F401


def test_import_is_prime():
    import is_prime  # noqa: F401
    from is_prime import is_prime  # noqa: F401,F811


def test_import_hasher():
    import hasher  # noqa: F401
    from hasher import djb2  # noqa: F401
    from hasher import strings_pyhash  # noqa: F401
