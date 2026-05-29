"""DEPRECATED: Colocated unittest — migrate to tests/global_attributes/ (roadmap 2.11)."""

from __future__ import annotations

from testing.colocated import deprecate_colocated_module

deprecate_colocated_module(
    path="global_attributes.test_shrine_object",
    migrated_to="tests/global_attributes/ (pending)",
)

from unittest import TestCase
from global_attributes.shrine_object import ShrineObject


class TestShrineObject(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.a = ShrineObject("my_block", "A building block made of wood")

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.a

    def test_name(self):
        self.assertEqual(self.a.name, "my_block")
