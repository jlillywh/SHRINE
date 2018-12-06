import unittest
import random
from datetime import datetime, date, time, timedelta
from clock import Clock

class TestClockCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        new_date = date(1986, 4, 28)
        self.c = Clock()
        self.c.set_start_date(new_date)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.c

    def testEndTime(self):
        """End Time should be 100 days from start"""
        end_date = date(1986, 8, 6)
        self.assertEqual(self.c.end_date, end_date)

    def testRemainingTime(self):
        """Check to see if remaining time is correct after one clock advancement"""
        num_days = random.randint(1,50)
        for t in range(num_days):
            self.c.advance()
        current_date = date(1986, 4, 28) + timedelta(days=num_days)
        remaining_time = timedelta(100 - num_days)
        self.assertEqual(self.c.remaining_time, remaining_time)
        self.assertEqual(self.c.current_date, current_date)

    def testChangeDuration(self):
        """Make sure the end time is correct after changing the duration"""
        self.c.set_duration(10)
        self.assertEqual(self.c.remaining_time, timedelta(10))
        self.assertEqual(self.c.end_date, date(1986, 5, 8))

    def testChangeStart(self):
        """Make sure the end date is correct after changing the start date"""
        self.c.set_start_date(date(2010, 1, 15))
        for t in range(10):
            self.c.advance()
        self.assertEqual(date(2010, 4, 25), self.c.end_date)



if __name__ == '__main__':
    unittest.main()