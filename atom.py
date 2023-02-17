from vector2d import Vector2d
from tmatrix import TMatrix
from event import Event


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 64, 64)


class Atom:
    r: int | float   # радиус атома

    def __init__(self, position: Vector2d, velocity: Vector2d, color):
        self.position = position
        self.velocity = velocity
        self.color = color

    def move(self, t: float):
        self.position += self.velocity * float(t)

    def collide(self, other, cur_time):
        assert(self.r > 0)
        if isinstance(other, Atom):
            x = other.position.x - self.position.x
            y = other.position.y - self.position.y
            vx = other.velocity.x - self.velocity.x
            vy = other.velocity.y - self.velocity.y
            a = vx ** 2 + vy ** 2
            b = 2 * (x * vx + y * vy)
            c = (x**2 + y**2) - (2*self.r)**2
            d = b*b - 4*a*c
            if d > 0:
                d_sqrt = d ** 0.5
                _t1 = (-b - d_sqrt) / (2 * a)
                _t2 = (-b + d_sqrt) / (2 * a)
                t1 = round(_t1, 10)
                t2 = round(_t2, 10)
                #assert(t1 * t2 > 0)
                if t1 * t2 > 0:
                    t = min(t1, t2)
                else:
                    t = t1 if abs(t1) > abs(t2) else t2
                if t > 0:
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
                    newv1 = tm.back(v1)
                    newv2 = tm.back(v2)
                    #  создаем событие
                    e = Event(self, other, cur_time+t, newv1, newv2)
                    return e
                return None
            return None
        return NotImplemented
