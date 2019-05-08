import unittest
from geometry.point import Point
from global_attributes.constants import U


class TestPoint(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.p1 = Point(2.5, 1.4, 0.6)
        self.dec_places = 3

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.p1
        
    def testGetters(self):
        """Values should be converted correctly upon initialize"""
        self.assertEqual(self.p1.x, 2.5)
        self.assertEqual(self.p1.y, 1.4)
        self.assertEqual(self.p1.z, 0.6)

    def testSetters(self):
        """Values should be converted correctly upon changing the unit"""
        new_point = [0.0, 100, -4.98]
        self.p1.x = new_point[0]
        self.p1.y = new_point[1]
        self.p1.z = new_point[2]
        self.assertEqual(self.p1.x, new_point[0])
        self.assertEqual(self.p1.y, new_point[1])
        self.assertEqual(self.p1.z, new_point[2])

    def testMovePoint(self):
        """The point should move the correct amount"""
        x_move = 2.3
        y_move = -9.4
        z_move = 101

        x = 4.8
        y = -8
        z = 101.6
        
        self.p1.move(x_move, 'x')
        self.p1.move(y_move, 'y')
        self.p1.move(z_move, 'z')

        self.assertAlmostEqual(self.p1.x, x, self.dec_places)
        self.assertAlmostEqual(self.p1.y, y, self.dec_places)
        self.assertAlmostEqual(self.p1.z, z, self.dec_places)
