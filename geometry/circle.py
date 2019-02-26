# A class for creating circle objects
"""
Created on Thu Nov 15 19:38:31 2012

@author: jlillywhite
"""
from geometry.shape import Shape
from utils.attr_setter import AttrMap
from geometry.datum import Datum
import math


class Circle(Shape):
    diameter = AttrMap('size')
    
    def __init__(self, size, datum=Datum()):
        Shape.__init__(self, size, datum)
        self.shape = 'circle'
        self.radius = self.radius()
    
    def xt(self):
        # Width
        return self.diameter
    
    def yt(self):
        # Height
        return self.diameter
    
    def area(self):
        return math.pi * self.diameter ** 2 / 4.0
    
    def circumference(self):
        return math.pi * self.diameter
    
    def radius(self):
        return self.diameter / 2.0
    
    def ic(self):
        # Moment of inertia
        return math.pi * self.diameter ** 4 / 64.0
    
    def rg(self):
        # Radius of gyration
        return self.diameter / 4.0
    
    def j(self):
        # Polar moment of inertia
        return math.pi * self.diameter ** 4 / 32.0
    
    def test_me(self):
        print("This " + str(self.shape) + " has a radius of " + str(self.radius) + " and area of " + str(self.area), '\n')
        print("Diameter is " + str(self.diameter) + " and Moment of Inertia is " + str(self.ic), '\n')
        print("The datum is " + str(self.datum), ' and centroid at ' + str(self.centroid))

