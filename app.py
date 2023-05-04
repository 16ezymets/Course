import random
from box import Box
from atom import *
from sorted_merge import *
from settings import *


class App:
    def __init__(self):
        self.box = Box(Vector2d(WIDTH, HEIGHT))
        self.events: list[Event] = []
        self.cur_time = 0
        self.atoms = App.create_atoms()
        self.events = self.calc_all_collisions()
        self.impulse_diff = [[0, 0, 0, 0] for _ in range(STAT_MOVE_COUNT)]

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

    def step(self, timestep: float):
        # рассчет кадра через timestep
        assert(len(self.events) > 0)
        e: Event = self.events[0]
        end_step_time = self.cur_time + timestep
        #  count of moves on timestep (for stat only)
        self.move_count = 0
        impulse_diff = [0, 0, 0, 0]
        while end_step_time > self.cur_time:
            self.move_count += 1
            if e.time > self.cur_time + timestep:
                self.move(timestep)
                self.cur_time += timestep
                break
            else:
                self.move(e.time - self.cur_time)
                if e.obj2 == self.box.borders[0]:
                    impulse_diff[0] += (e.newv1.x - e.obj1.velocity.x) * e.obj1.m
                if e.obj2 == self.box.borders[1]:
                    impulse_diff[1] += (e.obj1.velocity.x - e.newv1.x) * e.obj1.m
                if e.obj2 == self.box.borders[2]:
                    impulse_diff[2] += (e.newv1.y - e.obj1.velocity.y) * e.obj1.m
                if e.obj2 == self.box.borders[3]:
                    impulse_diff[3] += (e.obj1.velocity.y - e.newv1.y) * e.obj1.m
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
        self.impulse_diff.pop(0)
        self.impulse_diff.append([impulse_diff[0] / timestep, impulse_diff[1] / timestep, impulse_diff[2] / timestep, impulse_diff[3] / timestep])

    def move(self, timestep):
        for a in self.atoms:
            a.move(timestep)
        self.box.move(timestep)

    def hot_stat(self):
        e = 0
        px = 0
        py = 0
        for a in self.atoms:
            e += a.velocity.x**2 + a.velocity.y**2
            px += a.velocity.x
            py += a.velocity.y
        e = round(e / len(self.atoms) / 2, 2)
        px = round(px, 2)
        py = round(py, 2)
        cnt = len(self.events)
        left_pressure = sum(diff[0] for diff in self.impulse_diff) / (self.box.space_height() * SCALE * DEPTH)
        right_pressure = sum(diff[1] for diff in self.impulse_diff) / (self.box.space_height() * SCALE * DEPTH)
        top_pressure = sum(diff[2] for diff in self.impulse_diff) / (self.box.space_width() * SCALE * DEPTH)
        bottom_pressure = sum(diff[3] for diff in self.impulse_diff) / (self.box.space_width() * SCALE * DEPTH)
        return [f"Moves for step: {self.move_count:02}",
                f"Total energy: {e}",
                f"X-impulse: {px}",
                f"Y-impulse: {py}",
                f"Events_count: {cnt}",
                f"Left Pressure: {left_pressure}",
                f"Right Pressure: {right_pressure}",
                f"Top Pressure: {top_pressure}",
                f"Bottom Pressure: {bottom_pressure}"]

    def calc_all_collisions(self):
        # Подсчет всех будущих столкновений атомов и сортировка по времени
        events: list[Event] = []
        for i in range(len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                e = self.atoms[i].collide(self.atoms[j], self.cur_time)
                if e:
                    events.append(e)
            events += self.box.collide(self.atoms[i], self.cur_time)
        events.sort(key=lambda el: el.time)
        return events

    def calc_collisions(self, a) -> list:
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

