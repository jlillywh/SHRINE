import unittest
import numpy as np
import pandas as pd
from clock import Clock

class TestClockCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.start_date = pd.Timestamp('4/28/1975')
        self.end_date = pd.Timestamp('10/15/1988')
        self.duration = self.end_date - self.start_date
        self.c = Clock(self.start_date, self.end_date)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.c

    def testEndTime(self):
        """End Time should be 100 days from start"""
        self.assertEqual(self.c.end_date, self.end_date)

    def testRemainingTime(self):
        """Check to see if remaining time is correct after one clock advancement"""
        num_days = np.random.randint(1,50)
        for t in range(num_days):
            self.c.advance()
        current_date = pd.Timestamp(self.start_date + pd.Timedelta(days=num_days))
        remaining_time = pd.Timedelta(self.duration - pd.Timedelta(days=num_days))
        self.assertEqual(self.c.remaining_time, remaining_time)
        self.assertEqual(self.c.current_date, current_date)

    def testChangeDuration(self):
        """Make sure the end time is correct after changing the duration"""
        self.c.set_duration('10 days')
        end_date = self.start_date + pd.Timedelta(days=10)
        self.assertEqual(self.c.remaining_time, pd.Timedelta('10 days'))
        self.assertEqual(self.c.end_date, end_date)

    def testChangeStart(self):
        """Make sure the end date is correct after changing the start date"""
        start_date = '4/15/2010'
        self.c.set_start_date(start_date)
        num_days = np.random.randint(1, 50)
        for t in range(num_days):
            self.c.advance()
        current_date = pd.Timestamp(pd.Timestamp(start_date) + pd.Timedelta(days=num_days))
        self.assertEqual(current_date, self.c.current_date)



if __name__ == '__main__':
    unittest.main()