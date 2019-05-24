import unittest
from water_manage.flow_network import Network
import numpy as np
import os


class TestMyNetwork(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.n1 = Network()
        self.precip = 10.0
        self.et = 0.25
        
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.n1
        del self.precip
        del self.et
        
    def testFlowCapacity(self):
        capacity = 6337.5
        self.n1.add_source('C1')
        # self.n1.draw()
        self.n1.update(self.precip, self.et)
        self.assertEqual(self.n1.outflow, capacity)
        
    def testAddNodeFlow(self):
        """Add 2 nodes that both flow to the sink"""
        capacity = 6337.5 * 2
        self.n1.add_source('C1')
        self.n1.add_source('C2')
        self.n1.draw()
        self.n1.update(self.precip, self.et)
        self.assertEqual(self.n1.outflow, capacity)
        
    def testAddJunction(self):
        """Add a junction that joins 2 source nodes"""
        capacity = 6337.5 * 2
        self.n1.add_junction('J1', 'Sink')
        self.n1.add_source('C1', 'J1')
        self.n1.add_source('C2', 'J1')
        # self.n1.draw()
        self.n1.update(self.precip, self.et)
        self.assertEqual(self.n1.outflow, capacity)
        
    def testMultipleJunctions(self):
        """Add multiple junctions that joins 2 source nodes"""
        capacity1 = 6337.5
        capacity2 = 6337.5
        capacity3 = 6337.5
        capacity4 = 6337.5
        expected_sum = capacity1 + capacity2 + capacity3 + capacity4
        self.n1.add_junction('J1', 'Sink')
        self.n1.add_junction('J2', 'J1')
        self.n1.add_source('C1', 'J1')
        self.n1.add_source('C2', 'J1')
        self.n1.add_source('C3', 'J2')
        self.n1.add_source('C4', 'J2')
        # self.n1.draw()
        self.n1.update(self.precip, self.et)
        self.assertEqual(self.n1.outflow, expected_sum)

    def testReadFromGML(self):
        cwd = os.getcwd()
        filename = cwd + '\\test_data\\network_GML_input.gml'
        self.n1.load_from_file(filename)
        
        # self.n1.draw()
        discharge = 6337.5 * 4
        self.n1.update(self.precip, self.et)
        self.assertEqual(self.n1.outflow, discharge)


if __name__ == '__main__':
    unittest.main()
