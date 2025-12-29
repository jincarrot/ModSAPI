def lerp(a, b, t):
    return a * (1 - t) + b * t

def clamp(x, min, max):
    return max if x > max else min if x < min else x

def smoothstep(edge0, edge1, x):
    # type: (float, float, float) -> float
    # https://en.wikipedia.org/wiki/Smoothstep
    # x in [edge0, edge1]
    t = clamp((x - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)