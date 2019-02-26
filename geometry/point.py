"""
Cass for creating and managing geometric point objects
Author: Jason Lillywhite
Date: March, 2013
"""
from global_attributes.aegis import Aegis
from inputs.constants import U


class Point(Aegis):
    def __init__(self, x=0, y=0, z=0):
        self._x = x * U.meter
        self._y = y * U.meter
        self._z = z * U.meter
    
    def coordinates(self):
        return [self._x, self._y, self._z]
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value * self._x.units
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value * self._y.units

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value * self._z.units
    
    def set_unit(self, disp_unit):
        while True:
            try:
                self._x = self._x.to(disp_unit)
                self._y = self._y.to(disp_unit)
                self._z = self._z.to(disp_unit)
                break
    
            except ValueError:
                print("Oops!  That was no valid unit.  Try again...")
                break
    
    # Find the quadrant in which the point is located in
    def quadrant(self):
        x, y = self._x, self._y
    
        if x == 0 and y == 0:
            return 0
        elif x > 0 and y >= 0:
            return 1
        elif x <= 0 and y > 0:
            return 2
        elif x < 0 and y <= 0:
            return 3
        else:
            return 4


#Testing
'''
p1 = Point(1, -3)
p2 = Point(3.4, 0)

print p1.coordinates()
print p2.quadrant()
'''