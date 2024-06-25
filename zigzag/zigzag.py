from typing import List


class Kline:
    def __init__(self, idx: int, high: float, low: float) -> None:
        self.idx = idx
        self.high = high
        self.low = low


class ZigZagPoint(Kline):
    def __init__(self, kline: Kline, type: str = '-') -> None:
        super().__init__(**kline.__dict__)
        self.type = type  # '-', '^', 'v'


class Zigzag:
    def __init__(self, p_depth=100, p_deviation_range=[10.0, 5.0]) -> None:
        self.p_depth = p_depth
        self.p_deviation_start = p_deviation_range[0] / 100
        self.p_deviation_stop = p_deviation_range[1] / 100
        self.p_deviation_step = (self.p_deviation_start - self.p_deviation_stop) / self.p_depth
        self.p_deviation_pre = self.p_deviation_start
        self.p_deviation = self.p_deviation_start
        self.klines: List[Kline] = []           # K线
        self.points: List[ZigZagPoint] = []     # 高低点
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
        init_low, init_high = self.find_min(self.klines[0:self.p_depth]), self.find_max(self.klines[0:self.p_depth])
        if init_low.idx < init_high.idx:
            self.points.append(ZigZagPoint(init_low, 'v'))
            self.points.append(ZigZagPoint(init_high, '^'))
        else:
            self.points.append(ZigZagPoint(init_high, '^'))
            self.points.append(ZigZagPoint(init_low, 'v'))

    def find_points(self):
        previous = self.points[-1]
        step = previous.idx + 1
        while step < len(self.klines):
            pivot = self.klines[step]
            # 2022-09-29 Shawn: 极端情况，单个k线既有最大值，也有最小值，优先延续之前的信号
            if previous.type == 'v':
                if pivot.low < previous.low:
                    self.points[-1] = ZigZagPoint(pivot, 'v')
                elif pivot.high > previous.low * (1 + self.p_deviation):
                    self.points.append(ZigZagPoint(pivot, '^'))
            else:
                if pivot.high > previous.high:
                    self.points[-1] = ZigZagPoint(pivot, '^')
                elif pivot.low < previous.high * (1 - self.p_deviation):
                    self.points.append(ZigZagPoint(pivot, 'v'))
            previous = self.points[-1]
            step = step + 1

    def forward(self, high=None, low=None):
        self.klines.append(Kline(self.idx, high, low))

        if len(self.klines) < self.p_depth:
            pass
        elif len(self.points) < 2:
            self.init_points()
        else:
            self.find_points()

        if len(self.points) > 0 and self.points[-1].idx == self.idx:
            self.p_deviation_pre = self.p_deviation
            self.p_deviation = self.p_deviation_start
        elif self.p_deviation > self.p_deviation_stop:
            self.p_deviation -= self.p_deviation_step

        self.idx += 1

    def backward(self):
        self.klines.pop()

        if len(self.points) > 0 and self.points[-1].idx == (self.idx - 1):
            self.p_deviation = self.p_deviation_pre
            self.points.pop()
        elif self.p_deviation > self.p_deviation_stop:
            self.p_deviation += self.p_deviation_step

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

    z = Zigzag(100, [3, 3])
    high = 10000
    low = 10000
    for i in range(1000):
        is_up = random.random() > 0.5
        if is_up:
            low = high
            high = high * (1 + random.random() / 100)
        else:
            high = low
            low = low * (1 - random.random() / 100)
        z.forward(high, low)
        z.backward()
        z.forward(high, low)
        # z.render()
    z.render()
