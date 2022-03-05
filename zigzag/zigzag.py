from random import random
from typing import List


class Kline:
    def __init__(self, idx, high, low) -> None:
        self.idx = idx
        self.high = high
        self.low = low


class Point:
    def __init__(self, kline: Kline, is_low) -> None:
        self.kline = kline
        self.is_low = is_low


class Zigzag:
    def __init__(self) -> None:
        self.depth = 12
        self.deviation = 3.0
        self.data: List[Kline] = []
        self.points: List[Point] = []

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
            self.points.append(Point(init_low, True))
            self.points.append(Point(init_high, False))
        else:
            self.points.append(Point(init_high, False))
            self.points.append(Point(init_low, True))

    def init_position(self):
        if len(self.points) < 2:
            self.init_points()

    def find_points(self):
        # TODO: 考虑极端情况，单个k线既有最大值，也有最小值
        # TODO: 当历史数据即将处理完时，停止处理，信号值为划线分析趋势
        previous = self.points[-1]
        step = previous.kline.idx + 1
        while step < len(self.data):
            pivot = self.data[step]
            if previous.is_low:
                if pivot.low < previous.kline.low:
                    self.points[-1] = Point(pivot, True)
                elif pivot.high > previous.kline.low * (1 + self.deviation/100):
                    self.points.append(Point(pivot, False))
            else:
                if pivot.high > previous.kline.high:
                    self.points[-1] = Point(pivot, False)
                elif pivot.low < previous.kline.high * (1 - self.deviation/100):
                    self.points.append(Point(pivot, True))
            previous = self.points[-1]
            step = step + 1


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
    z.init_points()
    z.init_position()
    z.find_points()

    # import matplotlib.pyplot as plt
    x, y1, y2 = [], [], []
    for d in z.data:
        x.append(d.idx)
        y1.append(d.high)
        y2.append(d.low)
    scatter_x, scatter_y = [], []
    for d in z.points:
        scatter_x.append(d.kline.idx)
        scatter_y.append(d.kline.low if d.is_low else d.kline.high)
    print(scatter_x, scatter_y)
