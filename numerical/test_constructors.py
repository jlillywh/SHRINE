import unittest
from numerical.constructors import vector
import numpy as np


class TestConstructor(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.old_vector = [5, 4, 3, 2, 1]
        self.v1 = [True] * 5
        self.v2 = 4
        self.v3 = [3, 4, 2, 3, 3]
        self.if_true = "Hi"
        self.if_false = "shit!"

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.old_vector
        del self.v1
        del self.v2
        del self.v3
        del self.if_true
        del self.if_false

    def testVectorConstruct(self):
        expected_array = ["shit!", "Hi", "shit!", "shit!", "shit!"]
        new_array = vector(self.old_vector, self.v1, self.v2, self.v3, if_true =self.if_true, if_false=self.if_false)
        np.testing.assert_equal(expected_array, new_array)