from hypothesis import given, strategies as st

from hasher import djb2, strings_pyhash


def py_uint_wrap(x: int, wrap: int = 2**64) -> int:
    return (x + wrap) % wrap


def py_djb2(s: bytes) -> int:
    if not s:
        return 0
    w = py_uint_wrap
    h = 5381
    for c in s:
        h = w(w(w(h << 5) + h) + c)
    return h


def py_strings_pyhash(strings: list[bytes]) -> int:
    if sum(len(s) for s in strings) == 0:
        return 0
    w = py_uint_wrap
    h = 654321
    for s in strings:
        s_hash = w(hash(s))
        h = w(w(h << 7) + s_hash)
    return h


@given(st.binary())
def test_hasher_djb2(s: bytes) -> None:
    assert djb2(s) == py_djb2(s)


@given(st.lists(st.binary()))
def test_hasher_strings_pyhash(strings: list[bytes]) -> None:
    assert strings_pyhash(strings) == py_strings_pyhash(strings)
