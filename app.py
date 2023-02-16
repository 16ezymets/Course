
from objects import *
from func import *


class App:
    def __init__(self):
        self.events: list[Event] = []
        self.atoms = [
            Atom(Vector2d(40, 24), Vector2d(30, 30)),
            Atom(Vector2d(40, 404), Vector2d(30, 55)),
            Atom(Vector2d(99, 84), Vector2d(40, 70)),
            # Atom(Vector2d(33, 123), Vector2d(90, 55)),
            # Atom(Vector2d(111, 222), Vector2d(40, 30)),
            # Atom(Vector2d(23, 0), Vector2d(80, 55)),
        ]
        #print(f"v1:{self.atoms[0].velocity}  v2:{self.atoms[1].velocity} ")
        self.box = Box(Vector2d(900, 600))
        self.cur_time = 0
        self.events = self.calc_all_collisions()
            # Создание всех объектов
        #self.count = 0

    def run(self, timestep):
        assert(len(self.events) > 0)
        e: Event = self.events[0]
        endruntime = self.cur_time + timestep
        while endruntime > self.cur_time:
            if e.time > self.cur_time + timestep:
                #print('.', end='')
                #self.count += 1
                for a in self.atoms:
                    a.move(timestep)
                self.cur_time += timestep
                break
            else:
                #print('#')
                for a in self.atoms:
                    a.move(e.time - self.cur_time)
                e.obj1.velocity = e.newv1
                e.obj2.velocity = e.newv2
                #print(f"x: v1:{self.atoms[0].velocity}  v2:{self.atoms[1].velocity} ")
                self.cleanup(e.obj1)
                self.cleanup(e.obj2)
                self.cur_time = e.time
                events1 = self.calc_collisions(e.obj1)
                events2 = self.calc_collisions(e.obj2)
                add = sorted_merge(events1, events2)
                self.events = sorted_merge(self.events, add)
                assert (len(self.events) > 0)
                e = self.events[0]
                    # Рабочий процесс

    def calc_all_collisions(self):
        events: list[Event] = []
        for i in range(len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                e = self.atoms[i].collide(self.atoms[j], self.cur_time)
                if e:
                    events.append(e)
            events += self.box.collide(self.atoms[i], self.cur_time)
        events.sort(key=lambda e: e.time)
        return events
                # Подсчет всех будущих столкновений атомов и сортировка по времени

    def calc_collisions(self, a):
        events: list[Event] = []
        if isinstance(a, Atom):
            for b in self.atoms:
                if a != b:
                    e = a.collide(b, self.cur_time)
                    if e:
                        events.append(e)
            events += self.box.collide(a, self.cur_time)
        events.sort(key=lambda e: e.time)
        return events
                # Подсчет столновений атома с другими атомами и сортировка по времени

    def cleanup(self, obj) -> None:
        if isinstance(obj, Atom):
            self.events = [e for e in self.events if e.obj1 != obj and e.obj2 != obj]
            # Очистка всех событий, связанных с определенным атомом

#Основное приложение


