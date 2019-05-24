import unittest
from water_manage.flow_network import Network
import numpy as np
import os


class TestMyNetwork(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.n1 = Network()
        
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.n1
        
    def testFlowCapacity(self):
        capacity = 6337.5
        self.n1.add_source('C1')
        self.n1.draw()
        discharge = self.n1.outflow()
        self.assertEqual(discharge, capacity)
        
    def testAddNodeFlow(self):
        """Add 2 nodes that both flow to the sink"""
        capacity = np.random.random()
        self.n1.add_source('C1', capacity)
        self.n1.add_source('C2', capacity, 'Sink')
        # self.n1.draw()
        discharge = self.n1.outflow()
        self.assertEqual(discharge, capacity * 2)
        
    def testAddJunction(self):
        """Add a junction that joins 2 source nodes"""
        capacity = np.random.random()
        self.n1.add_junction('J1', 'Sink')
        self.n1.add_source('C1', capacity, 'J1')
        self.n1.add_source('C2', capacity, 'J1')
        # self.n1.draw()
        discharge = self.n1.outflow()
        self.assertEqual(discharge, capacity * 2)
        
    def testMultipleJunctions(self):
        """Add multiple junctions that joins 2 source nodes"""
        capacity1 = np.random.random()
        capacity2 = np.random.random()
        capacity3 = np.random.random()
        capacity4 = np.random.random()
        expected_sum = capacity1 + capacity2 + capacity3 + capacity4
        self.n1.add_junction('J1', 'Sink')
        self.n1.add_junction('J2', 'J1')
        self.n1.add_source('C1', capacity1, 'J1')
        self.n1.add_source('C2', capacity2, 'J1')
        self.n1.add_source('C3', capacity3, 'J2')
        self.n1.add_source('C4', capacity4, 'J2')
        # self.n1.draw()
        discharge = self.n1.outflow()
        self.assertEqual(discharge, expected_sum)

    def testReadFromGML(self):
        cwd = os.getcwd()
        filename = cwd + '\\test_data\\network_GML_input.gml'
        self.n1.load_from_file(filename)
        
        # self.n1.draw()
        discharge = 4 * 4
        self.assertEqual(self.n1.outflow(), discharge)


if __name__ == '__main__':
    unittest.main()
