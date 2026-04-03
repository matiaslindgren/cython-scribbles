from typing import Any

import pytest
from hypothesis import given, strategies as st

from .fuzz_strategies import non_negative_sizes, nice_floats

from vendor_vectorlib import InternalVectorF64


@pytest.mark.parametrize(
    "arg",
    [
        pytest.param(p, id=f"{p!r}")
        for p in [
            float("inf"),
            -float("inf"),
            -12.3,
            45.6,
            "one",
            None,
            {},
            ("hello", "world"),
            ("1.5", "2.5"),
            {1.5, 2.5},
            ["1", "2"],
        ]
    ],
)
def test_create_vector_invalid_type(arg: Any) -> None:
    with pytest.raises(TypeError):
        InternalVectorF64(arg)


@pytest.mark.parametrize(
    "arg",
    [
        pytest.param(p, id=f"{p!r}")
        for p in [
            -(2**32),
            -10,
            -1,
            0,
            [],
        ]
    ],
)
def test_create_vector_valid_type_invalid_value(arg: Any) -> None:
    with pytest.raises(ValueError):
        InternalVectorF64(arg)


@given(non_negative_sizes())
def test_create_vector_from_length(length: int) -> None:
    assert InternalVectorF64(length)


@given(st.lists(nice_floats(), min_size=1))
def test_create_vector_from_values(values: list[float]) -> None:
    assert InternalVectorF64(values)
