import unittest
from hydrology.watershed import Watershed
from hydrology.catchment import Catchment
from data.fileman import FileManager
from inputs.constants import U


class TestWatershed(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.precision = 2
        
        fm = FileManager('..\\data_external')
        filename = 'watershed_GML_input.gml'
        fm.add_file(filename)
        
        self.w = Watershed()
        self.w.load_from_file(fm.file_list[filename])
        self.w.network.adj['J2']['J1']['runoff'] = 9999 * U.m3 / U.day
        self.w.network.adj['J3']['J2']['runoff'] = 9999 * U.m3 / U.day

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.w
        
    def testOutflowLargeWatershed(self):
        """Outflow == defined value"""
        precip = 6.54 * U.mm / U.day
        et = 0.25 * U.mm / U.day
        
        precision = 1

        for i in range(0, 10):
            self.w.update(precip, et)

        self.assertAlmostEqual(self.w.outflow, 137809.7 * U.m3/U.day, precision)

    def testGettingWatershed(self):
        """Make sure you can get a node when requested."""
        
        node = self.w.get_node('C1')
        
        self.assertTrue(type(node), Catchment)


if __name__ == '__main__':
    unittest.main()
