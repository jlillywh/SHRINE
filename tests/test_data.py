import unittest
from inputs.data import Scalar


class TestScalar(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.s1 = Scalar(2.57, unit='in/day')
        self.dec_places = 3

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.s1

    def testChangeUnit(self):
        """Values should be converted correctly upon changing the unit"""
        new_unit = 'mm/day'
        s2 = self.s1
        s2.unit = new_unit
        self.assertAlmostEqual(s2.magnitude, 65.278, self.dec_places)

    def testChangeMagnitude(self):
        new_value = 3.1416
        s2 = self.s1
        s2.magnitude = new_value
        s2_si = s2.data.to_base_units()
        self.assertAlmostEqual(s2_si.magnitude, 9.236e-7, self.dec_places)