from vector2d import Vector2d
from tmatrix import TMatrix
from event import Event
from settings import *


class Atom:
    r: int = ATOM_R   # радиус атома
    m: float = ATOM_M   # масса атома

    def __init__(self, position: Vector2d, velocity: Vector2d, color):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.mass = self.m

    def __repr__(a):
        return f"{a.position=}, {a.velocity=}"

    def move(self, timestep):
        self.position.x += self.velocity.x * timestep
        self.position.y += self.velocity.y * timestep

    def collide(self, other, cur_time):
        # assert(self.r > 0)
        # if not isinstance(other, Atom):
        #    return NotImplemented
        x = other.position.x - self.position.x
        y = other.position.y - self.position.y
        vx = other.velocity.x - self.velocity.x
        vy = other.velocity.y - self.velocity.y
        #  ранняя отсечка
        # if x*vx > 0 or y * vy > 0:
        #    return None
        a = vx ** 2 + vy ** 2
        b = 2 * (x * vx + y * vy)
        c = (x**2 + y**2) - (2*self.r)**2
        d = b*b - 4*a*c
        if d <= 0:  # нет столкновения
            return None
        d_sqrt = d ** 0.5
        _t1 = (-b - d_sqrt) / (2 * a)
        _t2 = (-b + d_sqrt) / (2 * a)
        t1 = round(_t1, 10)
        t2 = round(_t2, 10)
        # assert(t1 * t2 > 0)
        if t1 * t2 > 0:
            t = min(t1, t2)
        else:
            t = t1 if abs(t1) > abs(t2) else t2
        if t <= 0:  # нет столкновения в будущем
            return None
        #  матрица перехода между системами отсчёта
        pos1 = self.position + self.velocity * t
        pos2 = other.position + other.velocity * t
        tm = TMatrix(pos1, pos2)
        #  перейдем в систему отсчета столкновения
        v1 = tm.trans(self.velocity)
        v2 = tm.trans(other.velocity)
        #  физика: динамика
        v1.x, v2.x = v2.x, v1.x
        #  вернёмся в исходную систему отсчёта
        new_v1 = tm.back(v1)
        new_v2 = tm.back(v2)
        #  создаем событие
        e = Event(self, other, cur_time+t, new_v1, new_v2)
        return e
