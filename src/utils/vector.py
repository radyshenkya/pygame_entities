import math
from typing import Union

from utils.math import lerp


class Vector2:
    def __init__(self, x=0.0, y=0.0) -> None:
        self.x = x
        self.y = y

    def get_tuple(self):
        return (self.x, self.y)

    def get_integer_tuple(self):
        return (int(self.x), int(self.y))

    def __add__(self, other: "Vector2"):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2"):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union[int, float]):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: Union[int, float]):
        return Vector2(self.x / other, self.y / other)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self) -> "Vector2":
        magnitude = self.magnitude()

        if magnitude == 0:
            return Vector2(0, 0)

        return Vector2(self.x / magnitude, self.y / magnitude)

    def lerp(a: "Vector2", b: "Vector2", t: float) -> "Vector2":
        return Vector2(lerp(a.x, b.x, t), lerp(a.y, b.y, t))

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
