import struct
import sys

from numpy import double, float64


# 字节长度函数
def size_of_type(typ):
    return struct.calcsize(typ, 0)


i: int = 214748364
f: float = 3.12132134e+38
d: float64 = 100000 / 3
b: bool = False
print(sys.getsizeof(i))

print(sys.getsizeof(f))

print(sys.getsizeof(d))

print(sys.getsizeof(b))

