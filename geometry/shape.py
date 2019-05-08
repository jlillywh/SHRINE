"""
Created on Thu Nov 15 19:47:42 2012

@author: jlillywhite
"""
from geometry.datum import Datum


class Shape:
    """A shape that is symmetrical in both axes.
        
        It has a datum that defines the lower left corner of
        the object.
        
        Attributes
        ----------
        size : flt
    """
    
    def __init__(self, size=10.0, unit='m'):
        self.size = size
        self.display_unit = unit
        self.datum = Datum(unit=unit)
    
    def get_xt(self):
        # Horizontal coordinate of the Right side of the shape
        return self.datum.x + self.size
    
    def get_yt(self):
        # Vertical coordinate of the Top side of the shape
        return self.datum.y + self.size
    
    def centroid(self):
        # Centroid coordinates
        xc = self.datum.x + self.size / 2.0
        yc = self.datum.y + self.size / 2.0
        centroid = (xc, yc)
        return centroid
    
    def set_datum(self, new_elev=100.0, new_x=0, new_y=0):
        self.datum = Datum(new_elev, new_x, new_y, self.display_unit)
    
    def ic(self):
        # Moment of Inertia
        return 0
    
    
