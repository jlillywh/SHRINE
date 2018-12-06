from datetime import datetime, date, time, timedelta
from aegis import Aegis


class Clock(Aegis):
    """Clock objects for keeping track of time during a simulation
        ...

        Attributes
        ----------

        Methods
        -------
        """
    def __init__(self, start_date=date.today(), duration = timedelta(days=100), time_step=timedelta(days=1)):
        Aegis.__init__(self)
        self.name = "Clock"
        self.description = "Clock to keep track of simulation time."
        self.start_date = start_date
        self.duration = duration
        self.end_date = start_date + duration
        self.current_date = self.start_date
        self.time_step = time_step
        self.remaining_time = self.duration

    def advance(self):
        """Increment the clock by 1 time step."""
        if self.current_date >= self.end_date:
            print("Simulation Complete!")
        else:
            self.current_date += self.time_step
            self.remaining_time -= self.time_step

    def set_start_date(self, new_date):
        """Change the start date before running a new simulation
            It is assumed that you want the end date to also change when
            you change the start date becasue the duration would be held
            constant. Therefore, the end_date is also adjusted here. The
            current date is also reset to the start date.

            Parameters
            ----------
            new_date : datetime

            Returns
            -------
            """
        self.start_date = new_date
        self.current_date = new_date
        self.end_date = self.current_date + self.duration

    def set_duration(self, new_duration):
        """Change the duration and update the end_date.
            It is assumed that if the duration changes, then the end
            date will also have to change rather than the start date."""
        self.duration = timedelta(days=new_duration)
        self.remaining_time = self.duration
        self.end_date = self.start_date + self.duration

    def to_s(self):
        object_summary = "Summary of the Clock: "