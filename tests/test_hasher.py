import pytest
from functools import cache

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


@cache
def get_this() -> str:
    from contextlib import redirect_stdout
    from io import StringIO

    with redirect_stdout(StringIO()) as out:
        import this  # noqa: F401

    return out.getvalue()


def strings_to_hash() -> list[str]:
    return [
        "",
        "1",
        "hey",
        " ",
        "hello 1234",
        "😂",
        "\n",
        get_this(),
    ]


@pytest.mark.parametrize(
    "s",
    [
        pytest.param(
            p.encode("utf-8"),
            id=f"{p!r}" if len(p) < (n := 24) else f"{p[:n]!r}...",
        )
        for p in strings_to_hash()
    ],
)
def test_hasher_djb2(s: bytes) -> None:
    assert djb2(s) == py_djb2(s)


@pytest.mark.parametrize(
    "strings",
    [
        pytest.param([], id="no strings"),
        pytest.param([b"", b"", b""], id="three empty strings"),
        pytest.param([b"a"], id="just 'a'"),
        pytest.param([b"ab"], id="just 'ab'"),
        pytest.param([b"ab", b"cd"], id="'ab' and 'cd'"),
        pytest.param([s.encode("utf-8") for s in strings_to_hash()], id="many non-empty strings"),
    ],
)
def test_hasher_strings_pyhash(strings: list[bytes]) -> None:
    assert strings_pyhash(strings) == py_strings_pyhash(strings)
