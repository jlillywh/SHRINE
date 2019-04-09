from results.chart import Chart
import matplotlib.pyplot as plt
from results.time_history import TimeHistory
import pandas as pd
import numpy as np


class TimeHistoryChart(Chart):
    def __init__(self):
        Chart.__init__(self)
        self.outputs = []
        self.values = TimeHistory()
        
    def add_result(self, time_series_result):
        """Add a time series object to the chart.
        
            Parameters
            ----------
            time_series_result : TimeSeries
                This must be in the form of an Aegis TimeSeries object
        """
        
        self.outputs.append(time_series_result.series)
        self.values = pd.concat(self.outputs, axis=1)
        
    def show(self):
        self.values.show()
        plt.show()
        plt.close()
