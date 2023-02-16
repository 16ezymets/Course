from math import sin, atan, cos
from vector2d import Vector2d


class TMatrix:
    def __init__(self, pos1, pos2):
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y
        phi = atan(dy/dx) if dx else 0.0
        assert(isinstance(phi, float))
        self.a11 = self.a22 = sin(phi)
        self.a21 = cos(phi)
        self.a12 = -cos(phi)

    def trans(self, v):
        x = v.x * self.a11 + v.y * self.a12
        y = v.x * self.a21 + v.y * self.a22
        return Vector2d(x, y)

    def back(self, v):
        x = v.x * self.a11 + v.y * self.a21
        y = v.x * self.a12 + v.y * self.a22
        return Vector2d(x, y)
