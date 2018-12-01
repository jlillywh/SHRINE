import unittest

# Import all tests here
import test_store_bounds
import test_store_outflow

# Initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add test to the test suite
suite.addTests(loader.loadTestsFromModule(test_store_outflow))
suite.addTests(loader.loadTestsFromModule(test_store_bounds))

# Initialize a runner, pass it the suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
