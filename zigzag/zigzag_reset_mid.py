from dynamic_range_reset_mid import DynamicRangeResetMid
from zigzag_base import Kline, ZigZagPoint, Zigzag


class ZigzagResetMid(Zigzag):
    def __init__(self, p_depth=200, p_deviation_range=[10.0, 5.0, 4.0]) -> None:
        super().__init__(p_depth, p_deviation_range)
        self.deviation = DynamicRangeResetMid(p_depth, p_deviation_range)

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
                if self.cache is not None and self.cache[0].idx + self.depth < self.idx:
                    self.deviation.reset_mid(self.idx)
                else:
                    self.deviation.reset(self.idx)
            else:
                self.deviation.forward()

        self.idx += 1


if __name__ == "__main__":
    import random
    random.seed(0)

    z = ZigzagResetMid(100, [10.0, 5.0, 4.0])
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
