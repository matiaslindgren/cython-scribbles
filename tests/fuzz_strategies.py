from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy


def nice_floats() -> SearchStrategy[float]:
    return st.floats(
        allow_nan=False,
        allow_infinity=False,
        allow_subnormal=False,
    )


def non_negative_sizes() -> SearchStrategy[int]:
    # 1 MiB of doubles should be enough
    return st.integers(
        min_value=1,
        max_value=(1024**2) // 8,
    )


@st.composite
def two_float_lists_same_length(draw) -> tuple[list[float], list[float]]:
    v1 = draw(st.lists(nice_floats(), min_size=1))
    v2 = draw(st.lists(nice_floats(), min_size=len(v1), max_size=len(v1)))
    return v1, v2
