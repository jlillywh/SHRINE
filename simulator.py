from aegis import Aegis
from clock import Clock
from watershed import Watershed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Simulator(Aegis):
	def __init__(self):
		Aegis.__init__(self)

		self.c = Clock()
		self.w = Watershed()
		self.ts = pd.Series(0, index=pd.date_range(self.c.start_date, periods=365, freq='D'))

	def run(self):
		while self.c.running:
			precip = np.random.uniform() * 3.0
			et = np.random.uniform()
			self.w.update(precip, et)
			self.ts[self.c.current_date] = self.w.outflow

			self.c.advance()

	def plot_ts(self):
		df = self.ts.to_frame()

		df.plot()

		plt.show()