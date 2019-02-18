import pandas as pd
import matplotlib.pyplot as plt
from global_attributes.aegis import Aegis
import numpy as np
from global_attributes.clock import Clock


class TimeHistory(Aegis):
    """Object to store time series data sets based on clock data

        Attributes
        ----------
        name : str
        start_date : str
            Use mm/dd/yyyy format for the dates
        periods : int
        freq : str
        series : pandas Series
        th_list : list(Series)

        """
    
    def __init__(self, name='TimeHistory', unit='in', clock=Clock()):
        Aegis.__init__(self)
        self.name = name
        self.unit = unit
        range = pd.date_range(clock.start_date, clock.range.size, clock.time_step.days)
        """range : pandas DatetimeIndex
            Represents the date range for the time series
            Must be used to provide the index list for the values"""
        self.series = pd.Series(np.zeros(len(range)), index=range)
        self.series.name = self.name
        self.series.index.name = 'date'
        self.th_list = []
    
    def set_value(self, series_name, at_date, value):
        """Find a value in the time series and replace it.

            Parameters
            ----------
            at_date : str
                (i.e. mm/dd/yyyy)
            value : any
                the type must match that of other values
                already in the series.
        """
        self.series[series_name][at_date] = value
    
    def add_series(self, new_series):
        """Add a series to be plotted with the other(s)
        
            Parameters
            ----------
            new_series : Series
                Make sure the Series is named!
        """
        self.th_list.append(new_series)
        self.series = pd.concat(self.th_list, axis=1)
    
    def load_csv(self, file_path):
        """Replaces the time series with data from csv file

            Parameters
            ----------
            file_path : str
                full or relative path to the file
        """
        self.series = pd.read_csv(file_path)
        
    def show(self):
        self.series.plot(title=self.name)
        plt.ylabel(self.unit)
        plt.tight_layout()
        plt.show()
