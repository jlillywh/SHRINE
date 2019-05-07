from geometry.point import Point


class Datum(Point):
    """Class for creating datum coordinates
        
        A datum is a reference point that has a location
        in space along with an elevation based on a geodetic datum """
    def __init__(self, elevation=0, display_unit='ft'):
        Point.__init__(self, display_unit=display_unit)
        self._location = (self.x, self.y)
        self.z = self.to_base_value(elevation)

    @property  # when you do Datum.location, it will call this function
    def location(self):
        return self._location

    @location.setter  # when you do Datum.location = x, it will call this function
    def location(self, x, y):
        self.x = self.to_base_value(x)
        self.y = self.to_base_value(y)
        self._location = (self.x, self.y)
        
    
