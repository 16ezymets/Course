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

    def collide(self, a: Atom, cur_time: float) -> list:
        # найдем все 4 столкновения (возможно, с Null-ами)
        ev = [b.collide(a, cur_time) for b in self.borders]
        # добавим в список лучшее из них по горизонтали и вертикали
        events = []
        Box.add_best(events, ev[0], ev[1], cur_time)
        Box.add_best(events, ev[2], ev[3], cur_time)
        return events

    @staticmethod
    def add_best(events: list[Event], e1: Event, e2: Event, cur_time):
        if e1 and e2:
            events.append(e1 if (e1.time > e2.time) else e2)
        elif e1:
            events.append(e1)
        elif e2:
            events.append(e2)
        else:
            assert (not e1.obj1.velocity.x) or (not e2.obj1.velocity.y)  # if atom speed is 0, nothing appends
        if events[-1].time < cur_time:
            events[-1].time = cur_time

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

    def collide(self, a: Atom, cur_time: float) -> Event:
        assert((self.position.x is None) or (self.position.y is None))
        if self.position.x is not None:  # по горизонтали
            dist = a.position.x - self.position.x
            speed = a.velocity.x - self.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.velocity.x, a.velocity.y)
        else:                            # по вертикали
            assert(self.position.y is not None)
            dist = a.position.y - self.position.y if self.position.y else a.position.y - ATOM_R  # чтобы атом не залезал на title
            speed = a.velocity.y - self.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.velocity.y)

        if speed != 0:
            time = - dist / speed
            return Event(a, self, time + cur_time, v, self.velocity)
        return None
