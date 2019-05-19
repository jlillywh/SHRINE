import unittest
from hydraulics.pipe import Pipe


class TestPipe(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        length = 304.8
        diameter = 0.3048
        material = 'steel'
        minor_loss = 1.7
        self.p1 = Pipe(length, diameter, material, minor_loss)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.p1

    def testHeadLoss(self):
        """Head loss should be correct"""
        q = 0.211386
        self.assertAlmostEqual(self.p1.head_loss(q, 'HW'), 9.13776, 3)
        self.p1.material = 'concrete'
        q = 0.199
        self.assertAlmostEqual(self.p1.head_loss(q, 'DW'), 9.18614, 3)
        
    def testMinorLoss(self):
        """Friction loss should be correct"""
        q = 0.212
        self.assertAlmostEqual(self.p1.minor_loss(q), 0.73169, 3)
        
    def testGravityFlow(self):
        """Friction loss should be correct"""
        dz = 9.144
        self.assertAlmostEqual(self.p1.gravity_flow(dz), 0.2115, 3)
        self.p1.material = 'concrete'
        self.assertAlmostEqual(self.p1.gravity_flow(dz, 'DW'), 0.1985, 3)


if __name__ == '__main__':
    unittest.main()