# ref: http://www.grantjenks.com/docs/sortedcontainers/

import json
from sortedcontainers import SortedSet, SortedDict, SortedList
from datetime import datetime

ss = SortedList()


class Test:
    def __init__(self, value) -> None:
        self.value = value
        self.timestamp = datetime.now()

    @property
    def data(self):
        d = {
            'value': self.value,
            'timestamp': self.timestamp
        }
        return d

    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)


ss.add(Test(1))
ss.add(Test(9))
ss.add(Test(3))
ss.add(Test(7))
ss.add(Test(5))
ss.add(Test(5))
ss.add(Test(6))
ss.add(Test(0))

a = Test(1)
b = a.data
c = getattr(a, 'value')
