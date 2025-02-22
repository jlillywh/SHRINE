from utils.unit_utils import ureg

class Datum:
    """Class for creating datum coordinates
        
        A datum is a reference point that has a location
        in space along with an elevation based on a geodetic datum """
    def __init__(self, elev=0.0, unit='m'):
        self.display_unit = unit
        self.elevation = elev * ureg(unit)

    def set_datum(self, new_elev=0.0, unit='m'):
        self.display_unit = unit
        self.elevation = new_elev * ureg(self.display_unit)
    
    def convert_units(self, new_unit):
        self.elevation = self.elevation.to(new_unit)
        self.display_unit = new_unit