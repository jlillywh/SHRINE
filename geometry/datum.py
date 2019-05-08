

class Datum:
    """Class for creating datum coordinates
        
        A datum is a reference point that has a location
        in space along with an elevation based on a geodetic datum """
    def __init__(self, elev=0.0, x=0.0, y=0.0, unit='ft'):
        self.x = x
        self.y = y
        self.display_unit = unit
        self.location = (self.x, self.y)
        self.elevation = elev
