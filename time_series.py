from datetime import date, timedelta
import random
from aegis import Aegis

class TimeSeries(Aegis):
    def __init__(self, start_date=date.today()):
        Aegis.__init__(self)
        self.date_header = "Date"
        self.value_header = "Value"
        self.start_date = start_date
        self.num_records = 10
        self.end_date = self.start_date + timedelta(days=self.num_records)

        self.dates = []
        self.values = []

        for i in range(self.num_records):
            self.dates.append(self.start_date + timedelta(days=i))
            self.values.append(random.randint(1,10))

"""

        self.dates = []

        for i in range(self.num_records):
            self.dates.append(self.start_date + timedelta(days=1))

    def get_value_header(self):
        print(self.value_header)
"""