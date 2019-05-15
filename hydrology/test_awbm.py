import unittest
from hydrology.awbm import Awbm


class TestBucketCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested
        
            Compare results to GoldSim model: AWBM Verification.gsm"""

        self.a1 = Awbm()
        self.a1.buckets.set_quantities([0.0042, 0.05, 0.0429])
        self.a1.base.quantity = 0.01
        self.a1.surface.quantity = 0.01
        for i in range(10):
            self.a1.runoff(0.01, 0.001)
        self.precision = 3

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.a1
        del self.precision

    def testUpdateCompCapacity(self):
        """New bucket capacity == user defined array"""
        new_buckets = [0.05743, 0.14333, 0.29849]
        self.a1.set_comp_capacity(new_buckets)
        for i in range(len(new_buckets)):
            self.assertEqual(self.a1.buckets.stores[i].capacity, new_buckets[i] * self.a1.partial_area_fraction[i])

    def testBucketsQuantity(self):
        """change the total quantity in the buckets"""
        self.assertAlmostEqual(self.a1.buckets.total_quantity(), 0.152, self.precision)

    def testBucketsOverflow(self):
        """change the total quantity in the buckets"""
        # cap = [0.04, 0.15, 0.3]
        # self.a1.set_comp_capacity(cap)
        overflow = self.a1.buckets.total_overflow()
        self.assertAlmostEqual(overflow, 0.0051, self.precision)

    def testSurfaceQuantity(self):
        """change the total quantity in the buckets"""
        v = self.a1.surface.quantity
        self.assertAlmostEqual(v, 0.0106, self.precision)

    def testBaseQuantity(self):
        """change the total quantity in the buckets"""
        self.assertAlmostEqual(self.a1.base.quantity, 0.0048565, self.precision)


class TestSurfaceStore(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.a2 = Awbm()
        self.a2.buckets.set_quantities([0.00502, 0.140, 0.063])
        self.precision = 3

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.a2

    def testStoreOutflow(self):
        """Make sure the outflow from the store is correct"""
        precip = 0.00654
        et = 0.00025
        outflow = 0.0
        for i in range(0, 10):
            outflow += self.a2.runoff(precip, et)

        self.assertAlmostEqual(outflow, 0.024936, self.precision)


if __name__ == '__main__':
    unittest.main()