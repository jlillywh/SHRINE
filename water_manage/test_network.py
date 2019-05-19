import unittest
from water_manage.flow_network import Network


class TestMyNetwork(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.n1 = Network()
        
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.n1
        
    def testFlowCapacity(self):
        capacity = 4.0
        self.n1.add_source('C1', capacity)
        discharge = self.n1.outflow()
        self.assertEqual(discharge, capacity)
        
    def testAddNodeFlow(self):
        """Add 2 nodes that both flow to the sink"""
        capacity = 4.0
        self.n1.add_source('C1', capacity)
        self.n1.add_source('C2', capacity, 'Sink')
        # self.n1.draw()
        discharge = self.n1.outflow()
        self.assertEqual(discharge, capacity * 2)


if __name__ == '__main__':
    unittest.main()
