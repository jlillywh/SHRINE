from unittest import TestCase
from geometry.shape import Shape
from geometry.datum import Datum
from utils.unit_utils import load_units, ureg

# Load units from JSON file
units = load_units("./data/aegis_units.json")

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