import unittest
from water_manage.allocator import Allocator
from water_manage.request import Request


class TestAllocator(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.supply = 60
        r1 = Request('pumping', 10, 2)
        r2 = Request('farm', 18, 2)
        r3 = Request('mine', 35, 3)
        r4 = Request('evaporation', 18, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests)

        # print("Test: " + str(self.s1.get_instance_count()))
    
    def tearDown(self):
        """Destroy the object after running tests"""
        # print("Tear down " + type(self.s1).__name__)
        del self.a1
        del self.supply
        del self.requests
        
    def testAddRequest(self):
        name = 'environmental'
        amount = 3.65
        self.a1.add_request(name, amount, 4)
        r = self.a1.get_request(name)
        self.assertEqual(r.amount, amount)
        
    def testProportionalPriority(self):
        self.a1.update()
        outflows = self.a1.deliveries
        outflow_actual = {'pumping': 10,
                          'evaporation': 18,
                          'farm': 18,
                          'mine': 14,
                          'remainder': 0
                          }
        self.assertDictEqual(outflows, outflow_actual)

    def testAllEqualPriorities(self):
        r1 = Request('pumping', 20, 2)
        r2 = Request('farm', 18, 2)
        r3 = Request('mine', 35, 2)
        r4 = Request('evaporation', 18, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests)
        self.a1.update()
        outflows = self.a1.deliveries
        outflow_actual = {'pumping': 11.506849315068493,
                          'evaporation': 18,
                          'farm': 10.356164383561644,
                          'mine': 20.136986301369863,
                          'remainder': 0}
        self.assertDictEqual(outflows, outflow_actual)
        
    def testRemainder(self):
        r1 = Request('pumping', 14.67, 2)
        r2 = Request('farm', 18, 2)
        r3 = Request('mine', 5, 2)
        r4 = Request('evaporation', 18, 1)
        self.requests = [r1, r2, r3, r4]
        self.a1 = Allocator(self.supply, self.requests)
        self.a1.update()
        outflows = self.a1.deliveries
        outlfow_actual = {'pumping': 14.67,
                          'evaporation': 18,
                          'farm': 18,
                          'mine': 5,
                          'remainder': 4.329999999999998}
        self.assertDictEqual(outflows, outlfow_actual)
