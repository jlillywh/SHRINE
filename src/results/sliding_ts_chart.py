from results.ts_chart import TimeHistoryChart
from collections import deque
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class TSlider(TimeHistoryChart):
    """Chart that slides the x-axis during a simulation to the left on each time step.
        
        The data for this chart is an array in which a value is appended to the beginning and the last one is removed
        like a typical queue.
        
        Attributes
        ----------
        queue : deque
            The queued results in the array
        
        Methods
        -------
        update()
            this updates the array by popping 1 entry.
    """
    
    def __init__(self, values=random.sample(range(100), 10), date='1/1/2019', size=10):
        """
            Parameters
            ----------
            values : list of numbers
            date : str
                The date of the value on far right of array
            size : int
                The size of the array
        """
        TimeHistoryChart.__init__(self)
        self.last_date = pd.Timestamp(date)
        first_date = self.last_date - pd.Timedelta(str(size) + ' days')
        self.dates = pd.date_range(first_date, periods=size)
        self.size = size
        self.queue = deque(values)
        self.data = pd.DataFrame(np.random.randn(6), index=self.dates, columns='A')
        
    def update(self, new_value):
        """Adds a value to the end of the array and removes the first.
        
            Parameters
            ----------
            new_value : Quantity
                The value that is added to the front of the list.
        """
        self.queue.append(new_value)
        self.queue.popleft()
        self.last_date += pd.Timedelta('1 days')

        plt.axis([0, 10, 0, 1])

        for i in range(10):
            y = np.random.random()
            plt.scatter(i, y)
            plt.pause(0.05)

        plt.show()
        
    