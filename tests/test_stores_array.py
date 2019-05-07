from unittest import TestCase
from water_manage.store_array import StoreArray


class TestStoresCase(TestCase):
    def setUp(self):
        """
        Set up a new object to be tested
        #TODO: add test for transferring _quantity from one item to another.
        """

        self.sa = StoreArray(4, unit='gal')
        inflow = [2.5, 7.8, 23.65, 5.23]
        outflow = [11.0, 0.0, 2.2, 100.0]
        self.sa.update(inflow, outflow)
        self.total_quantity = 29.25

    def tearDown(self):
        del self.sa

    def testQuantity(self):
        self.assertEqual(self.sa.total_quantity(), self.total_quantity)

    def testOverflow(self):
        self.assertEqual(self.sa.total_overflow(), 0.0)

    def testOutflow(self):
        self.assertAlmostEqual(self.sa.total_outflow(), 9.93)
