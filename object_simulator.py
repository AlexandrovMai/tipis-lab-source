import math
import matplotlib.pyplot as plt
import numpy as np


class Mes:
    def __init__(self, t, h, v, a):
        self.t = t
        self.h = h
        self.v = v
        self.a = a

    def __str__(self):
        return "At time: " + str(self.t) + " s [altitude: " + str(self.h) + " m, speed: " + str(self.v) + " m/s] " + \
                "acceleration: " + str(self.a) + " m/s2"


class FlyingObject:
    def __init__(self, oem):
        self.oem = oem
        self.K = 0
        self.L = 0
        self.h_current = 0
        self.h_last = 0
        self.v_current = 0
        self.v_last = 0
        self.i: int = 0
        self.dt = .01
        self.tc = 0

    def calc_acceleration(self, hc):
        return self.oem.get_a(hc)

    def speed_counter_iteration(self):
        v = self.v_last + (self.calc_acceleration(self.h_last) +
                   3 * self.calc_acceleration(2 / 3 * self.h_last + 1 / 3 * self.h_current) +
                   3 * self.calc_acceleration(1 / 3 * self.h_last + 2 / 3 * self.h_current) +
                   self.calc_acceleration(self.h_current)
                   ) / 8 * self.dt

        self.v_last, self.v_current = self.v_current, v

    def height_counter_iteration(self):
        h = self.h_last + (self.v_last +
                   3 * (2 / 3 * self.v_last + 1 / 3 * self.v_current) +
                   3 * (1 / 3 * self.v_last + 2 / 3 * self.v_current) +
                   self.v_current
                   ) / 8 * self.dt

        self.h_last, self.h_current = self.h_current, h

    def __iter__(self):
        return self

    def __next__(self):
        self.speed_counter_iteration()
        self.height_counter_iteration()
        self.i += 1
        self.tc += self.dt
        return Mes(self.tc, self.h_current, self.v_current, self.calc_acceleration(self.h_current)), self.i

    def get_balloons(self):
        return self.oem.get_balloons()

    def get_mass(self):
        return self.oem.get_mass()


class ObjectEmulator:
    sigma = 1200

    def __init__(self):
        self.m_stud = 0
        self.m_chair = 0
        self.m_balloon = 0
        self.balloon_counts = 0
        self.balloon_v = 0
        self._balloon_counts_current = 0
        self.ro_balloon = 0
        self.h_critical = 0
        self._h_dest_max = 0

    def balloon_gaussian(self, h):
        if h > self._h_dest_max:
            self._balloon_counts_current = self._balloon_counts_current - self.balloon_counts * (math.exp(
                                        -0.5 * ((h - self.h_critical) / self.sigma) ** 2
                                        ) / self.sigma / math.sqrt(2 * math.pi))
            self._h_dest_max = h

    def set_balloon_count(self, bc):
        self._balloon_counts_current = bc
        self.balloon_counts = bc

    def get_balloons(self):
        return self._balloon_counts_current

    def get_air_ro(self, h):
        return .99988382 ** h

    def get_mass(self):
        return (self.ro_balloon * self.balloon_v + self.m_balloon) * self._balloon_counts_current + self.m_stud + self.m_chair

    def get_a(self, h):
        self.balloon_gaussian(h)
        m = self.get_mass()
        ap = self.get_air_ro(h)
        return self.balloon_v * self._balloon_counts_current * 9.81 * ap / m - 9.81


class ObjectWithConstants:
    def __init__(self):
        self.m_stud = 0
        self.m_chair = 0
        self.m_balloon = 0
        self.balloon_counts = 0
        self.balloon_v = 0
        self.ro_balloon = 0
        self.h_critical = 0
        self.ob_name = ""

    def create_object_emulator(self) -> ObjectEmulator:
        oe = ObjectEmulator()
        oe.m_stud = self.m_stud
        oe.m_chair = self.m_chair
        oe.m_balloon = self.m_balloon
        oe.set_balloon_count(self.balloon_counts)
        oe.balloon_v = self.balloon_v
        oe.ro_balloon = self.ro_balloon
        oe.h_critical = self.h_critical
        return oe


if __name__ == '__main__':
    ob = ObjectEmulator()
    ob.set_balloon_count(345)
    ob.m_balloon = 0.003
    ob.balloon_v = 0.425
    ob.ro_balloon = 0.17846
    ob.h_critical = 3000
    ob.m_chair = 2
    ob.m_stud = 62
    plt.figure(figsize=(16, 10))
    time_arr = []
    a_arr = []
    v_arr = []
    h_arr = []
    b_cnt = []
    m_arr = []
    fo = FlyingObject(ob)

    for a, b in fo:
        if b % 100 == 0:
            time_arr.append(a.t)
            v_arr.append(a.v)
            h_arr.append(a.h)
            a_arr.append(a.a)
            b_cnt.append(fo.get_balloons())
            m_arr.append(fo.get_mass())
        if b == 280000 or a.h <= 0.0:
            break

