from cython import cclass, ccall, address, cast, size_t
from cython.cimports.vector import (
    InternalVectorF64,
    vectorlib_add,
    vectorlib_resize,
)


@cclass
class VectorF64(InternalVectorF64):
    def __iadd__(self, other: InternalVectorF64):
        vectorlib_add(address(self.v), address(other.v))
        return self

    def __len__(self):
        return cast(int, self.v.length)

    @ccall
    def from_list(self, new_value: list[float]):
        n: size_t = cast(size_t, len(new_value))
        vectorlib_resize(address(self.v), n)
        for i, x in enumerate(new_value):
            self.v.data[i] = x

    @ccall
    def into_list(self) -> list[float]:
        n: size_t = self.v.length
        res: list[float] = [0 for _ in range(n)]
        for i in range(n):
            res[i] = cast(float, self.v.data[i])
        return res
