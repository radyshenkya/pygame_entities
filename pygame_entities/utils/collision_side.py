from pygame import Rect

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
ERROR_SIDE = 4


def check_side_x(a: Rect, b: Rect) -> int:
    if a.center[0] > b.center[0]:
        return RIGHT
    return LEFT


def check_side_y(a: Rect, b: Rect) -> int:
    if a.center[1] > b.center[1]:
        return DOWN
    return UP


def check_side(a: Rect, b: Rect) -> int:
    if abs(a.center[0] - b.center[0]) > abs(a.center[1] - b.center[1]):
        return check_side_x(a, b)
    return check_side_y(a, b)
