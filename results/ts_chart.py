from results.chart import Chart
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class TimeSeriesChart(Chart):
    def __init__(self, name):
        Chart.__init__(self, name)
        range = pd.date_range('1/1/2019', periods=365, freq='D')
        self.series = pd.Series(np.zeros(len(range)), index=range)
        
    def show(self):
        self.series.plot()
        plt.show()
    
    