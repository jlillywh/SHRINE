import pandas as pd
import numpy as np
from watershed import Watershed
from clock import Clock
import matplotlib.pyplot as plt

c = Clock()
ts = pd.Series(0, index=pd.date_range(c.start_date, periods=365, freq='D'))
w = Watershed()

from store import Store
s = Store()
s.capacity = 10.0
s.quantity = 9.0
s.update(100.0, 7.0)

w.add_catchment("C1", 100.0)
w.add_catchment("C2", 50.0)

w.link_flow("C1", "C2")



while c.running:
	precip = np.random.uniform() * 10.0
	et = np.random.uniform()

	ts[c.current_date] = catch01.runoff(precip, et)

	c.advance()

print(ts.head())

df = ts.to_frame()

df.plot()

plt.show()

