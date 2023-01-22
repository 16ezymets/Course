from math import atan, cos, sin, sqrt
import pygame

class Vector2d:
    def __init__(self, x: float, y: float):
        self.x = float(x) if x is not None else None
        self.y = float(y) if y is not None else None

    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Vector2d(self.x ** other, self.y ** other)

    def __mul__(self, other):
        if not isinstance(other, float):
            return NotImplemented
        return Vector2d(self.x * other, self.y * other)

    def __add__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return Vector2d(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return Vector2d(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return f"({self.x}, {self.y})"

'''
def atom_collide(a1, a2):
    a2.velocity.x = a2.velocity.x-a1.position.x
    a2.velocity.y = a2.velocity.y-a1.velocity.y
    D = (a2.position.x*a2.velocity.x - a2.position.y*a2.velocity.y)**2 -\
        ((a2.position.x-a1.position.x + a2.position.y-a1.position.y)**2)*(a2.velocity.x**2 - a2.velocity.y**2)
    if D > 0:
        t1 = (a2.position.x*a2.velocity.x - a2.position.y*a2.velocity.y +
              sqrt(D))/(a2.velocity.x**2 - a2.velocity.y**2)
        t2 = (a2.position.x*a2.velocity.x - a2.position.y*a2.velocity.y -
              sqrt(D))/(a2.velocity.x**2 - a2.velocity.y**2)
        assert(t1 > 0 and t2 > 0)
        t = min(t1, t2)
        if t < 0:
            t = None
            return t, D
        else:
            return t, D
    else:
        t = None
        return None, D
'''

class Atom:
    # Характеристики атома
    def __init__(self, position: Vector2d, velocity: Vector2d):
        self.position = position
        self.velocity = velocity

    def move(self, t: float):
        self.position += self.velocity * float(t)

    def collide(self, other, cur_time):
        if isinstance(other, Atom):
            a2x = other.velocity.x - self.velocity.x
            a2y = other.velocity.y - self.velocity.y
            D = (other.position.x * a2x - other.position.y * a2y) ** 2 - \
                ((other.position.x - self.position.x)**2 + (other.position.y - self.position.y)**2) *\
                (other.velocity.x ** 2 - other.velocity.y ** 2)
            if D > 0:
                t1 = (other.position.x * a2x - other.position.y * a2y +
                      sqrt(D)) / (a2x ** 2 - a2y ** 2)
                t2 = (other.position.x * a2x - other.position.y * a2y -
                      sqrt(D)) / (a2x ** 2 - a2y ** 2)
                #assert t1 > 0 and t2 > 0 or t1 < 0 and t2 < 0, 'Разные знаки у корней'
                t = min(t1, t2)
                if t == 0:
                    tm = TMatrix(self.position, other.position)
                    #  перейдем в систему отсчета столкновения
                    v1 = tm.trans(self.velocity)
                    v2 = tm.trans(other.velocity)
                    #  физика: динамика
                    v1.x, v2.x = v2.x, v1.x
                    #  вернемся в исходную систему отсчета
                    self.velocity = tm.back(v1)
                    other.velocity = tm.back(v2)
                    # время столкновения
                    return self.velocity, other.velocity
                elif t > 0:
                    e = Event(self, other, t, self.velocity, other.velocity)
                    return e
                else:
                    return None
            else:
                return None
            # return Event or None
        else:
            return NotImplemented


class Box:
    # Характеристики ящика
    def __init__(self, size: Vector2d):
        self.size = size
        self.borders = [
            Border(Vector2d(0, None), Vector2d(0, 0)),
            Border(Vector2d(size.x, None), Vector2d(0, 0)),
            Border(Vector2d(None, 0), Vector2d(0, 0)),
            Border(Vector2d(None, size.y), Vector2d(0, 0)),
        ]
                # Параметры ящика

    def collide(self, a:Atom, cur_time) -> list:
        events = []
        # по горизонтали
        if a.velocity.x < 0:
            time = -a.position.x / a.velocity.x
            v = Vector2d(-a.velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[0], time + cur_time, v, 0))
        elif a.velocity.x > 0:
            time = (self.size.x - a.position.x) / a.velocity.x
            v = Vector2d(-a.velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[1], time + cur_time, v, 0))
        # по вертикали
        if a.velocity.y < 0:
            time = -a.position.y / a.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y)
            events.append(Event(a, self.borders[2], time + cur_time, v, 0))
        elif a.velocity.y > 0:
            time = (self.size.y - a.position.y) / a.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y)
            events.append(Event(a, self.borders[3], time + cur_time, v, 0))
        return events
                # Атом врезался в стенку



class Border:
    def __init__(self, pos: Vector2d, v: Vector2d):
        self.position = pos
        self.velocity = v
            # Стенка


class Event:
    def __init__(self, obj1, obj2, collision_time, v1, v2):
        self.obj1: Atom = obj1
        self.obj2: (Atom | Border) = obj2
        self.time = collision_time
        self.newv1 = v1
        self.newv2 = v2
            # Событие между двумя объектами и их новые скорости


class TMatrix:
    def __init__(self, pos1, pos2):
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y
        phi = atan(dx/dy) if dy else 0
        assert(isinstance(phi, float))
        self.a11 = self.a22 = cos(phi)
        self.a21 = sin(phi)
        self.a12 = -sin(phi)

    def trans(self, v):
        x = v.x * self.a11 + v.y * self.a12
        y = v.x * self.a21 + v.y * self.a22
        return Vector2d(x, y)

    def back(self, v):
        x = v.x * self.a11 + v.y * self.a21
        y = v.x * self.a12 + v.y * self.a22
        return Vector2d(x, y)

