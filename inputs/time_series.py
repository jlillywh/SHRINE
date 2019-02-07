import pandas as pd
from pandas import Series
import numpy as np


class TimeSeries(Series):
    def __init__(self, start_date='1/1/2019', periods=365, freq='D'):
        Series.__init__(self)
        self.range = pd.date_range(start_date, periods=periods, freq=freq)
        self.values = pd.Series(np.zeros(len(self.range)), index=self.range)

    def set_value(self, at_date, value):
	    self.values[at_date] = value