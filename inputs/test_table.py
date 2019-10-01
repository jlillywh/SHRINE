import unittest
#from data.fileman import FileManager
from inputs.table import Table


class TestAllocator(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        x = [0.0, 10.0, 20.0]
        y = [0.0, 35.0, 48.0]
        self.table = Table(x, y)
        self.decimals = 3
        
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.table
        self.decimals
        
    def test_Interpolate_Y(self):
        x_value = 12.0
        y_expected = 37.60
        y_result = self.table.lookup_y(x_value)
        self.assertEqual(y_expected, y_result)

    def test_Interpolate_X(self):
        y_value = 12.0
        x_expected = 3.4286
        x_result = self.table.lookup_x(y_value)
        self.assertAlmostEqual(x_expected, x_result, self.decimals)

# fm = FileManager('..\\data_external')
# filename = 'data.xlsx'
# fm.add_file(filename)
# input_file = fm.files[filename]
#
# t = Table()
# t.load_from_excel(input_file, 'Table', 'a4')
# t.name = "Elevation-Area Table"
# t.plot()