import unittest
from hydrology.watershed import Watershed
from hydrology.catchment import Catchment
from data.fileman import FileManager


class TestWatershed(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested
        
            Note the model used for verification is called:
            Watershed Verification large.gsm
        """
        self.precision = 2
        
        fm = FileManager('..\\hydrology\\test_data')
        filename = 'watershed_GML_input.gml'
        fm.add_file(filename)
        
        self.w = Watershed()
        self.w.load_from_file(fm.file_list[filename])
       
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.w
        
    def testOutflowLargeWatershed(self):
        """Outflow == defined value"""
        precip = 0.00654
        et = 0.00025
        
        precision = 1

        for i in range(0, 11):
            self.w.update(precip, et)

        self.assertAlmostEqual(self.w.outflow, 396.272, precision)

    def testGettingWatershed(self):
        """Make sure you can get a node when requested."""
        
        node = self.w.get_node('C1')
        
        self.assertTrue(type(node), Catchment)


if __name__ == '__main__':
    unittest.main()
