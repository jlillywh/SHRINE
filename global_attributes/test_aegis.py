from unittest import TestCase
from global_attributes.aegis import Aegis
import numpy as np


class TestAegis(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.a = Aegis('my_block', 'A building block made of wood')
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.a
    
    def test_name(self):
        self.assertEqual(self.a.name, 'my_block')
