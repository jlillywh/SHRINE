import unittest
from awbm import Awbm

class TestBucketCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""

        self.a1 = Awbm()

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.s1).__name__)
        del self.a1

    def testChangeBuckets(self):
        """New bucket capacity == user defined array"""
        new_buckets = [57.43, 143.33, 298.49]
        self.a1.set_comp_capacity(new_buckets)
        self.assertEqual(self.a1.depth_comp_capacity, new_buckets)

    #def testBucketOverflow(self):


if __name__ == '__main__':
    unittest.main()