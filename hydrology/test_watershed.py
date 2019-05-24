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
        
if __name__ == '__main__':
    unittest.main()
