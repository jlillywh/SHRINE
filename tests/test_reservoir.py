import unittest
from water_manage.reservoir import Reservoir


class TestReservoir(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.r1 = Reservoir()
        self.r1.water_level = 9.9
        self.r1.spillway_crest = 10.9

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.r1

    def testReducedOutflow(self):
        inflow = 10
        for i in range(10):
            self.r1.update(inflow, 0.0)
            
        self.assertAlmostEqual(self.r1.quantity, 176700, 1)
