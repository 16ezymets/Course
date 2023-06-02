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
        self.time = []
        self.press = []
        self.volume = []
        self.temperature = []
        self.data = [self.time, self.press, self.volume, self.temperature]

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
            x = random.randint(0, (WIDTH // SCALE) - 1)
            y = random.randint(0, (HEIGHT // SCALE) - 1)
            while is_bad_pos(x, y, atoms):
                x = random.randint(0, (WIDTH // SCALE) - 1)
                y = random.randint(0, (HEIGHT // SCALE) - 1)
            vx = random.randint(-MAX_SPEED, MAX_SPEED)
            vy = random.randint(-MAX_SPEED, MAX_SPEED)
            color = RED if random.randint(0, RED_PART) == 0 else WHITE
            atom = Atom(Vector2d(x, y), Vector2d(vx, vy), color)
            atoms.append(atom)
        return atoms

    def step(self, timestep: float) -> bool:
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
        return True if self.box.volume() > extreme_volume else False

    def move(self, timestep):
        for a in self.atoms:
            a.move(timestep)
        self.box.move(timestep)

    def hot_stat(self):
        e = 0
        a = 0
        px = 0
        py = 0
        for atom in self.atoms:
            e += atom.velocity.x**2 + atom.velocity.y**2
            px += atom.velocity.x
            py += atom.velocity.y
        e = round(e / len(self.atoms) / 2, 2)
        s = self.box.borders[0].position.x  # пройденное расстояние
        px = round(px, 2)
        py = round(py, 2)
        n = len(self.atoms)
        cnt = len(self.events)
        left_pressure = sum(diff[0] for diff in self.impulse_diff) / (self.box.space_height() * DEPTH)
        right_pressure = sum(diff[1] for diff in self.impulse_diff) / (self.box.space_height() * DEPTH)
        top_pressure = sum(diff[2] for diff in self.impulse_diff) / (self.box.space_width() * DEPTH)
        bottom_pressure = sum(diff[3] for diff in self.impulse_diff) / (self.box.space_width() * DEPTH)
        all_pressures = [left_pressure, right_pressure, top_pressure, bottom_pressure]
        a += left_pressure * s
        p1 = left_pressure
        # p v = nu r t
        # t = p * v / (n * K)
        t = (p1 * self.box.volume()) / (NA * K * n)
        p2 = (n * K * NA * t) / (self.box.volume())
        ie = K * t  # средняя энергия молекул
        de = e - a
        # stat
        self.time.append(self.cur_time)
        self.press.append(sum(all_pressures) / 4)
        self.volume.append(self.box.volume())
        self.temperature.append(t)
        return [f"Moves for step: {self.move_count:02}",
                f"Total energy: {e}",
                f"E(k): {ie}",
                f"Temperature (K): {t}",
                f"Piston work: {a}",
                f"{de}",
                f"X-impulse: {px}",
                f"Y-impulse: {py}",
                f"Events_count: {cnt}",
                f"NKT pressure: {p2}",
                f"Left pressure: {left_pressure}",
                f"Right pressure: {right_pressure}",
                f"Top pressure: {top_pressure}",
                f"Bottom pressure: {bottom_pressure}"]

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

