import unittest
from watershed import Watershed
from catchment import Catchment

class TestWatershed(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.w = Watershed()
        #self.w.add_node(Catchment('C1'), 'J1')
        self.precision = 2

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.w

    def testOutflow(self):
        """Outflow == defined value"""
        precip = 6.54
        et = 0.25

        for i in range(0,10):
            self.w.update(precip, et)

        self.assertAlmostEqual(self.w.outflow, 63905.34, self.precision)


if __name__ == '__main__':
    unittest.main()