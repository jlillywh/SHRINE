import unittest
from water_manage.store import Store

class TestOutflowsCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.store_name = "Reservoir01"
        init_quantity = 10.0
        self.capacity = 15.0
        self.s1 = Store(init_quantity, self.capacity)
        self.s1.name = self.store_name

        #print("Test: " + str(self.s1.getInstanceCount()))

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.s1).__name__)
        del self.s1

    def testReducedOutflow(self):
        """Outflow < request when _quantity reaches lower bound"""
        inflow = 0.43
        request = 15.0
        self.s1.update(inflow, request)
        self.assertTrue(self, self.s1.outflow < request)

class TestStoreBoundsCase(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.store_name = "Reservoir01"
        init_quantity = 10.0
        self.capacity = 15.0
        self.s1 = Store(init_quantity, self.capacity)
        self.s1.name = self.store_name
        self.precision = 3
        #print("Test: " + str(self.s1.getInstanceCount()))

    def tearDown(self):
        """Destroy the object after running tests"""
        #print("Tear down " + type(self.s1).__name__)
        del self.s1

    def testName(self):
        """Check to make sure the name is correct"""
        self.assertEqual(self.s1.name, self.store_name)

    def testUpper(self):
        """Store _quantity == capacity when inflow causes overflow"""
        inflow = 7.43
        outflow = 0.03
        self.s1.update(inflow, outflow)
        self.assertEqual(self.s1.quantity, self.capacity)

    def testLower(self):
        """Store _quantity == 0.0 when outflow causes empty"""
        inflow = 0.43
        outflow = 10.438
        self.s1.update(inflow, outflow)
        self.assertEqual(self.s1.quantity, 0.0)

    def testSettingQuantity(self):
        """Make sure a new _quantity is limited to the store's bounds"""
        self.s1.quantity = 999.99
        quantity1 = self.s1.quantity
        self.s1.quantity = -100.0
        quantity2 = self.s1.quantity
        self.s1.quantity = 13.8685
        quantity3 = self.s1.quantity

        self.assertEqual(quantity1, self.s1.capacity)
        self.assertEqual(quantity2, 0.0)
        self.assertEqual(quantity3, 13.8685)

    def testOverflow(self):
        """Make sure the store returns the correct overflow rate.
        """
        inflow = 0.6295
        cumulative_overflow = 0.0
        for i in range(0,10):
            self.s1.update(inflow)
            cumulative_overflow += self.s1.overflow

        self.assertAlmostEqual(cumulative_overflow, 1.295, self.precision)



if __name__ == '__main__':
    unittest.main()