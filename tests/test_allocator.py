import unittest
from water_manage.allocator import Allocator
from inputs.constants import U


class TestAllocator(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.proportional = False
        self.supply = 60 * U.m3
        self.requests = [10, 40, 35, 18] * U.m3 / U.day
        self.priorities = [2, 2, 3, 1]
        self.a1 = Allocator(self.supply, self.requests, self.priorities, self.proportional)

        # print("Test: " + str(self.s1.getInstanceCount()))
    
    def tearDown(self):
        """Destroy the object after running tests"""
        # print("Tear down " + type(self.s1).__name__)
        del self.proportional
        del self.supply
        del self.requests
        del self.priorities
    
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