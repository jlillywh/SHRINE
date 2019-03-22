import unittest
from hydraulics.pipe import Pipe


class TestPipe(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.p1 = Pipe(1000.0, 1.0, 'steel', 1.7)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.p1

    def testHeadLoss(self):
        """Head loss should be correct"""
        q = 7.47
        self.assertAlmostEqual(self.p1.head_loss(q, 'HW'), 30, 1)
        self.p1.material = 'concrete'
        q = 7.01
        self.assertAlmostEqual(self.p1.head_loss(q, 'DW'), 30, 1)
        
    def testMinorLoss(self):
        """Friction loss should be correct"""
        q = 7.47
        self.assertAlmostEqual(self.p1.minor_loss(q), 2.4, 1)
        
    def testGravityFlow(self):
        """Friction loss should be correct"""
        dz = 30.0
        self.assertAlmostEqual(self.p1.gravity_flow(dz), 7.47, 2)
        self.p1.material = 'concrete'
        self.assertAlmostEqual(self.p1.gravity_flow(dz, 'DW'), 7.01, 2)

