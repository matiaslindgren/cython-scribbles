import pytest
from typing import Any
from itertools import chain

from vendor_vectorlib import InternalVectorF64


@pytest.mark.parametrize(
    "not_length",
    [
        pytest.param(p, id=f"{p!r}")
        for p in [
            -(2**32),
            -10,
            -1,
            0,
            "one",
            None,
            {},
            [],
        ]
    ],
)
def test_create_vector_invalid_length(not_length: Any) -> None:
    with pytest.raises(TypeError):
        InternalVectorF64(not_length)


@pytest.mark.parametrize(
    "length",
    chain(
        range(1, 10),
        range(125, 130),
        range(4090, 4100),
        range(2**16, 5 + 2**16),
    ),
)
def test_create_vector_valid_length(length: int) -> None:
    assert InternalVectorF64(length)
