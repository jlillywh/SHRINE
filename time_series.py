from aegis import Aegis
from datetime import date, timedelta

class TimeSeries(Aegis):
    def __int__(self):
        Aegis.__init__(self)

        self.value_header = "Value"
        self.date_header = "Date"

        self.start_date = date.today()
        self.end_date = self.start_date + timedelta(days=100)