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
        
    def testPriorityOrder(self):
        expected_first_request = 'evaporation'
        self.assertEqual(self.a1.requests[0].name, expected_first_request)
        expected_last_request = 'mine'
        self.assertEqual(self.a1.requests[-1].name, expected_last_request)
        
    def testChangePriority(self):
        self.a1.edit_priority('evaporation', 10)
        #self.a1.get_request('evaporation').priority = 10
        new_request = Request('seepage', 300.0, 1)
        self.a1.add_request(new_request)
        expected_first_request = 'seepage'
        self.assertEqual(self.a1.requests[0].name, expected_first_request)
    
    def testSupplySetter(self):
        new_supply = 80.0
        self.a1.supply = new_supply
        expected_delivery = new_supply
        self.assertAlmostEqual(self.a1.total_deliveries(), expected_delivery)
        
    def testAddRequest(self):
        name = 'environmental'
        amount = 3.65
        new_request = Request(name, amount, 4)
        self.a1.add_request(new_request)
        r = self.a1.get_request(name)
        self.assertEqual(r.amount, amount)
        
    def testProportionalPriority(self):
        outflows = self.a1.deliveries
        outflow_actual = {'pumping': 10,
                          'evaporation': 18,
                          'farm': 18,
                          'mine': 14,
                          'remainder': 0
                          }
        self.assertDictEqual(outflows, outflow_actual)

    def testAllEqualPriorities(self):
        self.a1.get_request('pumping').amount = 20
        self.a1.get_request('mine').priority = 2
        outflows = self.a1.deliveries
        outflow_actual = {'pumping': 11.506849315068493,
                          'evaporation': 18,
                          'farm': 10.356164383561644,
                          'mine': 20.136986301369863,
                          'remainder': 0}
        self.assertDictEqual(outflows, outflow_actual)
        
    def testRemainder(self):
        self.a1.get_request('pumping').amount = 14.67
        self.a1.get_request('mine').amount = 5
        self.a1.get_request('mine').priority = 2
        outflows = self.a1.deliveries
        outlfow_actual = {'pumping': 14.67,
                          'evaporation': 18,
                          'farm': 18,
                          'mine': 5,
                          'remainder': 4.329999999999998}
        self.assertDictEqual(outflows, outlfow_actual)

    def testDefaultRequests(self):
        """Make sure the default request is zero."""
        a2 = Allocator()
        self.assertEqual(a2.total_deliveries(), 0.0)
        self.assertEqual(a2.requests[0].name, 'outflow1')
        
    def testChangeRequest(self):
        """Change a request amount and make sure allocation is
            as expected."""
        pumping = self.a1.requests[0]
        pumping.amount = 17.43
        