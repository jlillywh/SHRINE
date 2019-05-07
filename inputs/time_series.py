import pandas as pd
from global_attributes.aegis import Aegis
import numpy as np


class TimeSeries(Aegis):
    """Object to store time series data sets
    
        Attributes
        ----------
        name : str
        start_date : str
            Use mm/dd/yyyy format for the dates
        periods : int
        freq : str
        series : pandas Series
        
        """
    def __init__(self, name='TimeSeries', display_unit='in', start_date='1/1/2019', periods=365, freq='D'):
        Aegis.__init__(self)
        self.name = name
        range = pd.date_range(start_date, periods=periods, freq=freq)
        """range : pandas DatetimeIndex
            Represents the date range for the time series
            Must be used to provide the index list for the values"""
        self.series = pd.Series(np.zeros(len(range)), index=range)

    def set_value(self, at_date, value):
        """Find a value in the time series and replace it.
        
            Parameters
            ----------
            at_date : str
                (i.e. mm/dd/yyyy)
            value : any
                the type must match that of other values
                already in the series.
        """
        self.series[at_date] = value

    def load_csv(self, file_path):
        """Replaces the time series with data from csv file
        
            Parameters
            ----------
            file_path : str
                full or relative path to the file
        """
        self.series = pd.read_csv(file_path)
    