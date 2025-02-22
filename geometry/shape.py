"""
Created on Thu Nov 15 19:47:42 2012
...
"""
from geometry.datum import Datum
from utils.unit_utils import load_units, ureg

# Load units from JSON file
units = load_units("./data/aegis_units.json")

class Shape:
    """A generic shape class.
        
    Attributes
    ----------
    size : float
    display_unit : str
    datum : Datum
    """
    
    def __init__(self, size=10.0, unit=units['length']):
        self.size = size * ureg(unit)
        self.display_unit = unit
        self.datum = Datum(unit=unit)
    
    def change_unit(self, new_unit):
        self.size = self.size.to(new_unit)
        self.display_unit = new_unit
        self.datum.convert_units(new_unit)
    
    def set_datum(self, new_elev, unit=units['length']):
        self.datum.set_datum(new_elev, unit)
        self.datum = Datum(new_elev, self.display_unit)