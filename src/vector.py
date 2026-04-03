from collections.abc import Generator

from cython import cclass, ccall, address, cast, size_t
from cython.cimports.vector import (
    InternalVectorF64,
    vectorlib_add,
    vectorlib_sub,
    vectorlib_mul,
)


@cclass
class VectorF64(InternalVectorF64):
    def __len__(self) -> int:
        return cast(int, self.v.length)

    def __iter__(self) -> Generator[float]:
        for i in range(len(self)):
            yield self.v.data[cast(size_t, i)]

    @ccall
    def into_list(self) -> list[float]:
        return list(self)

    def __add__(self, other: InternalVectorF64):
        res: VectorF64 = type(self)(len(self))
        vectorlib_add(address(res.v), address(self.v), address(other.v))
        return res

    def __sub__(self, other: InternalVectorF64):
        res: VectorF64 = type(self)(len(self))
        vectorlib_sub(address(res.v), address(self.v), address(other.v))
        return res

    def __mul__(self, other: InternalVectorF64):
        res: VectorF64 = type(self)(len(self))
        vectorlib_mul(address(res.v), address(self.v), address(other.v))
        return res
