import pint

# Set up the units of measurement database
U = pint.UnitRegistry()
U.define('cfs = cu_ft / second')

# Water density at 4 deg C in units of g/cm3
WATER_DENSITY = 1.102 * U.g / U.cm**3

# Gravitational acceleration
G = 9.81 * U.m / U.sec**2
G_english = 32.2

