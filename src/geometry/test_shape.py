from unittest import TestCase

from geometry.datum import Datum
from geometry.shape import Shape
from shrine.units import get_default_units, get_unit_registry

units = get_default_units()
ureg = get_unit_registry()

class TestShape(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        size = 65.0
        self.s = Shape(size, unit=units['length'])

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.s
        
    def test_convert_units(self):
        """Test unit conversion"""
        self.s.change_unit('ft')
        self.assertAlmostEqual(self.s.size.magnitude, 65.0 * ureg(units['length']).to('ft').magnitude, places=3)
        self.assertEqual(self.s.display_unit, 'ft')

    def test_set_datum(self):
        """Test setting a new datum"""
        self.s.set_datum(new_elev=100.0)
        self.assertEqual(self.s.datum.elevation, 100.0 * ureg(units['length']))

class TestDatum(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.d = Datum(elev=100.0, unit=units['length'])

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.d

    def test_convert_units(self):
        """Test unit conversion"""
        self.d.change_units('ft')
        self.assertAlmostEqual(self.d.elevation.magnitude, 100.0 * ureg(units['length']).to('ft').magnitude, places=3)
        self.assertEqual(self.d.display_unit, 'ft')