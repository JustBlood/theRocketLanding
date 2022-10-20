class Calculation:

    h = []
    v = [0.0]
    a = [0.0]
    fuel_less = [0]

    def __init__(self, m_fuel: float, m_rocket: float, g: float, v_gas: float, height: float, allow_landing_v: float, dt: float, allow_max_dm: float):
        self.allow_max_dm = allow_max_dm
        self.dt = dt
        self.allow_landing_v = allow_landing_v
        self.h.append(height)
        self.v_gas = v_gas
        self.g = g
        self.m_rocket = m_rocket
        self.m_fuel = m_fuel

    def calculate(self, now_dm: int):
        fi = now_dm/self.dt
        self.fuel_less.append(fi)
        self.m_fuel -= now_dm
        mt = self.m_fuel + self.m_rocket
        self.verlet(mt)
        print(f"Высота ракеты: {self.h[-1]}\nУскорение ракеты: {self.a[-1]}\nСкорость ракеты: {self.v[-1]}")

    def verlet(self, mt: float):
        self.h.append(self.h[-1] + self.v[-1] * self.dt + 0.5 * self.a[-1] * self.dt * self.dt)
        self.a.append(self.accel(mt))
        self.v.append(self.v[-1] + 0.5 * (self.a[-2]+self.a[-1]) * self.dt)

    def accel(self, mt: float):
        return self.v_gas * self.fuel_less[-1] / mt - self.g