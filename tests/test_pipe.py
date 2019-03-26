import unittest
from hydraulics.pipe import Pipe
from inputs.constants import U


class TestPipe(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        length = 1000.0 * U.ft
        diameter = 12.0 * U.inch
        self.p1 = Pipe(length, diameter, 'steel', 1.7)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.p1

    def testHeadLoss(self):
        """Head loss should be correct"""
        q = 7.47 * U.cfs
        self.assertAlmostEqual(self.p1.head_loss(q, 'HW'), 30.03 * U.ft, 2)
        self.p1.material = 'concrete'
        q = 7.01 * U.cfs
        self.assertAlmostEqual(self.p1.head_loss(q, 'DW'), 30 * U.ft, 1)
        
    def testMinorLoss(self):
        """Friction loss should be correct"""
        q = 7.47 * U.cfs
        self.assertAlmostEqual(self.p1.minor_loss(q), 2.4 * U.ft, 1)
        
    def testGravityFlow(self):
        """Friction loss should be correct"""
        dz = 30.0 * U.ft
        self.assertAlmostEqual(self.p1.gravity_flow(dz), 7.47 * U.cfs, 2)
        self.p1.material = 'concrete'
        self.assertAlmostEqual(self.p1.gravity_flow(dz, 'DW'), 7.01 * U.cfs, 2)

