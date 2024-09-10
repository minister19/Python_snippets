from typing import List
from dynamic_range import DynamicRange


class Kline:
    def __init__(self, idx: int, high: float, low: float) -> None:
        self.idx = idx
        self.high = high
        self.low = low


class ZigZagPoint(Kline):
    def __init__(self, kline: Kline, type: str) -> None:
        super().__init__(**kline.__dict__)
        self.type = type  # '-', '^', 'v'


class Zigzag:
    def __init__(self, p_depth=200, p_deviation_range=[10.0, 5.0, 4.0]) -> None:
        self.depth = p_depth
        self.deviation = DynamicRange(p_depth, p_deviation_range)
        self.klines: List[Kline] = []           # K线
        self.points: List[ZigZagPoint] = []     # 高低点
        self.step = p_depth
        self.step_pre = p_depth
        self.cache: tuple[ZigZagPoint, float] = (None, None)
        self.idx = 0

    @staticmethod
    def find_min(data: List[Kline]):
        min = data[0]
        for d in data:
            if d.low < min.low:
                min = d
        return min

    @staticmethod
    def find_max(data: List[Kline]):
        max = data[0]
        for d in data:
            if d.high > max.high:
                max = d
        return max

    def init_points(self):
        self.points.clear()
        init_low, init_high = self.find_min(self.klines[0:self.depth]), self.find_max(self.klines[0:self.depth])
        if init_low.idx < init_high.idx:
            self.points.append(ZigZagPoint(init_low, 'v'))
            self.points.append(ZigZagPoint(init_high, '^'))
        else:
            self.points.append(ZigZagPoint(init_high, '^'))
            self.points.append(ZigZagPoint(init_low, 'v'))

    def find_points(self):
        while self.step < len(self.klines):
            pivot = self.klines[self.step]
            # 2022-09-29 Shawn: 极端情况，单个k线既有最大值，也有最小值，优先延续之前的信号
            if self.points[-1].type == 'v':
                if pivot.low < self.points[-1].low:
                    self.cache = (self.points[-1], self.deviation.value)
                    self.points[-1] = ZigZagPoint(pivot, 'v')
                elif pivot.high > self.points[-1].low * (1 + self.deviation.value):
                    self.points.append(ZigZagPoint(pivot, '^'))
            else:
                if pivot.high > self.points[-1].high:
                    self.cache = (self.points[-1], self.deviation.value)
                    self.points[-1] = ZigZagPoint(pivot, '^')
                elif pivot.low < self.points[-1].high * (1 - self.deviation.value):
                    self.points.append(ZigZagPoint(pivot, 'v'))
            self.step += 1

    def forward(self, high=None, low=None):
        self.klines.append(Kline(self.idx, high, low))

        if len(self.klines) < self.depth:
            pass
        elif len(self.points) < 2:
            self.init_points()
        else:
            self.step_pre = self.step
            self.find_points()
            if self.points[-1].idx == self.idx:
                self.deviation.reset()
            else:
                self.deviation.forward()

        self.idx += 1

    # 2024-09-09 Shawn: 当覆写 self.points[-1] 时，backward 应恢复原始 point
    def backward(self):
        self.klines.pop()

        if len(self.points) < 2:
            pass
        else:
            self.step = self.step_pre
            if self.points[-1].idx == (self.idx - 1):
                point_new = self.points.pop()
                if point_new.type == self.cache[0].type:
                    self.points.append(self.cache[0])
                    self.deviation.restore(self.cache[1])
                else:
                    self.deviation.restore()
            else:
                self.deviation.backward()

        self.idx -= 1

    def render(self):
        import matplotlib.pyplot as plt
        x, y1, y2 = [], [], []
        for d in self.klines:
            x.append(d.idx)
            y1.append(d.low)
            y2.append(d.high)
        scatter_x1, scatter_y1 = [], []
        scatter_x2, scatter_y2 = [], []
        for d in self.points:
            if d.type == 'v':
                scatter_x1.append(d.idx)
                scatter_y1.append(d.low)
            else:
                scatter_x2.append(d.idx)
                scatter_y2.append(d.high)

        fig, ax = plt.subplots(nrows=1, ncols=1)

        p1, = ax.plot(x, y1, "g-")
        p2, = ax.plot(x, y2, "r-")
        x = ax.scatter(x=scatter_x1, y=scatter_y1, s=25, c='black', marker='^')
        x = ax.scatter(x=scatter_x2, y=scatter_y2, s=25, c='blue', marker='v')

        plt.show()


if __name__ == "__main__":
    import random
    random.seed(0)

    z = Zigzag(100, [10.0, 5.0, 4.0])
    high = 10000
    low = 10000
    for i in range(10000):
        data = random.random() - 0.5
        is_up = data > 0
        if is_up:
            low = high
            high = high * (1 + data / 100)
        else:
            high = low
            low = low * (1 + data / 100)
        z.forward(high, low)
        z.backward()
        z.forward(high, low)
        # z.render()
    z.render()
