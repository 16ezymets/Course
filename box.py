from vector2d import Vector2d
from event import Event
from atom import Atom
from settings import *


class Box:
    # Характеристики ящика
    def __init__(self, size: Vector2d):
        # Параметры ящика
        self.size = size
        self.borders = [
            Border(Vector2d(0, None), Vector2d(BOX_SPEED, 0)),       # левый
            Border(Vector2d(size.x, None), Vector2d(0, 0)),   # правый
            Border(Vector2d(None, 0), Vector2d(0, 0)),        # верхний
            Border(Vector2d(None, size.y), Vector2d(0, 0)),   # нижний
        ]

    def space_width(self):
        return self.borders[1].position.x - self.borders[0].position.x

    def space_height(self):
        return self.borders[3].position.y - self.borders[2].position.y

    def volume(self):
        return self.space_width() * self.space_height()

    def center(self):
        return Vector2d((self.borders[0].position.x + self.borders[1].position.x) / 2,
                        (self.borders[2].position.y + self.borders[3].position.y) / 2)

    def collide(self, a: Atom, cur_time: float) -> list:
        center = self.center()
        # найдем все 4 столкновения (возможно, с Null-ами)
        ev = [b.collide(a, cur_time, center) for b in self.borders]
        # добавим в список только корректные события (по одному по горизонтали и вертикали)
        events = [e for e in ev if e]
        return events

    def move(self, timestep):
        for b in self.borders:
            b.move(timestep)


class Border:
    def __init__(self, pos: Vector2d, v: Vector2d):
        self.position = pos
        self.velocity = v

    def move(self, timestep):
        if self.position.x is not None:
            self.position.x += self.velocity.x * timestep
        if self.position.y is not None:
            self.position.y += self.velocity.y * timestep

    def collide(self, a: Atom, cur_time: float, center: Vector2d) -> Event:
        assert((self.position.x is None) or (self.position.y is None))
        if self.position.y is None:     # вертикальная стенка
            assert (self.position.x is not None)
            dist = a.position.x - self.position.x
            speed = a.velocity.x - self.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.velocity.x, a.velocity.y)
            #  если атом движется (относительно стенки) не от центра, то это "неправильное" столкновение
            if speed * (self.position.x - center.x) < 0:
                speed = 0
        else:                           # горизонтальная стенка
            assert(self.position.y is not None)
            if not self.position.y:
                dist = a.position.y - ATOM_R
            else:
                dist = a.position.y - self.position.y
            speed = a.velocity.y - self.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.velocity.y)
            #  если атом движется (относительно стенки) не от центра, то это "неправильное" столкновение
            if speed * (self.position.y - center.y) < 0:
                speed = 0

        if speed != 0:
            time = - dist / speed
            return Event(a, self, time + cur_time, v, self.velocity)
        return None
