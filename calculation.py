import math


class Calculation:

    v_cialc = [0.0]

    t = 0
    h = []
    v = []
    a = []
    fuel_less = [0]

    def __init__(self, m_fuel: float, m_rocket: float, g: float, v_gas: float, height: float, allow_landing_v: float, dt: float, allow_max_dm: float):
        self.allow_max_dm = allow_max_dm
        self.dt = dt
        self.allow_landing_v = allow_landing_v
        self.h.append(height)
        self.v_gas = v_gas
        self.g = g
        self.m_rocket = m_rocket
        self.m0 = m_fuel+m_rocket
        self.m_fuel = m_fuel
        # вычисление начального ускорения методом Эйлера:
        self.a.append(self.accel(self.dt))
        self.v.append(self.a[-1]*self.dt)
        print(self.v)
        self.h.append(self.h[-1]+self.v[-1]*dt)
        print(self.h)
        self.t += self.dt

    def calculate(self, now_dm: int):
        # fi - массовый расход топлива в 1 секунду = вводимому значению
        if len(self.h) > 100:
            print("\n=========================================\n====================================================\n\n")
            self.h = [self.h[-1]]
            self.v = [self.v[-1]]
            self.a = [self.a[-1]]
            self.fuel_less = [self.fuel_less[-1]]
        fi = now_dm
        self.fuel_less.append(fi)
        self.m_fuel -= now_dm * self.dt
        mt = self.m_fuel + self.m_rocket
        self.t += self.dt
        self.verlet(mt)
        # self.cialc(mt)
        if int(self.t) != int(self.t - self.dt):
            print(f"Высота ракеты: {self.h[-1]}\nУскорение ракеты: {self.a[-1]}\nСкорость ракеты Верлет: {self.v[-1]}\n"
                  f"Скорость ракеты Циолковский: {self.v_cialc[-1]}\nВремени прошло:{self.t}\nТопливо: {self.m_fuel}")

    def cialc(self, mt: float):
        # print(math.log(self.m0 / mt))
        self.v_cialc.append(self.v_gas*math.log(self.m0 / mt) - self.g * self.t)

    def verlet(self, mt: float):
        self.h.append(self.h[-1] + self.v[-1] * self.dt + 0.5 * self.a[-1] * self.dt * self.dt)
        self.a.append(self.accel(mt))
        self.v.append(self.v[-1] + 0.5 * (self.a[-2]+self.a[-1]) * self.dt)

    def accel(self, mt: float):
        return self.v_gas * self.fuel_less[-1] / mt - self.g