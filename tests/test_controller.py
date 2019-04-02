import unittest
from controllers.onoff import OnOff
from inputs.constants import U


class TestScalar(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        direction = 'UP'
        set_point = 7.6 * U.m
        self.c1 = OnOff(direction, set_point)

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.c1

    def testChangeUnit(self):
        right_answers = 0
        measurement = 7.9 * U.m
        self.c1.update(measurement)     # This makes status false
        measurement = 7.3 * U.m
        if self.c1.update(measurement):
            right_answers += 1
        measurement = 7.8 * U.m
        if self.c1.update(measurement):
            right_answers += 1
        measurement = 7.89 * U.m
        if not self.c1.update(measurement):
            right_answers += 1
        measurement = 7.93 * U.m
        if not self.c1.update(measurement):
            right_answers += 1
        measurement = 7.8 * U.m
        if not self.c1.update(measurement):
            right_answers += 1
        measurement = 7.5 * U.m
        if not self.c1.update(measurement):
            right_answers += 1
        measurement = 7.4 * U.m
        if not self.c1.update(measurement):
            right_answers += 1
        measurement = 7.3 * U.m
        if self.c1.update(measurement):
            right_answers += 1
        
        self.assertEqual(right_answers, 8)
