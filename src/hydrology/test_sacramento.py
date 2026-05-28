import unittest
from hydrology.sacramento import Sacramento
import numpy as np

class TestSacramento(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested

            Compare results to GoldSim model: AWBM Verification.gsm"""
        init_states = {'uztwc': 60.0,
                       'uzfwc': 0.5,
                       'lztwc': 100.0,
                       'lzfsc': 11.0,
                       'lzfpc': 47.0,
                       'adimc': 160.0
                       }
        
        params = {'uztwm': 40.0,    #default
                  'uzfwm': 30.0,    #default
                  'lztwm': 330.0,   #default
                  'lzfpm': 40.0,    #default
                  'lzfsm': 15.0,    #default
                  'uzk': 0.4,       #default
                  'lzpk': 0.005,    #default
                  'lzsk': 0.1,      #default
                  'zperc': 150.0,   #default
                  'rexp': 2.0,      #default
                  'pfree': 0.1,     #default
                  'pctim': 0.0,     #default
                  'adimp': 0.0,     #default
                  'riva': 0.01,     #default
                  'side': 0.0,      #default
                  'rserv': 0.3      #default
                  }
        
        globals = {'pxv': 2.5,
                   'isc': 1.0,
                   'aesc': 1.0
                   }
        self.s1 = Sacramento(init_states, params, globals)
        self.precision = 2
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.s1
        del self.precision
    
    def testET(self):
        p = [0,2,4,8,16,32,0,0,0,0,0,0,0]
        et = 1.5
        for i in range(10):
            self.s1.update(p[i], et)
        self.assertAlmostEqual(self.s1.tci, 0.152, self.precision)