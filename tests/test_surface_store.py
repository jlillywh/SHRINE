import unittest
from awbm import Awbm

class TestBucketCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up a new object to be tested
        '''

        self.a1 = Awbm()
        self.a1.runoff(100.0, 0.0)
        self.precision = 3  # decimal places for testing equality among floats

    def tearDown(self):
        '''
        destroy the object after running tests
        '''
        #print("Tear down " + type(self.s1).__name__)
        del self.a1

    def testInflow(self):
	    self.assertAlmostEqual(self.a1.surface.quantity, 2.887, self.precision)

    def testOutflow(self):
        self.a1.runoff(100.0, 0.0)
        self.assertAlmostEqual(self.a1.surface.outflow, 0.378, self.precision)

if __name__ == '__main__':
    unittest.main()