import unittest   # second test

# Import all tests here
from global_attributes.test_aegis import TestAegis
from global_attributes.test_clock import TestClockCase
# TODO add test for model: from global_attributes.test_model import ________
from controllers.test_controller import TestController
from geometry.test_shape import TestShape, TestPoint
from geometry.test_bowl import TestBowl
from geometry.test_circle import TestCircle
from hydraulics.test_pipe import TestPipe
from hydrology.test_awbm import TestBucketCase, TestSurfaceStore
from hydrology.test_catchment import TestCatchment
# TODO add test for: from hydrology.test_junction import ________
from hydrology.test_watershed import TestWatershed
from hydrology.test_wgen import TestWGEN
from inputs.test_data import TestScalar, TestVector
# TODO add test for: from inputs.test_table import _______
# TODO - add new test for: from inputs.test_timeseries import _______
from numerical.test_constructors import TestConstructor
from water_manage.test_allocator import TestAllocator
# TODO add test for: from water_manage.test_network import _______
from water_manage.test_reservoir import TestReservoir
from water_manage.test_store import TestOutflowsCase
from water_manage.test_stores_array import TestStoresCase


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestAegis))
    test_suite.addTest(unittest.makeSuite(TestClockCase))
    test_suite.addTest(unittest.makeSuite(TestController))
    test_suite.addTest(unittest.makeSuite(TestShape))
    test_suite.addTest(unittest.makeSuite(TestBowl))
    test_suite.addTest(unittest.makeSuite(TestCircle))
    test_suite.addTest(unittest.makeSuite(TestPoint))
    test_suite.addTest(unittest.makeSuite(TestPipe))
    test_suite.addTest(unittest.makeSuite(TestBucketCase, TestSurfaceStore))
    test_suite.addTest(unittest.makeSuite(TestCatchment))
    test_suite.addTest(unittest.makeSuite(TestWatershed))
    test_suite.addTest(unittest.makeSuite(TestWGEN))
    test_suite.addTest(unittest.makeSuite(TestScalar, TestVector))
    test_suite.addTest(unittest.makeSuite(TestConstructor))
    test_suite.addTest(unittest.makeSuite(TestReservoir))
    test_suite.addTest(unittest.makeSuite(TestStoresCase))
    test_suite.addTest(unittest.makeSuite(TestOutflowsCase))
    test_suite.addTest(unittest.makeSuite(TestAllocator))
    return test_suite


mySuit = suite()

runner = unittest.TextTestRunner(verbosity=3)
runner.run(mySuit)


