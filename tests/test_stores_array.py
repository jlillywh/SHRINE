import unittest
import random
from store_array import StoreArray

"""To Do:
    - add test for transferring _quantity from one item to another.
    """

class TestStoresCase(unittest.TestCase):
    def setUp(self):
        """
        Set up a new object to be tested
        """

        self.sa = StoreArray(4)
        inflow = [2.5, 7.8, 23.65, 5.23]
        outflow = [11.0, 0.0, 2.2, 100.0]
        self.sa.update(inflow, outflow)

        self.total_quantity = 325.98

    def tearDown(self):
        """
        destroy the object after running tests
        """
        #print("Tear down " + type(self.s1).__name__)
        del self.sa

    def testQuantity(self):
        self.assertEqual(self.sa.total_quantity(), self.total_quantity)

    def testOverflow(self):
	    self.assertEqual(self.sa.total_overflow(), 0.0)

    def testOutflow(self):
        self.assertAlmostEqual(self.sa.total_outflow(), 113.2)

if __name__ == '__main__':
    unittest.main()