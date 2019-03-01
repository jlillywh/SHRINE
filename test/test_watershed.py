import unittest
from hydrology.watershed import Watershed
from hydrology.catchment import Catchment

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
        
    def testOutflowLargeWatershed(self):
        """Outflow == defined value"""
        precip = 6.54
        et = 0.25
        
        precision = 1
        
        self.w.link_catchment('C2', 'J1')
        self.w.link_catchment('C3', 'J2')
        self.w.link_catchment('C4', 'J2')
        self.w.link_catchment('C5', 'J3')
        self.w.link_catchment('C6', 'J3')
        self.w.add_junction('J2', 'J1')
        self.w.add_junction('J3', 'J2')

        for i in range(0,10):
            self.w.update(precip, et)

        self.assertAlmostEqual(self.w.outflow, 383432.0, precision)

    def testGettingWatershed(self):
        """Make sure you can get a node when requested."""
        
        node = self.w.get_node('C1')
        
        self.assertTrue(type(node), Catchment)

if __name__ == '__main__':
    unittest.main()