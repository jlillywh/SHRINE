import unittest
from clock import Clock
from wgen import Wgen

class TestWGEN(unittest.TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.obs = [1.41, 1.68, 2.51, 3.63, 4.45, 4.15, 3.95,
                    2.84, 4.00, 3.12, 1.58, 1.66]
        self.c = Clock()
        self.w = Wgen()
        self.precision = 0
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.w
    
    def testDetermWGEN(self):
        self.w.rain_deterministic = 0.05
        self.w.markov_deterministic = 0.177
        rain = self.w.precipitation()
        self.assertEqual(rain, self.w.alpha_array[0])
    
    def test1monthRain(self):
        realizations = 200
        total_precip = 0.0
        self.c.set
        self.w.rain_deterministic = -1
        self.w.markov_deterministic = -1
        self.w.min_rain = 0.0
        for i in range(0,realizations):
            precip =  self.w.precipitation(self.c.current_date)
            total_precip += precip
            
        total_precip = (total_precip / realizations) * 31
        
        self.assertAlmostEqual(total_precip, self.obs[0], self.precision)
    
    def testMonthlyRain(self):
        """Check cumulative rain avg"""
        rain_array = [0.0] * 12
        realizations = 100
        for i in range(1, realizations):
            self.c.set_start_date('1/1/2019')
            while self.c.running:
                month = self.c.current_date.month - 1
                precip = self.w.precipitation(self.c.current_date)
                rain_array[month] += precip
                self.c.advance()
        
        for i in range(0, 12):
            rain_array[i] /= realizations
        
        for i in range(0, 12):
            self.assertAlmostEqual(rain_array[i], self.obs[i], self.precision)

if __name__ == '__main__':
    unittest.main()