class BaseDynamicRange:
    def __init__(self, depth=100, range=[16, 8, 4]) -> None:
        self.depth = depth
        self.range = range
        self.start = range[0] / 100
        self.mid = range[1] / 100
        self.stop = range[2] / 100
        self.step_mid = (self.start - self.mid) / (self.depth / 2)
        self.step_stop = (self.mid - self.stop) / (self.depth / 2)
        self.value = self.start
        self.value_pre = self.start
        self.idx = None

    def forward(self):
        if self.value > self.mid:
            self.value -= self.step_mid
        elif self.value > self.stop:
            self.value -= self.step_stop

    def backward(self):
        if self.value > self.mid:
            self.value += self.step_mid
        elif self.value > self.stop:
            self.value += self.step_stop

    def reset(self, idx):
        self.value_pre = self.value
        self.value = self.start
        self.idx = idx

    def restore(self, value=None):
        if value is None:
            self.value = self.value_pre
        else:
            self.value = value
        self.idx = None


class DynamicRange(BaseDynamicRange):
    def __init__(self, p_depth=100, p_range=[16, 8, 4]) -> None:
        super().__init__(p_depth, p_range)
        self.idx_mid = None

    def reset_mid(self, idx):
        self.value_pre = self.value
        self.value = self.mid
        self.idx_mid = idx

    def restore(self, value=None):
        if value is None:
            self.value = self.value_pre
        else:
            self.value = value
        self.idx = None
        self.idx_mid = None


if __name__ == "__main__":
    deviation = DynamicRange(100, [10, 5, 4])
    deviation.forward()
    deviation.backward()
    deviation.reset(0)
    deviation.restore()
    deviation.reset_mid(0)
    deviation.restore()
