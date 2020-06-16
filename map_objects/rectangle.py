from typing import Tuple


class Rect:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other) -> bool:
        """Returns true if this rectangle intersects with other"""
        return (self.x1 <= other.x2 and self.x2 >= other.x2 and
                self.y1 <= other.y2 and self.y2 >= other.y1)