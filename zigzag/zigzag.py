from random import random
from typing import List


class Kline:
    def __init__(self, idx: int, high: float, low: float) -> None:
        self.idx = idx
        self.high = high
        self.low = low


class ZigZagPoint(Kline):
    def __init__(self, idx, high, low, type='-') -> None:
        super().__init__(idx, high, low)
        self.type = type  # '-', '^', 'v'


class Zigzag:
    def __init__(self, depth=12, deviation=3.0) -> None:
        self.depth = depth
        self.deviation = deviation
        self.data: List[Kline] = []
        self.points: List[ZigZagPoint] = []

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
        init_low, init_high = self.find_min(self.data[0:self.depth]), self.find_max(self.data[0:self.depth])
        if init_low.idx < init_high.idx:
            self.points.append(ZigZagPoint(init_low.idx, init_low.high, init_low.low, 'v'))
            self.points.append(ZigZagPoint(init_high.idx, init_high.high, init_high.low, '^'))
        else:
            self.points.append(ZigZagPoint(init_high.idx, init_high.high, init_high.low, '^'))
            self.points.append(ZigZagPoint(init_low.idx, init_low.high, init_low.low, 'v'))

    def find_points(self):
        previous = self.points[-1]
        step = previous.idx + 1
        while step < len(self.data):
            pivot = self.data[step]
            # 2022-09-29 Shawn: 极端情况，单个k线既有最大值，也有最小值，优先延续之前的信号
            if previous.type == 'v':
                if pivot.low < previous.low:
                    self.points[-1] = ZigZagPoint(pivot.idx, pivot.high, pivot.low, 'v')
                elif pivot.high > previous.low * (1 + self.deviation/100):
                    self.points.append(ZigZagPoint(pivot.idx, pivot.high, pivot.low, '^'))
            else:
                if pivot.high > previous.high:
                    self.points[-1] = ZigZagPoint(pivot.idx, pivot.high, pivot.low, '^')
                elif pivot.low < previous.high * (1 - self.deviation/100):
                    self.points.append(ZigZagPoint(pivot.idx, pivot.high, pivot.low, 'v'))
            previous = self.points[-1]
            step = step + 1

    def forward(self):
        if len(self.data) < self.depth:
            pass
        elif len(self.points) < 2:
            self.init_points()
        else:
            self.find_points()

    def render(self):
        import matplotlib.pyplot as plt
        x, y1, y2 = [], [], []
        for d in self.data:
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
    z = Zigzag()
    high = 10000
    low = 10000
    for i in range(1000):
        is_up = random() > 0.5
        if is_up:
            low = high
            high = high * (1 + random() / 100)
        else:
            high = low
            low = low * (1 - random() / 100)
        z.data.append(Kline(i, high, low))
        # z.forward()
        # z.render()
    z.forward()
    z.render()
