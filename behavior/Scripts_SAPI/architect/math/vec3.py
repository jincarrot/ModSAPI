from mod.common.utils.mcmath import Vector3
import math

def vec(tup):
    return Vector3(tup)

def add(a, b):
    # type: (Vector3, Vector3) -> Vector3
    return a + b

def sub(a, b):
    # type: (Vector3, Vector3) -> Vector3
    return a - b

def mul(a, b):
    # type: (Vector3, float | int) -> Vector3
    return a * b

def div(a, b):
    # type: (Vector3, float | int) -> Vector3
    return a / b

def dot(a, b):
    # type: (Vector3, Vector3) -> float
    return a * b

def cross(a, b):
    # type: (Vector3, Vector3) -> Vector3
    return Vector3.Cross(a, b)

def modulo(a):
    # type: (Vector3) -> float
    return Vector3.Length(a)

def normalize(a):
    # type: (Vector3) -> Vector3
    return Vector3.Normalized(a)

def compare(a, b):
    # type: (Vector3, Vector3) -> float
    """
    Greater if a > b
    Less if a < b
    Equal if a == b
    """
    return Vector3.LengthSquared(a) - Vector3.LengthSquared(b)

def clamp(v, min, max):
    # type: (Vector3, float, float) -> Vector3
    lenSqrt = Vector3.LengthSquared(v)
    if lenSqrt > max * max:
        return v * (max / math.sqrt(lenSqrt))
    elif lenSqrt < min * min:
        return v * (min / math.sqrt(lenSqrt))

def lerp(a, b, t):
    # type: (Vector3, Vector3, float) -> Vector3
    return a * (1 - t) + b * t

def nlerp(a, b, t):
    # type: (Vector3, Vector3, float) -> Vector3
    """
    a和b应为单位向量，否则插值不经过起点和终点
    """
    return normalize(lerp(a, b, t))