from time import timezone
import pandas as pd
from datetime import datetime

# print(datetime.fromtimestamp(1603209600))
# print(datetime.fromtimestamp(1612868324294/1000))
# print(datetime.fromtimestamp(1613283396746//1000))
print(datetime.fromtimestamp(1640851200))
print(datetime.fromtimestamp(1640649600))
print(datetime.fromtimestamp(1640617020000//1000))
a = datetime.now()
b = pd.Timestamp(ts_input=a, tzinfo=a.tzinfo)
c = b.floor(freq='T')
d = b.ceil(freq='T')
e = d.timestamp()
f = int(e)
g = datetime.fromtimestamp(f)
print(a, c, d, g)

delta = datetime.now() - datetime.utcnow()
print(delta.seconds / 3600)
