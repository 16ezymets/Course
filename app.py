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
        self.atoms: list[Atom] = []
        self.create_atoms()
        self.events = self.calc_all_collisions()
        self.impulse_diff = [[0, 0, 0, 0] for _ in range(STAT_MOVE_COUNT)]
        self.time = []
        self.press = []
        self.volume = []
        self.temperature = []
        self.pvt = []
        self.data = [self.time, self.press, self.volume, self.temperature]
        self.e_initial = None
        self.a = 0

    def create_atoms(self):
        d2 = (2*Atom.r)**2

        def is_bad_pos(_x: int, _y: int, _atoms: list[Atom]) -> bool:
            #  проверка наложения атома в позиции (x, y) с каким-то из уже имеющихся атомов
            for a in _atoms:
                if a.position.dist_2_xy(_x, _y) < d2:
                    return True
            return False

        for _ in range(ATOM_COUNT):
            x = random.random() * self.box.space_width()
            y = random.random() * self.box.space_height()
            while is_bad_pos(x, y, self.atoms):
                x = random.random() * self.box.space_width()
                y = random.random() * self.box.space_height()
            vx = (random.random()-0.5)*2*MAX_SPEED
            vy = (random.random()-0.5)*2*MAX_SPEED
            color = RED if random.randint(0, RED_PART) == 0 else WHITE
            atom = Atom(Vector2d(x, y), Vector2d(vx, vy), color)
            self.atoms.append(atom)

    def step(self, timestep: float) -> bool:
        # рассчет кадра через timestep
        assert len(self.events) > 0
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
                #assert e.time >= self.cur_time
                self.move(e.time - self.cur_time)
                if e.obj2 == self.box.borders[0]:
                    impulse_diff[0] += abs(e.newv1.x - e.obj1.velocity.x) * e.obj1.m
                if e.obj2 == self.box.borders[1]:
                    impulse_diff[1] += abs(e.obj1.velocity.x - e.newv1.x) * e.obj1.m
                if e.obj2 == self.box.borders[2]:
                    impulse_diff[2] += abs(e.newv1.y - e.obj1.velocity.y) * e.obj1.m
                if e.obj2 == self.box.borders[3]:
                    impulse_diff[3] += abs(e.obj1.velocity.y - e.newv1.y) * e.obj1.m
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
        self.impulse_diff.append([impulse_diff[0] / timestep,
                                  impulse_diff[1] / timestep,
                                  impulse_diff[2] / timestep,
                                  impulse_diff[3] / timestep])
        return True if self.box.volume() > extreme_volume else False

    def move(self, timestep):
        for a in self.atoms:
            a.move(timestep)
        self.box.move(timestep)

    def hot_stat(self, timestep):
        n = len(self.atoms)
        cnt = len(self.events)

        e_total = 0
        px = 0
        py = 0
        for atom in self.atoms:
            e_total += (atom.velocity.x ** 2 + atom.velocity.y ** 2)
            px += atom.velocity.x
            py += atom.velocity.y
        v_avr = (e_total / n) ** 0.5
        e_total *= Atom.m / 2
        p_avr = v_avr * Atom.m
        px *= Atom.m
        py *= Atom.m
        if self.e_initial is None:
            self.e_initial = e_total
        e_delta = e_total - self.e_initial
        e_avr = e_total / n
        T_kin = e_avr / K

        #  давление
        left_pressure = sum(diff[0] for diff in self.impulse_diff) / \
                        len(self.impulse_diff) / (self.box.space_height() * DEPTH)
        right_pressure = sum(diff[1] for diff in self.impulse_diff) / \
                         len(self.impulse_diff) / (self.box.space_height() * DEPTH)
        top_pressure = sum(diff[2] for diff in self.impulse_diff) / \
                       len(self.impulse_diff) / (self.box.space_width() * DEPTH)
        bottom_pressure = sum(diff[3] for diff in self.impulse_diff) / \
                          len(self.impulse_diff) / (self.box.space_width() * DEPTH)
        P_avr = (left_pressure + right_pressure + top_pressure + bottom_pressure) / 4

        #  PV/T = K * n
        PV_T = P_avr * self.box.volume() / T_kin
        Kn = K * n

        #  работа
        s = self.box.space_height() * DEPTH     #  площадь поршня
        ds = self.box.borders[0].velocity.x * timestep  # пройденное расстояние (за шаг)
        da = P_avr * s * ds
        self.a += da
        e_factor = e_delta / self.a if self.a else 0

        # p v = nu r T = n K T
        # T = P * V / (n * K)
        T = (P_avr * self.box.volume()) / Kn
        t_factor = T / T_kin

        # stat log
        self.time.append(self.cur_time)
        self.press.append(P_avr)
        self.volume.append(self.box.volume())
        self.temperature.append(T_kin)
        self.pvt.append(PV_T)

        return [
                f"V (avr): {round(v_avr)}",
                f"p (avr): {p_avr:8e}",
                f"px (total): {px:8e}",
                f"py (total): {py:8e}",
                "",
                f"E (initial): {self.e_initial:8e}",
                f"E (total): {e_total:8e}",
                f"E (total delta): {e_delta:8e}",
                f"A (piston work): {self.a:8e}",
                f"E (avr): {e_avr:8e}",
                f"T (kinetic): {round(T_kin)}",
                f"T (K): {round(T)}",
                "",
                f"PV/T: {PV_T:8e}",
                f"Kn: {Kn:8e}",
                "",
                f"PV/T / Kn: {PV_T / Kn:8f}",
                f"T / T_kin: {t_factor:8f}",
                f"dE / A: {e_factor:8f}",
                "",
                f"P (avr): {P_avr:4e}",
                "",
                # f"-Events_count: {cnt}",
                # "-Moves for step: {self.move_count:02}",
                ]

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

