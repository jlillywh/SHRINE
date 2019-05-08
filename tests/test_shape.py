from unittest import TestCase
from geometry.shape import Shape


class TestShape(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        size = 65.0
        self.s = Shape(size)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.s
        
    def test_centroid(self):
        centroid = 65 / 2.0
        self.assertEqual(self.s.centroid()[0], centroid)
