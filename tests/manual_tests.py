import pandas as pd
import numpy as np
from awbm import Awbm
from clock import Clock
import matplotlib.pyplot as plt

c = Clock()
ts = pd.Series(0, index=pd.date_range(c.start_date, periods=365, freq='D'))
a = Awbm()

while c.running:
	precip = np.random.uniform() * 10.0
	et = np.random.uniform()

	ts[c.current_date] = a.runoff(precip, et)

	c.advance()

print(ts.head())

df = ts.to_frame()

df.plot()

plt.show()

