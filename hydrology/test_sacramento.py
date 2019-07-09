import unittest
from hydrology.sacramento import Sacramento


class TestSacramento(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested

            Compare results to GoldSim model: AWBM Verification.gsm"""
        init_states = {'uztwc': 0.0,
                       'uzfwc':0.0,
                       'lztwc':20.0,
                       'lzfsc': 10.0,
                       'lzfpc': 10.0,
                       'adimc':0.0
                       }
        
        params = {'uztwm': 50.0,
                  'uzfwm': 40.0,
                  'lztwm': 130.0,
                  'lzfpm': 60.0,
                  'lzfsm': 25.0,
                  'uzk': 0.3,
                  'lzpk': 0.01,
                  'lzsk': 0.05,
                  'zperc': 40.0,
                  'rexp': 1.0,
                  'pfree': 0.06,
                  'pctim': 0.01,
                  'adimp': 0.0,
                  'riva': 0.4,
                  'side': 0.0,
                  'saved': 1.0,
                  'rserv': 0.3
                  }
        
        globals = {'kint': 1,
                   'pxv': 1.0,
                   'pcti': 1.0,
                   'simpvt': 1.0,
                   'dt': 1.0,
                   'ifrze': 0.0
                   }
        self.s1 = Sacramento(init_states, params, globals)
        self.precision = 2
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.s1
        del self.precision
    
    def testUpdateCompCapacity(self):
        """New bucket capacity == user defined array"""
        new_buckets = [0.05743, 0.14333, 0.29849]
        self.a1.set_comp_capacity(new_buckets)
        for i in range(len(new_buckets)):
            self.assertEqual(self.a1.buckets.stores[i].capacity, new_buckets[i] * self.a1.partial_area_fraction[i])

