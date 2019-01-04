import unittest

# Import all tests here
import test_store
import test_awbm
import test_stores_array
import test_clock
import test_catchment
import test_watershed
import test_wgen

# Initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add test to the test suite
suite.addTests(loader.loadTestsFromModule(test_store))
suite.addTests(loader.loadTestsFromModule(test_awbm))
suite.addTests(loader.loadTestsFromModule(test_stores_array))
suite.addTests(loader.loadTestsFromModule(test_clock))
suite.addTests(loader.loadTestsFromModule(test_catchment))
suite.addTests(loader.loadTestsFromModule(test_watershed))
suite.addTests(loader.loadTestsFromModule(test_wgen))

# Initialize a runner, pass it the suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
