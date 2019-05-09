from unittest import TestCase
from water_manage.store import Store


class TestOutflowsCase(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        init_quantity = 10.0
        self.capacity = 15.0
        self.s1 = Store(init_quantity)
        self.s1.capacity = self.capacity
        self.precision = 4
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.s1
        del self.capacity
        del self.precision
    
    def testReducedOutflow(self):
        """Outflow < request when _quantity reaches lower bound"""
        inflow = 0.43
        request = 15.0
        self.s1.update(inflow, request)
        self.assertTrue(self, self.s1.outflow < request)
    
    def testName(self):
        """Check to make sure the name is correct"""
        store_name = 'Big Pond'
        s1 = Store()
        s1.name = store_name
        self.assertEqual(s1.name, store_name)
        del s1
    
    def testUpper(self):
        """Store _quantity == capacity when inflow causes overflow"""
        inflow = 7.43
        outflow = 0.03
        self.s1.update(inflow, outflow)
        self.assertAlmostEqual(self.s1.quantity, self.capacity, self.precision)
    
    def testLower(self):
        """Store _quantity == 0.0 when outflow causes empty"""
        inflow = 0.43
        outflow = 10.438
        self.s1.update(inflow, outflow)
        self.assertAlmostEqual(self.s1.quantity, 0.0, self.precision)
    
    def testSettingQuantity(self):
        """Make sure a new _quantity is limited to the store's bounds"""
        self.s1.quantity = 999.99
        quantity1 = self.s1.quantity
        self.s1.quantity = 1.0
        quantity2 = self.s1.quantity
        self.s1.quantity = 13.8685
        quantity3 = self.s1.quantity
        
        self.assertEqual(quantity1, self.s1.capacity)
        self.assertAlmostEqual(quantity2, 1.0, self.precision)
        self.assertAlmostEqual(quantity3, 13.8685, self.precision)
    
    def testOverflow(self):
        """Make sure the store returns the correct overflow rate.
        """
        inflow = 0.6295
        cumulative_overflow = 0.0
        for i in range(0, 10):
            self.s1.update(inflow, 0)
            cumulative_overflow += self.s1.overflow
        
        self.assertAlmostEqual(cumulative_overflow, 1.295, self.precision)

    def test_quantity(self):
        init_vol = 32.54
        s1 = Store(init_vol)
        self.assertEqual(s1.quantity, init_vol)
        del s1
    
    def test_quantity_setter(self):
        s1 = Store()
        new_vol = 132.54
        s1.quantity = new_vol
        self.assertEqual(s1.quantity, new_vol)
        del s1

