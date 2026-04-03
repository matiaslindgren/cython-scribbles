import pytest

from itertools import product
from vector import VectorF64


@pytest.mark.parametrize("length", range(1, 10))
def test_init_empty_vector_f64(length: int) -> None:
    v = VectorF64(length)
    assert v
    assert len(v) == length
    assert v.into_list() == [0.0 for _ in range(length)]


def init_values() -> list[float]:
    return [
        list(map(float, v))
        for v in [
            [-2],
            [-1],
            [0],
            [1],
            [2],
            [-1],
            [1, 2],
            [-1, 1],
            [-1, 0, 1],
            [-2, 0, 1],
            [-1, 0, 2],
        ]
    ]


@pytest.mark.parametrize(
    "values",
    [pytest.param(values, id=f"{values=!r}") for values in init_values()],
)
def test_init_nonempty_vector_f64(values: list[float]) -> None:
    v = VectorF64(1)
    v.from_list(values)
    assert len(v) == len(values)
    assert v.into_list() == [float(x) for x in values]


@pytest.mark.parametrize(
    ("v1", "v2"),
    [
        pytest.param(v1, v2, id=f"{v1=!r} {v2=!r}")
        for v1, v2 in product(init_values(), repeat=2)
        if len(v1) == len(v2)
    ],
)
def test_add_vectors_f64(v1: list[float], v2: list[float]) -> None:
    vec1 = VectorF64(1)
    vec2 = VectorF64(1)
    vec1.from_list(v1)
    vec2.from_list(v2)
    assert len(vec1) == len(vec2)
    vec1 += vec2
    assert vec1.into_list() == [x1 + x2 for x1, x2 in zip(v1, v2)]
    assert vec2.into_list() == v2
