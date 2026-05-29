"""DEPRECATED: Colocated unittest — migrate to tests/geometry/ (roadmap 2.11)."""

from __future__ import annotations

from testing.colocated import deprecate_colocated_module

deprecate_colocated_module(path="geometry.test_circle", migrated_to="tests/geometry/ (pending)")

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
