from vector2d import Vector2d
from atom import Atom, BLUE
from event import Event
import screen_settings

class Box:
    # Характеристики ящика
    def __init__(self, size: Vector2d):
        # Параметры ящика
        self.size = size
        self.borders = [
            Border(Vector2d(10, None), Vector2d(0, None)),        # левый
            Border(Vector2d(size.x, None), Vector2d(0, None)),   # правый
            Border(Vector2d(None, 0), Vector2d(None, 0)),        # верхний
            Border(Vector2d(None, size.y), Vector2d(None, 0)),   # нижний
        ]

    def collide(self, a: Atom, cur_time) -> list:
        events = []
        #  по горизонтали
        if a.velocity.x < 0:
            time = (self.borders[0].position.x-a.position.x+Atom.r) / a.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.borders[0].velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[0], time + cur_time, v, self.borders[0].velocity))
        elif a.velocity.x > 0:
            time = (self.borders[1].position.x - a.position.x) / a.velocity.x
            v = Vector2d(-a.velocity.x + 2 * self.borders[1].velocity.x, a.velocity.y)
            events.append(Event(a, self.borders[1], time + cur_time, v, self.borders[1].velocity))
        #  по вертикали
        if a.velocity.y < 0:
            time = (self.borders[2].position.y - a.position.y+Atom.r) / a.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.borders[2].velocity.y)
            events.append(Event(a, self.borders[2], time + cur_time, v, self.borders[2].velocity))
        elif a.velocity.y > 0:
            time = (self.borders[3].position.y - a.position.y) / a.velocity.y
            v = Vector2d(a.velocity.x, -a.velocity.y + 2 * self.borders[3].velocity.y)
            events.append(Event(a, self.borders[3], time + cur_time, v, self.borders[3].velocity))
        return events
                # Атом врезался в стенку


class Border():
    def __init__(self, pos: Vector2d, v: Vector2d):
        self.position = pos
        self.velocity = v
            # Стенка / Поршень

    def move(self):
        if self.velocity.x is not None:
            if self.position.x >= screen_settings.width or self.position.x < 0:
                self.velocity.x *= -1
            self.position.x += self.velocity.x
        else:
            if self.position.y >= screen_settings.height + Atom.r:
                self.velocity.y *= -1
            self.position.y += self.velocity.y
