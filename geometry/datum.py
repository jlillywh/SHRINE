from geometry.point import Point


class Datum:
    """Class for creating datum coordinates
        
        A datum is a reference point that has a location
        in space along with an elevation based on a geodetic datum """
    def __init__(self, elev=0, lat=40.0, long=101.3, unit='ft'):
        self.latitude = lat
        self.longitude = long
        self.display_unit = unit
        self._location = (self.latitude, self.longitude)
        self.elevation = elev
