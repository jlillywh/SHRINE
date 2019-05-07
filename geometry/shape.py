"""
Created on Thu Nov 15 19:47:42 2012

@author: jlillywhite
"""
from geometry.datum import Datum
from global_attributes.aegis import Aegis
from global_attributes.constants import U


class Shape(Aegis):
    """A shape that is symmetrical in both axes.
        
        It has a datum that defines the lower left corner of
        the object.
        
        Attributes
        ----------
        size : flt
    """
    
    def __init__(self, size=10.0, display_unit='m'):
        Aegis.__init__(self, display_unit=display_unit)
        self._size = self.to_base_value(size)
        self.datum = Datum(display_unit=display_unit)
        self.location = self.datum.location
    
    def getXt(self):
        # Horizontal coordinate of the Right side of the shape
        return self.width + self.get_x()
    
    def getYt(self):
        # Vertical coordinate of the Top side of the shape
        return self.size + self.getY()
    
    def setWidth(self, value):
        # Horizontal extent of the shape
        self.width = U._build_quantity(value, self.disp_unit)
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, new_size):
        self._size = new_size * self._size.units
        
    def set_unit(self, new_unit):
        self.datum.set_unit(new_unit)
        self._size.to(new_unit)
    
    def centroid(self):
        # Centroid coordinates
        self.xc = self.x + self.xt / 2.0
        self.yc = self.y + self.yt / 2.0
        return [self.xc, self.yc]
    
    def set_datum(self, x=0, y=0):
        self.datum = Datum(x, y)
        self.x = self.datum.get_x()
        self.y = self.datum.getY()
    
    def ic(self):
        # Moment of Inertia
        return 0
    
    def test_me(self):
        print("This " + str(self.shape) + "'s datum is at " + str(self.datum) + " and size of " + str(self.size))
        print('The centroid is ' + str(self.centroid))
        self.datum = [2, 1]
        print("The datum has been reassigned to " + str(self.datum))
        print("The vertical componant of the datum is " + str(self.y))
