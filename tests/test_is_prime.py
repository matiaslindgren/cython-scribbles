import pytest
from pathlib import Path

from is_prime import is_prime


@pytest.fixture
def primes() -> list[int]:
    with open(Path(__file__).parent / "primes.txt") as f:
        lines = (line.strip() for line in f)
        return [int(x) for x in lines if x]


def test_is_prime(primes: list[int]) -> None:
    assert len(primes) >= 1000
    for x in primes:
        assert is_prime(x)


def test_is_not_prime(primes: list[int]) -> None:
    not_primes = sorted(set(range(-100, primes[-1])) - set(primes))
    assert len(not_primes) >= 1000
    for x in not_primes:
        assert not is_prime(x)
