import unittest
from water_manage.allocator import Allocator
from water_manage.request import Request
from inputs.constants import U


class TestAllocator(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.supply = 60 * U.m3 / U.day
        r1 = Request('pumping', 10 * U.m3 / U.day, 2)
        r2 = Request('farm', 18 * U.m3 / U.day, 2)
        r3 = Request('mine', 35 * U.m3 / U.day, 3)
        r4 = Request('evaporation', 18 * U.m3 / U.day, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests)

        # print("Test: " + str(self.s1.getInstanceCount()))
    
    def tearDown(self):
        """Destroy the object after running tests"""
        # print("Tear down " + type(self.s1).__name__)
        del self.a1
        del self.supply
        del self.requests
        
    def testAddRequest(self):
        name = 'environmental'
        amount = 3.65 * U.m3 / U.day
        self.a1.add_request(name, amount, 4)
        r = self.a1.get_request(name)
        self.assertEqual(self.a1.get_request(name).amount, amount)
        
    def testProportionalPriority(self):
        self.a1.update()
        outflows = self.a1.deliveries
        outlfow_actual = {'pumping': 10 * U.m3 / U.day,
                          'evaporation': 18 * U.m3 / U.day,
                          'farm': 18 * U.m3 / U.day,
                          'mine': 14 * U.m3 / U.day,
                          'remainder': 0 * U.m3 / U.day}
        self.assertDictEqual(outflows, outlfow_actual)

    def testAllEqualPriorities(self):
        r1 = Request('pumping', 20 * U.m3 / U.day, 2)
        r2 = Request('farm', 18 * U.m3 / U.day, 2)
        r3 = Request('mine', 35 * U.m3 / U.day, 2)
        r4 = Request('evaporation', 18 * U.m3 / U.day, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests)
        self.a1.update()
        outflows = self.a1.deliveries
        outlfow_actual = {'pumping': 11.506849315068493 * U.m3 / U.day,
                          'evaporation': 18 * U.m3 / U.day,
                          'farm': 10.356164383561644 * U.m3 / U.day,
                          'mine': 20.136986301369863 * U.m3 / U.day,
                          'remainder': 0 * U.m3 / U.day}
        self.assertDictEqual(outflows, outlfow_actual)
        
    def testRemainder(self):
        r1 = Request('pumping', 14.67 * U.m3 / U.day, 2)
        r2 = Request('farm', 18 * U.m3 / U.day, 2)
        r3 = Request('mine', 5 * U.m3 / U.day, 2)
        r4 = Request('evaporation', 18 * U.m3 / U.day, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests)
        self.a1.update()
        outflows = self.a1.deliveries
        outlfow_actual = {'pumping': 14.67 * U.m3 / U.day,
                          'evaporation': 18 * U.m3 / U.day,
                          'farm': 18 * U.m3 / U.day,
                          'mine': 5 * U.m3 / U.day,
                          'remainder': 4.329999999999998 * U.m3 / U.day}
        self.assertDictEqual(outflows, outlfow_actual)