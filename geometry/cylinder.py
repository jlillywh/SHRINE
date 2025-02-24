from geometry.shape import Shape
import math

class Cylinder(Shape):
    """A cylinder shape, typically used for tanks.
    
    Attributes
    ----------
    radius : float
    height : float
    """
    
    def __init__(self, radius=1.0, height=1.0, unit='m'):
        super().__init__(size=radius*2, unit=unit)
        self.radius = radius * self.size.units
        self.height = height * self.size.units
    
    def area(self):
        # Surface area of the cylinder cross section (πr^2)
        return math.pi * self.radius ** 2
    
    def volume(self):
        # Volume of the cylinder (πr^2h)
        return math.pi * self.radius ** 2 * self.height
    
    def change_unit(self, new_unit):
        super().change_unit(new_unit)
        self.radius = self.radius.to(self.size.units)
        self.height = self.height.to(self.size.units)
        self.datum.change_units(self.size.units)