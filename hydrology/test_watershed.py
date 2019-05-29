import unittest
from hydrology.watershed import Watershed
from hydrology.catchment import Catchment
import numpy as np
from data.fileman import FileManager


class TestWatershed(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested
        
            Note the model used for verification is called:
            Watershed Verification large.gsm
        """
        self.w = Watershed()
        self.w.add_junction('J1', 'sink')
        self.w.link_catchment('C1', 'J1')
        self.w.link_catchment('C2', 'J1')
        self.precision = 3
       
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.w
        
    def testDischarge(self):
        precip = np.random.uniform(0, 15)
        et = np.random.uniform(0, 2)
        
        c = Catchment()
        expected_ouflow = c.outflow(precip, et) * 2
        
        self.assertAlmostEqual(self.w.discharge(precip, et), expected_ouflow, self.precision)
        
    def testLoadFile(self):
        precip = np.random.uniform(0, 15)
        et = np.random.uniform(0, 2)
        c = Catchment()
        expected_ouflow = c.outflow(precip, et) * 4
        
        filename = "C:\\Users\\jlillywhite\\PyCharmProjects\\AegisProject\\hydrology\\test_data\\watershed_GML_input.gml"

        self.w = Watershed()
        self.w.load_from_file(filename)
        self.assertAlmostEqual(self.w.discharge(precip, et), expected_ouflow, self.precision)

        
if __name__ == '__main__':
    unittest.main()
