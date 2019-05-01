import unittest
from water_manage.allocator import Allocator
from water_manage.request import Request
from inputs.constants import U


class TestAllocator(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.proportional = False
        self.supply = 60 * U.m3
        r1 = Request('pumping', 10 * U.m3 / U.day, 2)
        r2 = Request('farm', 40 * U.m3 / U.day, 2)
        r3 = Request('mine', 35 * U.m3 / U.day, 3)
        r4 = Request('evaporation', 18 * U.m3 / U.day, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests, self.proportional)

        # print("Test: " + str(self.s1.getInstanceCount()))
    
    def tearDown(self):
        """Destroy the object after running tests"""
        # print("Tear down " + type(self.s1).__name__)
        del self.proportional
        del self.supply
        del self.requests
    
    def testEqualPriority(self):
        self.a1.proportional = False
        self.a1.allocate()
        outflows = self.a1.outflows
        outlfow_actual = [10, 32, 0, 18, 0] * U.m3/U.day
        error = 0.0 * U.m3/U.day
        for i in range(len(outflows)):
            error += abs(outflows[i] - outlfow_actual[i])
        self.assertAlmostEqual(error, 0.0 * U.m3/U.day, 3)
        
    def testProportionalPriority(self):
        self.a1.proportional = True
        self.a1.allocate()
        outflows = self.a1.outflows
        outlfow_actual = [8.4, 33.6, 0, 18, 0] * U.m3/U.day
        error = 0.0 * U.m3/U.day
        for i in range(len(outflows)):
            error += abs(outflows[i] - outlfow_actual[i])
        self.assertAlmostEqual(error, 0.0 * U.m3/U.day, 3)