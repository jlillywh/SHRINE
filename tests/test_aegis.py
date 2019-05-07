from unittest import TestCase
from global_attributes.aegis import Aegis
from global_attributes.constants import U


class TestAegis(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.a = Aegis('my_block', 'A building block made of wood', 'foot')
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.a
    
    def test_value_at_unit(self):
        value = 3.41
        value_si = value * U.m
        value_unit = self.a.value_at_unit(value)
        self.assertEqual(value_unit, value_si.to('ft').magnitude)

    def test_to_base_value(self):
        value_display = 3.41
        value_display_units = value_display * self.a.display_unit
        value_base = self.a.to_base_value(value_display)
        self.assertEqual(value_base, value_display_units.to(self.a.base_unit).magnitude)
        
