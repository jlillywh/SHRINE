import unittest
from awbm import Awbm

class TestBucketCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""

        self.a1 = Awbm()
        self.init_quantity_buckets = [4.2, 140.4, 42.9]
        self.a1.buckets.set_quantities(self.init_quantity_buckets)
        self.a1.base.set_quantity(10.0)
        self.a1.surface.set_quantity(10.0)
        self.a1.runoff(10.0, 1.0)
        self.precision = 4

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.s1).__name__)
        del self.a1

    def testUpdateCompCapacity(self):
        """New bucket capacity == user defined array"""
        new_buckets = [57.43, 143.33, 298.49]
        self.a1.set_comp_capacity(new_buckets)
        new_capacity = []
        for i in range(len(new_buckets)):
            self.assertEqual(self.a1.buckets.stores[i].capacity, new_buckets[i] * self.a1.partial_area_fraction[i])

    def testBucketsQuantity(self):
        """change the total quantity in the buckets"""
        self.assertEqual(self.a1.buckets.total_qantity(), 192.047)

    def testBucketsOverflow(self):
        """change the total quantity in the buckets"""
        self.assertAlmostEqual(self.a1.buckets.total_overflow(), 4.345, self.precision)

    def testSurfaceQuantity(self):
        """change the total quantity in the buckets"""
        self.assertAlmostEqual(self.a1.surface._quantity, 10.176, self.precision)

    def testBucketsQuantity(self):
        """change the total quantity in the buckets"""
        self.assertAlmostEqual(self.a1.base._quantity, 5.949, self.precision)

"""
catchment.buckets.total_quantity()))
print("Bucket overflow = " + str(catchment.buckets.total_overflow()))
print("Surface Store amount = " + str(catchment.surface._quantity))
print("Baseflow Store amount = " + str(catchment.base._quantity))"""

if __name__ == '__main__':
    unittest.main()