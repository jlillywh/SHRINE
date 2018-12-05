import unittest
from store import Store

class TestOutflowsCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up a new object to be tested
        '''
        self.store_name = "Reservoir01"
        init_quantity = 10.0
        self.capacity = 15.0
        self.s1 = Store(init_quantity, self.capacity)
        self.s1.name = self.store_name

        #print("Test: " + str(self.s1.getInstanceCount()))

    def tearDown(self):
        '''
        destroy the object after running tests
        '''
        #print("Tear down " + type(self.s1).__name__)
        del self.s1

    def testReducedOutflow(self):
        '''
        Outflow < request when quantity reaches lower bound
        '''
        inflow = 0.43
        request = 15.0
        self.s1.update(inflow, request)
        self.assertTrue(self, self.s1.outflow < request)

if __name__ == '__main__':
    unittest.main()