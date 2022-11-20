def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b


def clamp(x, minimum, maximum):
    return min(max(x, minimum), maximum)
