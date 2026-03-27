import pytest
from functools import cache

from hasher import djb2


def expected(s: bytes) -> int:
    def m(h: int) -> int:
        return h % (2**64)

    h = 5381
    for c in s:
        h = m(m(m(h << 5) + h) + c)
    return h


@cache
def get_this() -> str:
    from contextlib import redirect_stdout
    from io import StringIO

    with redirect_stdout(StringIO()) as out:
        import this  # noqa: F401

    return out.getvalue()


@pytest.mark.parametrize(
    "s",
    [
        pytest.param(p, id=f"{p!r}")
        for p in [
            b"",
            b"1",
            b"hey",
            b" ",
            b"hello 1234",
            get_this().encode(),
        ]
    ],
)
def test_hasher_djb2(s: bytes) -> None:
    assert djb2(s) == expected(s)
