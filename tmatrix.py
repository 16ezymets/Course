from math import atan, cos, sin, pi
from vector2d import Vector2d


class TMatrix:
    def __init__(self, pos1, pos2):
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y
        phi = atan(dy/dx) if dx else pi/2
        assert isinstance(phi, float)
        self.a11 = self.a22 = cos(phi)
        self.a21 = -sin(phi)
        self.a12 = sin(phi)

    def trans(self, v):
        x = v.x * self.a11 + v.y * self.a12
        y = v.x * self.a21 + v.y * self.a22
        return Vector2d(x, y)

    def back(self, v):
        x = v.x * self.a11 + v.y * self.a21
        y = v.x * self.a12 + v.y * self.a22
        return Vector2d(x, y)

