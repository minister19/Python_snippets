from dynamic_range import DynamicRange


class DynamicRangeResetMid(DynamicRange):
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
    deviation = DynamicRangeResetMid(100, [10, 5, 4])
    deviation.forward()
    deviation.backward()
    deviation.reset(0)
    deviation.restore()
    deviation.reset_mid(1)
    deviation.restore()
