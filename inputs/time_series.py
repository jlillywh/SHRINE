import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns


class TimeSeries:
    """Object to store time series data sets
    
        Attributes
        ----------
        start_date : str
            Use mm/dd/yyyy format for the dates
        periods : int
        freq : str
        data : numpy.ndarray
        
        """
    def __init__(self, values_name='values', start_date='1/1/19', periods=365):
        """Initialize with values of zero for the duration and frequency.
        
            Parameters
            ----------
            date_range : pandas DatetimeIndex
            Represents the date range for the time series
            Must be used to provide the index list for the values"""
        _start_date = datetime.strptime(start_date, '%x').date()
        self.date_rng = pd.date_range(start=start_date, periods=periods)
        self.values_name = values_name
        # self.df = pd.DataFrame({date': [_start_date + timedelta(days=x) for x in range(periods)], self.values_name: pd.Series(np.random.randn(periods))})
        # self.df = self.df.set_index('date')
        self.df = pd.DataFrame(self.date_rng, columns=['date'])
        self.df[values_name] = np.random.randint(0, 100, size=len(self.date_rng))
        self.df['datetime'] = pd.to_datetime(self.df['date'])
        self.df = self.df.set_index('datetime')
        self.df.drop(['date'], axis=1, inplace=True)
        
        # self.date_range = pd.date_range(start_date, periods=periods, freq=freq)
        # np.random.seed(seed=1111)
        # self.data = np.random.randint(1, high=100, size=len(self.date_range))
        # self.df = pd.DataFrame({'Date': self.date_range, 'Values': self.data})
        # self.df.set_index('Date')
    
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
        self.df[at_date] = value
    
    def load_csv(self, file_path):
        """Replaces the time series with data from csv file
        
            Parameters
            ----------
            file_path : str
                full or relative path to the file
        """
        self.df = pd.read_csv(file_path, skiprows=2)
    
    def num_of_records(self):
        """ The number of time-value records (or rows in the time series).
        
        Returns:
            int: the return value
        """
        return len(self.df.index)
    
    def start_date(self):
        """ The calendar time of the *first* datetime or etime of the time series.
        
        Returns:
            datetime.date: the return value
        """
        return self.df.index.min()
    
    def end_date(self):
        """ The calendar time of the *last* datetime or etime of the time series.
        
        Returns:
            datetime.date: the return value
        """
        return self.df.index.max()
    
    def duration(self):
        """ The duration between the start and end time of the index.
            1 day is added for the last day of the time series,
        Returns:
            timedelta: the return value
        """
        return self.end_date() - self.start_date() + timedelta(days=1)

    def date_at_value(self, value):
        date_list = self.df.loc[self.df[self.values_name] == value]
        return date_list.index.min()
    
    def plot(self):
        sns.set(rc={'figure.figsize': (11, 4)})
        axis = self.df[self.values_name].plot(linewidth=1)
        axis.set_ylabel(self.values_name)
        # self.df.plot()
