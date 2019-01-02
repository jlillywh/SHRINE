import unittest
from catchment import Catchment

class TestCatchment(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.catchment_name = "C1"
        self.area = 15.0
        self.c1 = Catchment(self.catchment_name, self.area)
        self.c1.name = self.catchment_name
        self.precision = 2

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.c1).__name__)
        del self.c1

    def testOutflow(self):
        """Outflow == defined value"""
        precip = 3.54
        et = 0.25

        for i in range(1,4):
            self.c1.update_runoff(precip, et)

        self.assertAlmostEqual(self.c1.outflow, 372.63, self.precision)


if __name__ == '__main__':
    unittest.main()