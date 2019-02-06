import unittest
from hydrology.catchment import Catchment

class TestCatchment(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.catchment_name = "C1"
        self.area = 12.6
        self.c1 = Catchment(self.catchment_name, self.area)
        self.c1.name = self.catchment_name
        self.precision = 1

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.c1).__name__)
        del self.c1

    def testOutflow(self):
        """Outflow == defined value"""
        precip = 6.54
        et = 0.25

        for i in range(0,10):
            self.c1.update_runoff(precip, et)

        self.assertAlmostEqual(self.c1.outflow, 8052.1, self.precision)


if __name__ == '__main__':
    unittest.main()