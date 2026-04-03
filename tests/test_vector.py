from operator import add, sub, mul

import pytest
from pytest import approx
from hypothesis import given, strategies as st

from .fuzz_strategies import non_negative_sizes, nice_floats, two_float_lists_same_length
from vector import VectorF64


@given(non_negative_sizes())
def test_init_empty_vector_f64(length: int) -> None:
    v = VectorF64(length)
    assert v
    assert len(v) == length
    for x in v:
        assert x == 0.0
    assert v.into_list() == [0.0 for _ in range(length)]


@given(st.lists(nice_floats(), min_size=1))
def test_init_nonempty_vector_f64(values: list[float]) -> None:
    v = VectorF64(values)
    assert len(v) == len(values)
    # no approx, must be exact copy of each bit!
    assert v.into_list() == values


@pytest.mark.parametrize(
    "op",
    [pytest.param(op, id=f"{op.__name__}") for op in [add, sub, mul]],
)
@given(two_float_lists_same_length())
def test_bin_ops_vectors_f64(op, args: tuple[list[float], list[float]]) -> None:
    v1, v2 = args
    vec1 = VectorF64(v1)
    vec2 = VectorF64(v2)
    assert len(vec1) == len(vec2)

    result = op(vec1, vec2)
    expected = [op(x1, x2) for x1, x2 in zip(v1, v2)]

    assert len(vec1) == len(result)
    assert len(vec1) == len(expected)

    assert vec1.into_list() == v1
    assert vec2.into_list() == v2
    for r, e in zip(result, expected):
        assert r == approx(e)
