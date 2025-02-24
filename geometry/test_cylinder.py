from unittest import TestCase
from geometry.cylinder import Cylinder
from utils.unit_utils import load_units, ureg
import math

# Load units from JSON file
units = load_units("./data/aegis_units.json")

class TestCylinder(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.cylinder = Cylinder(radius=2.0, height=5.0, unit=units['length'])

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.cylinder
        
    def test_area(self):
        """Test the area calculation"""
        expected_area = math.pi * self.cylinder.radius ** 2
        self.assertAlmostEqual(self.cylinder.area().magnitude, expected_area.magnitude, places=3)
        
    def test_volume(self):
        """Test the volume calculation"""
        expected_volume = math.pi * self.cylinder.radius ** 2 * self.cylinder.height
        self.assertAlmostEqual(self.cylinder.volume().magnitude, expected_volume.magnitude, places=3)

    def test_change_units(self):
        """Test unit conversion"""
        self.cylinder.change_unit('ft')
        expected_radius = 2.0 * ureg(units['length']).to('ft')
        expected_height = 5.0 * ureg(units['length']).to('ft')
        self.assertAlmostEqual(self.cylinder.radius.magnitude, expected_radius.magnitude, places=3)
        self.assertAlmostEqual(self.cylinder.height.magnitude, expected_height.magnitude, places=3)
        self.assertEqual(self.cylinder.display_unit, 'ft')

    def test_set_datum(self):
        """Test setting a new datum"""
        self.cylinder.set_datum(new_elev=200.0)
        self.assertEqual(self.cylinder.datum.elevation, 200.0 * ureg(units['length']))

if __name__ == "__main__":
    unittest.main()