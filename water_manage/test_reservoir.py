import unittest
from water_manage.reservoir import Reservoir
import numpy as np


class TestReservoir(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.r1 = Reservoir()
        self.r1.water_level = 9.9
        self.r1.spillway_crest = 10.9

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.r1
        
    def testVolumeEqualQuantity(self):
        self.assertEqual(self.r1.volume, self.r1.quantity)

    def testReducedOutflow(self):
        inflow = 10
        for i in range(10):
            self.r1.update(inflow, 0.0)
            
        self.assertAlmostEqual(self.r1.volume, 274.24, 2)

    def testChangeCapacityOverflow(self):
        """Test that volume == capacity when updated capacity is
                changed to be less than the current volume
        """
        updated_capacity = 25.0
        self.r1.capacity = updated_capacity
        self.assertEqual(self.r1.capacity, updated_capacity)
    
    def testExcessInflowOverflow(self):
        """Test that volume == capacity after update when:
                - inflow + outflow + initial volume > capacity
        """
        self.r1.capacity = 25.0
        self.r1.update(0, np.random.random() + 2.0)
        self.r1.update(5.0 + np.random.random(), 0.0)
        self.assertEqual(self.r1.volume, self.r1.capacity)
        
    def testLevelOutput(self):
        """Test that correct water level is reported."""
        self.r1.water_level = 12.52
        self.assertEqual(self.r1.water_level, 12.52)
        
    def testUpdateLevel(self):
        """Test that correct volume is reported after updating level."""
        self.r1.water_level = 3.4
        self.assertAlmostEqual(self.r1.volume, 59.84, 2)

    def testAreaOutput(self):
        """Test that correct pool area is reported."""
        self.r1.water_level = 12.52
        self.assertAlmostEqual(self.r1.area, 38.276, 2)

