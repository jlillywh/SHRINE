import unittest
from water_manage.reservoir import Reservoir
from inputs.constants import U


class TestReservoir(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.r1 = Reservoir()
        self.r1.water_level = 9.9 * U.m
        self.r1.spillway_crest = 10.9 * U.m

        #print("Test: " + str(self.s1.getInstanceCount()))

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.s1).__name__)
        del self.r1

    def testReducedOutflow(self):
        inflow = 1000 * U.m3 / U.day
        for i in range(10):
            self.r1.update(inflow, 0 * U.m3 / U.day)
            
        self.assertAlmostEqual(self.r1._quantity, 186600 * U.m3, 1)
