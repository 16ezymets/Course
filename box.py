from vector2d import Vector2d
from atom import Atom
from event import Event


class Box:
    # Характеристики ящика
    def __init__(self, size: Vector2d):
        # Параметры ящика
        self.size = size
        self.borders = [
            Border(Vector2d(0, None), Vector2d(0, None)),        # левый
            Border(Vector2d(size.x, None), Vector2d(0, None)),   # правый
            Border(Vector2d(None, 0), Vector2d(None, 0)),        # верхний
            Border(Vector2d(None, size.y), Vector2d(None, 0)),   # нижний
        ]

    def collide(self, a: Atom, cur_time) -> list:
        events = []
        #  по горизонтали
        if a.velocity.x < 0:
            time = (-a.position.x+Atom.r) / a.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.borders[0].velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[0], time + cur_time, v, Vector2d(0, 0)))
        elif a.velocity.x > 0:
            time = (self.size.x - a.position.x) / a.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.borders[1].velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[1], time + cur_time, v, Vector2d(0, 0)))
        #  по вертикали
        if a.velocity.y < 0:
            time = (-a.position.y+Atom.r) / a.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.borders[2].velocity.y)
            events.append(Event(a, self.borders[2], time + cur_time, v, Vector2d(0, 0)))
        elif a.velocity.y > 0:
            time = (self.size.y - a.position.y) / a.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.borders[3].velocity.y)
            events.append(Event(a, self.borders[3], time + cur_time, v, Vector2d(0, 0)))
        return events
                # Атом врезался в стенку


class Border:
    def __init__(self, pos: Vector2d, v: Vector2d):
        self.position = pos
        self.velocity = v
            # Стенка
