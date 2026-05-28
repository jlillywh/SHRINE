"""
Created on Thu Nov 15 19:47:42 2012
...
"""
from geometry.datum import Datum
from shrine.units import get_default_units, get_unit_registry


class Shape:
    """A generic shape class.
        
    Attributes
    ----------
    size : float
    display_unit : str
    datum : Datum
    """
    
    def __init__(self, size=10.0, unit=None):
        if unit is None:
            unit = get_default_units()["length"]
        ureg = get_unit_registry()
        self.size = size * ureg(unit)
        self.display_unit = unit
        self.datum = Datum(unit=unit)
    
    def change_unit(self, new_unit):
        self.size = self.size.to(new_unit)
        self.display_unit = new_unit
        self.datum.change_units(new_unit)
    
    def set_datum(self, new_elev, unit=None):
        if unit is None:
            unit = get_default_units()["length"]
        self.datum.set_datum(new_elev, unit)
        self.datum = Datum(new_elev, self.display_unit)