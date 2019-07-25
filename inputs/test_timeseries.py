from unittest import TestCase
from inputs.time_series import TimeSeries
import datetime
from datetime import timedelta
from data.fileman import FileManager
import pandas as pd


class TestTimeSeries(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        fm = FileManager('..\\data_external')
        fm.add_file("WGEN PAR Input Time Series.xlsx")
        xls_file = pd.ExcelFile(fm.get_file(0))
        df = xls_file.parse(skiprows=3, index_col=0)
        self.s1 = df['Rain']
        self.s2 = df['Tmax']
        self.s3 = df['Tmin']
        self.s4 = df['Rad']
        self.ts = TimeSeries('1/1/19', periods=365)
        self.dec_places = 3
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.ts
    
    
    def test_num_of_records(self):
        nr = 365
        self.assertEqual(self.ts.num_of_records(), nr)

    def test_start_date(self):
        sd = datetime.date(2019, 1, 1)
        self.assertEqual(self.ts.start_date(), sd)
    
    def test_end_date(self):
        ed = datetime.date(2019, 12, 31)
        self.assertEqual(self.ts.end_date(), ed)
        
    def test_end_date(self):
        ed = datetime.date(2019, 12, 31)
        self.assertEqual(self.ts.end_date(), ed)
        
    def test_duration(self):
        dur = timedelta(days=365)
        self.assertEqual(self.ts.duration(), dur)