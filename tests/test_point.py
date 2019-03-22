import unittest
from geometry.point import Point


class TestPoint(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.p1 = Point(2.5, 1.4, 0.6, 'foot')
        self.dec_places = 3

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.p1

    def testSetUnit(self):
        """Values should be converted correctly upon changing the unit"""
        new_unit = 'meter'
        p2 = self.p1
        p2.set_unit(new_unit)
        self.assertAlmostEqual(p2.x.magnitude, 0.762, self.dec_places)
        self.assertAlmostEqual(p2.y.magnitude, 0.427, self.dec_places)
        self.assertAlmostEqual(p2.z.magnitude, 0.183, self.dec_places)

    def testMovePoint(self):
        """The point should move the correct amount"""
        x_move = 2.3
        y_move = -9.4
        z_move = 101
        
        x = self.p1.x.magnitude + x_move
        y = self.p1.y.magnitude + y_move
        z = self.p1.z.magnitude + z_move
        
        self.p1.move(x_move, 'x')
        self.p1.move(y_move, 'y')
        self.p1.move(z_move, 'z')

        self.assertAlmostEqual(self.p1.x.magnitude, x, self.dec_places)
        self.assertAlmostEqual(self.p1.y.magnitude, y, self.dec_places)
        self.assertAlmostEqual(self.p1.z.magnitude, z, self.dec_places)
