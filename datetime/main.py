from time import timezone
import pandas as pd
from datetime import datetime

# print(datetime.fromtimestamp(1603209600))
# print(datetime.fromtimestamp(1612868324294/1000))
# print(datetime.fromtimestamp(1613283396746//1000))
print(datetime.fromtimestamp(1629252000))

a = datetime.now()
b = pd.Timestamp(ts_input=a, tzinfo=a.tzinfo)
c = b.floor(freq='T')
d = b.ceil(freq='T')
e = d.timestamp()
f = int(e)
g = datetime.fromtimestamp(f)
print(a, c, d, g)
