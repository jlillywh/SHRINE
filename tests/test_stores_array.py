import unittest
from water_manage.store_array import StoreArray
from inputs.constants import U



class TestStoresCase(unittest.TestCase):
    def setUp(self):
        """
        Set up a new object to be tested
        #TODO: add test for transferring _quantity from one item to another.
        """

        self.sa = StoreArray(4, unit=U.m3)
        inflow = [2.5, 7.8, 23.65, 5.23] * U.m3/U.day
        outflow = [11.0, 0.0, 2.2, 100.0] * U.m3/U.day
        self.sa.update(inflow, outflow)

        self.total_quantity = 29.25 * U.m3

    def tearDown(self):
        """
        destroy the object after running tests
        """
        #print("Tear down " + type(self.s1).__name__)
        del self.sa

    def testQuantity(self):
        self.assertEqual(self.sa.total_quantity(), self.total_quantity)

    def testOverflow(self):
        self.assertEqual(self.sa.total_overflow(), 0.0 * U.m3/U.day)

    def testOutflow(self):
        self.assertAlmostEqual(self.sa.total_outflow(), 9.93 * U.m3/U.day)

if __name__ == '__main__':
    unittest.main()