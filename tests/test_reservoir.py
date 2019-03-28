import unittest
from water_manage.reservoir import Reservoir
from inputs.constants import U


class TestReservoir(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        init_quantity = 10.0 * U.m3
        self.capacity = 15.0 * U.m3
        self.r1 = Reservoir(init_quantity)
        self.r1.capacity = self.capacity

        #print("Test: " + str(self.s1.getInstanceCount()))

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.s1).__name__)
        del self.r1

    def testReducedOutflow(self):
        inflow = 10 * U.m3 / U.sday
        for i in range(10):
            self.r1.update(inflow, 0 * U.m3 / U.d)
            self.r1.spillway_flow()
