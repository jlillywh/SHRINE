from results.chart import Chart
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class TimeSeriesChart(Chart):
    def __init__(self, name):
        Chart.__init__(self, name)
        range = pd.date_range('1/1/2019', periods=365, freq='D')
        series = pd.Series(np.zeros(len(range)), index=range)
        self.outputs = []
        self.values = series
        
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
        self.values.plot()
        plt.show()
        plt.close()