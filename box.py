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

    def collide(self, a: Atom, cur_time: float) -> list:
        events = []
        for b in self.borders:
            events += b.collide(a, cur_time)
        return events

    def move_borders(self, timestep):
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

    def collide(self, a: Atom, cur_time: float) -> list:
        if self.position.x is not None:
            assert(self.position.y is None)
            #  по горизонтали
            dist = a.position.x - self.position.x
            #dist = (dist - Atom.r) if dist > 0 else (dist + Atom.r)
            speed = a.velocity.x - self.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.velocity.x, a.velocity.y)
        else:
            assert(self.position.y is not None)
            #  по вертикали
            dist = a.position.y - self.position.y
            #dist = (dist - Atom.r) if dist > 0 else (dist + Atom.r)
            speed = a.velocity.y - self.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.velocity.y)

        #if (dist > 0 and speed < 0) or (dist < 0 and speed > 0):
        if dist * speed < 0:
            time = - dist / speed
            return [Event(a, self, time + cur_time, v, self.velocity)]
        return []
