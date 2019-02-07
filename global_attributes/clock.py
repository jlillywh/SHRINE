import pandas as pd
from global_attributes.aegis import Aegis


class Clock(Aegis):
    """Clock objects for keeping track of time during a simulation
        ...

        Attributes
        ----------
            start_date : pandas Timestamp
            duration :

        Methods
        -------
            set_current_date
            reset
            advance
        """
    def __init__(self, start_date='1/1/2019', end_date='1/1/2020', time_step='1 days'):
        Aegis.__init__(self)
        self.description = "Clock to keep track of simulation time."
        ## Static time variables
        self.start_date = pd.Timestamp(start_date)
        self.end_date = pd.Timestamp(end_date)
        self.duration = self.end_date - self.start_date
        self.range = pd.date_range(start=self.start_date, end=self.end_date)
        self.time_step = pd.Timedelta(time_step)

        ## Dynamic time variables
        self.current_date = self.start_date
        self.remaining_time = self.duration
        self.running = True
        
    def reset(self):
        """Reset the clock settings back to their original state.
        
            This is useful when performing multiple simulations
        """
        self.current_date = self.start_date
        self.remaining_time = self.duration
        self.running = True

    def advance(self):
        """Increment the clock by 1 time step."""
        if self.current_date >= self.end_date:
            self.running = False
        else:
            self.current_date += self.time_step
            self.remaining_time -= self.time_step

    def set_start_date(self, new_date):
        """Change the start date before running a new simulation
            It is assumed that you want the end date to also change when
            you change the start date because the duration would be held
            constant. Therefore, the end_date is also adjusted here. The
            current date is also reset to the start date.

            The "running" state is also set to True.

            Parameters
            ----------
            new_date : str
                string formats allowed: 'mm/dd/yyyy'; 'mm-dd-yyyy'

            Returns
            -------
            """
        self.start_date = pd.Timestamp(new_date, freq=self.time_step)
        self.current_date = self.start_date
        self.end_date = self.current_date + self.duration
        self.running = True
        self.range = pd.date_range(start=self.start_date, end=self.end_date)
        
    def set_current_date(self, new_date):
        """Set the current date of the clock.
        
            This is useful if you want to force the clock time to a known
            point in time for debugging.
            
            Parameters : str
                new_date
        """
        self.current_date = pd.Timestamp(new_date, freq=self.time_step)
        if self.current_date >= self.end_date:
            self.running = False
            self.duration = pd.Timedelta('0 days')
        else:
            self.duration = self.end_date - self.current_date

        self.remaining_time = self.duration

    def set_duration(self, new_duration):
        """Change the duration and update the end_date.
            It is assumed that if the duration changes, then the end
            date will also have to change rather than the start date.

            Parameters
            ----------
                new_duration : str (i.e. '100 days')
        """
        self.duration = pd.Timedelta(new_duration)
        self.remaining_time = self.duration
        self.end_date = self.start_date + self.duration

    def to_s(self):
        object_summary = "Summary of the Clock: "