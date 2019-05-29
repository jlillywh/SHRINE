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
        self.precision = 5
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.n1
        del self.precip
        del self.et
        del self.precision
    
    def testFlowCapacity(self):
        flow = np.random.random()
        self.n1.add_catchment('C1')
        self.n1.update_capacity('C1', flow)
        # self.n1.draw()
        self.assertEqual(self.n1.outflow(), flow)
    
    def testAddNodeFlow(self):
        """Add 2 nodes that both flow to the sink"""
        flow1 = np.random.random()
        flow2 = np.random.random()
        self.n1.add_catchment('C1')
        self.n1.add_catchment('C2')
        self.n1.update_capacity('C1', flow1)
        self.n1.update_capacity('C2', flow2)
        # capacity = {('C1', 'sink'): flow1, ('C2', 'sink'): flow2}
        # self.n1.draw()
        self.assertEqual(self.n1.outflow(), flow1 + flow2)
    
    def testAddJunction(self):
        """Add a junction that joins 2 source nodes"""
        flow1 = np.random.random()
        flow2 = np.random.random()
        self.n1.add_junction('J1', 'sink')
        self.n1.add_catchment('C1', 'J1')
        self.n1.add_catchment('C2', 'J1')
        self.n1.update_capacity('C1', flow1)
        self.n1.update_capacity('C2', flow2)
        # self.n1.draw()
        self.assertEqual(self.n1.outflow(), flow1 + flow2)
    
    def testMultipleJunctions(self):
        """Add multiple junctions that joins 2 source nodes"""
        flow1 = np.random.uniform(1, 100)
        flow2 = np.random.uniform(1, 100)
        flow3 = np.random.uniform(1, 100)
        flow4 = np.random.uniform(1, 100)
        expected_sum = flow1 + flow2 + flow3 + flow4
        self.n1.add_junction('J1', 'sink')
        self.n1.add_junction('J2', 'J1')
        self.n1.add_catchment('C1', 'J1')
        self.n1.add_catchment('C2', 'J1')
        self.n1.add_catchment('C3', 'J2')
        self.n1.add_catchment('C4', 'J2')
        # self.n1.draw()
        self.n1.update_capacity('C1', flow1)
        self.n1.update_capacity('C2', flow2)
        self.n1.update_capacity('C3', flow3)
        self.n1.update_capacity('C4', flow4)
        self.assertAlmostEqual(self.n1.outflow(), expected_sum, self.precision)
    
    def test_update_all(self):
        flow1 = np.random.uniform(1, 100)
        flow2 = np.random.uniform(1, 100)
        flow3 = np.random.uniform(1, 100)
        flow4 = np.random.uniform(1, 100)
        expected_sum = flow1 + flow2 + flow3 + flow4

        self.n1.add_junction('J1', 'sink')
        self.n1.add_junction('J2', 'J1')
        self.n1.add_catchment('C1', 'J1')
        self.n1.add_catchment('C2', 'J1')
        self.n1.add_catchment('C3', 'J2')
        self.n1.add_catchment('C4', 'J2')
        
        # capacity = {('C1', 'J1'): {'capacity': flow1}, ('C2', 'J1'): {'capacity': flow2}, ('C3', 'J2'): {'capacity': flow3}, ('C4', 'J2'): {'capacity': flow4}}
        capacity = {'C1': flow1, 'C2': flow2, 'C3': flow3, 'C4': flow4}
        
        self.n1.update_all(capacity)
        self.assertAlmostEqual(self.n1.outflow(), expected_sum, self.precision)
        
    def testReadFromGML(self):
        filename = "C:\\Users\\jlillywhite\\PyCharmProjects\\AegisProject\\water_manage\\test_data\\network_GML_input.gml"
        self.n1.load_from_file(filename)
        
        # self.n1.draw()
        flow1 = np.random.uniform(1, 100)
        flow2 = np.random.uniform(1, 100)
        flow3 = np.random.uniform(1, 100)
        flow4 = np.random.uniform(1, 100)
        expected_sum = flow1 + flow2 + flow3 + flow4
        capacity = {'C1': flow1, 'C2': flow2, 'C3': flow3, 'C4': flow4}

        self.n1.update_all(capacity)
        self.n1.outflow()
        self.assertAlmostEqual(self.n1.outflow(), expected_sum, self.precision)


if __name__ == '__main__':
    unittest.main()
