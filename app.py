import random
from box import Box
from atom import *
from sorted_merge import *


#  параметры газа
Atom.r = 0.4
ATOM_COUNT = 1000
#Atom.r = 5
#ATOM_COUNT = 300
Atom.r = 16
ATOM_COUNT = 200

MAX_SPEED = 200
RED_PART = 20

#  параметры бокса (экрана)
WIDTH = 1200
HEIGHT = 800


class App:
    def __init__(self):
        self.box = Box(Vector2d(WIDTH, HEIGHT))
        self.events: list[Event] = []
        self.cur_time = 0
        self.atoms = App.create_atoms()
        self.events = self.calc_all_collisions()

    @staticmethod
    def create_atoms() -> list[Atom]:
        d2 = (2*Atom.r)**2
        atoms = []

        def is_bad_pos(_x: int, _y: int, _atoms: list[Atom]) -> bool:
            #  проверка наложения точки (x, y) с каким-то из уже имеющихся атомов
            for a in _atoms:
                if a.position.dist_2_xy(_x, _y) < d2:
                    return True
            return False

        for _ in range(ATOM_COUNT):
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            while is_bad_pos(x, y, atoms):
                x = random.randint(0, WIDTH - 1)
                y = random.randint(0, HEIGHT - 1)
            vx = random.randint(-MAX_SPEED, MAX_SPEED)
            vy = random.randint(-MAX_SPEED, MAX_SPEED)
            color = RED if random.randint(0, RED_PART) == 0 else WHITE
            atom = Atom(Vector2d(x, y), Vector2d(vx, vy), color)
            atoms.append(atom)
        return atoms

    def run(self, timestep: float):
        # рассчет кадра через timestep
        assert(len(self.events) > 0)
        e: Event = self.events[0]
        end_step_time = self.cur_time + timestep
        #  count of moves on timestep (for stat only)
        self.move_count = 0
        while end_step_time > self.cur_time:
            self.move_count += 1
            if e.time > self.cur_time + timestep:
                for a in self.atoms:
                    a.move(timestep)
                self.cur_time += timestep
                break
            else:
                for a in self.atoms:
                    a.move(e.time - self.cur_time)
                e.obj1.velocity = e.newv1
                e.obj2.velocity = e.newv2
                self.cur_time = e.time
                self.cleanup(e.obj1)
                self.cleanup(e.obj2)
                events1 = self.calc_collisions(e.obj1)
                events2 = self.calc_collisions(e.obj2)
                add = sorted_merge(events1, events2)
                self.events = sorted_merge(self.events, add)
                assert (len(self.events) > 0)
                e = self.events[0]

    def hot_stat(self):
        e = 0
        px = 0
        py = 0
        for a in self.atoms:
            e += a.velocity.x**2 + a.velocity.y**2
            px += a.velocity.x
            py += a.velocity.y
        e = round(e, 2)
        px = round(px, 2)
        py = round(py, 2)
        cnt = len(self.events)
        return [f"Moves for step: {self.move_count:02}",
                f"Total energy: {e}",
                f"X-impulse: {px}",
                f"Y-impulse: {py}",
                f"Events_count: {cnt}"]

    def calc_all_collisions(self):
        # Подсчет всех будущих столкновений атомов и сортировка по времени
        events: list[Event] = []
        for i in range(len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                e = self.atoms[i].collide(self.atoms[j], self.cur_time)
                if e:
                    events.append(e)
            events += self.box.collide(self.atoms[i], self.cur_time)
        events.sort(key=lambda e: e.time)
        return events

    def calc_collisions(self, a):
        # Подсчет столновений атома с другими атомами и сортировка по времени
        events: list[Event] = []
        if isinstance(a, Atom):
            for b in self.atoms:
                if a != b:
                    e = a.collide(b, self.cur_time)
                    if e:
                        events.append(e)
            events += self.box.collide(a, self.cur_time)
        events.sort(key=lambda el: el.time)
        return events

    def cleanup(self, obj) -> None:
        # Очистка всех событий, связанных с определенным атомом
        if isinstance(obj, Atom):
            self.events = [e for e in self.events if e.obj1 != obj and e.obj2 != obj]

