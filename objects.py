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
        if not isinstance(other, float|int):
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

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def dist_2(self, other):
        return (other.x-self.x)**2 +(other.y-self.y)**2


class Atom:
    r = 0
    # Характеристики атома

    def __init__(self, position: Vector2d, velocity: Vector2d):
        self.position = position
        self.velocity = velocity

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
                t1 = (-b - d_sqrt) / (2 * a)
                t2 = (-b + d_sqrt) / (2 * a)
                #assert(t1 * t2 >= 0)
                t = min(t1, t2)
                if t > 0:
                    #  матрица перехода между системами отсчёта
                    tm = TMatrix(self.position, other.position)
                    #  перейдем в систему отсчета столкновения
                    v1 = tm.trans(self.velocity)
                    v2 = tm.trans(other.velocity)
                    #  физика: динамика
                    v1.x, v2.x = v2.x, v1.x
                    #  вернемся в исходную систему отсчета
                    newv1 = tm.back(v1)
                    newv2 = tm.back(v2)
                    #  создаем событие
                    e = Event(self, other, cur_time+t, newv1, newv2)
                    return e
                else:
                    return None
            else:
                return None
        else:
            return NotImplemented


class Box:
    # Характеристики ящика
    def __init__(self, size: Vector2d):
        # Параметры ящика
        self.size = size
        self.borders = [
            Border(Vector2d(0, None), Vector2d(0, 0)),       # левый
            Border(Vector2d(size.x, None), Vector2d(0, 0)),  # правый
            Border(Vector2d(None, 0), Vector2d(0, 0)),       # нижний
            Border(Vector2d(None, size.y), Vector2d(0, 0)),  # верхний
        ]

    def collide(self, a: Atom, cur_time) -> list:
        events = []
        #  по горизонтали
        if a.velocity.x < 0:
            time = (-a.position.x+Atom.r) / a.velocity.x
            v = Vector2d(-a.velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[0], time + cur_time, v, 0))
        elif a.velocity.x > 0:
            time = (self.size.x - a.position.x) / a.velocity.x
            v = Vector2d(-a.velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[1], time + cur_time, v, 0))
        #  по вертикали
        if a.velocity.y < 0:
            time = (-a.position.y+Atom.r) / a.velocity.y
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

