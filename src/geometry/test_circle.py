from unittest import TestCase
from geometry.circle import Circle
import math


class TestCircle(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        dia = 65.0
        self.c = Circle(dia)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.c
        
    def test_area(self):
        area = math.pi * 65**2 / 4
        self.assertEqual(self.c.area(), area)
