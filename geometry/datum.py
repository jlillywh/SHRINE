#Class for creating datum coordinates
#Accept up to 2 arguments but no more.

from geometry.point import Point


class Datum(Point):
    def __init__(self, elevation=0):
        Point.__init__(self)
        self._location = (self._x, self._y)
        self._z = elevation * self._z.units

    @property  # when you do Datum.elevation, it will call this function
    def elevation(self):
        return self._z
    
    @elevation.setter   # when you do Datum.elevation = x, it will call this function
    def elevation(self, new_elevation):
        self._z = new_elevation * self._z.units

    @property  # when you do Datum.location, it will call this function
    def location(self):
        return self._location

    @location.setter  # when you do Datum.location = x, it will call this function
    def location(self, new_location):
        self._x = new_location[0] * self._x.units
        self._y = new_location[1] * self._y.units
        self._location = (self._x, self._y)
        
    
