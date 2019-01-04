import unittest
from clock import Clock
from wgen import Wgen

class TestWGEN(unittest.TestCase):
	def setUp(self):
		"""Set up a new object to be tested"""
		self.c = Clock()
		self.w = Wgen()
		self.precision = 0

	def tearDown(self):
		"""Destroy the object after running tests"""
		del self.w

	def testMonthlyRain(self):
		"""Check cumulative rain avg"""
		rain_f_array = [1.27, 1.68, 2.97, 3.4, 4.12, 4.79,
		                4.43, 3.14, 3.94, 3.36, 1.73, 1.86]
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
			self.assertAlmostEqual(rain_array[i], rain_f_array[i], self.precision)

if __name__ == '__main__':
	unittest.main()