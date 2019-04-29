import pint
from iapws import IAPWS97
from global_attributes.set_label import SetLabel

# Set up the array label sets used for the model
ArrayLabelSet = SetLabel()
Months = ArrayLabelSet.get_list('Months')

# Set up the units of measurement database
# I am using auto reduction of dimensions but this could be expensive so be aware!
U = pint.UnitRegistry(auto_reduce_dimensions=True)

# load the custom units file
try:
    U.load_definitions('..\\data\\aegis_units.txt')
except ValueError:
    U.load_definitions('.\\data\\aegis_units.txt')

# Water density at 4 deg C in units of g/cm3
WATER_DENSITY = 1.102 * U.g / U.cm**3

# Water kinematic viscosity at 60 deg F
water_temp = U.Quantity(60.0, 'degF').to('degC')
water=IAPWS97(T=water_temp.magnitude+273.15, x=0.0)

# Kinematic viscosity in units of m2/s
nu = U.Quantity(water.Liquid.nu, 'm^2/s')

# Gravitational acceleration
G = 9.81 * U.m / U.sec**2
G_english = 32.2

# Default time step
TS = 1 * U.day
