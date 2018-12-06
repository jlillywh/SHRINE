import unittest
from awbm import Awbm

class TestBucketCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""

        self.a1 = Awbm()
        self.partial_area_fraction = [0.134, 0.433, 0.433]

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
            self.assertEqual(self.a1.buckets.stores[i].capacity, new_buckets[i] * self.partial_area_fraction[i])

    #def testBucketOverflow(self):


if __name__ == '__main__':
    unittest.main()