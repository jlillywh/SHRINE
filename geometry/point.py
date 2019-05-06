from global_attributes.aegis import Aegis


class Point(Aegis):
    """A class to create a new point in a 3-dimensional space.
    
        This point has x, y, z coordinates in terms of length magnitude
        and also a unit dimension for the magnitude of each. Each
        coordinate is labeled 'x', 'y', and 'z' for convenience.
    
    Parameters
    ----------
    x, y, z: int or float with dimensions
        Coordinates of the point. Defaults are zero. For 2-dimensions, z = 0
        The default unit is meters.
    coords : dictionary of x, y, and z
        Dictionary of values that represent the x, y, z coordinate values
        Values also have unit dimensions of length
    unit : str
        specify the unit name for all coordinates of the point.
        
    Methods
    -------
    set_unit(disp_unit)
        Allows the user to set a new unit and value is automatically converted
        
    """
    def __init__(self, x=0, y=0, z=0, unit='ft'):
        Aegis.__init__(self, unit=unit)
        x = self.to_base_value(x)
        y = self.to_base_value(y)
        z = self.to_base_value(z)
        self.coords = {'x': x, 'y': y, 'z': z}
    
    def coordinates(self):
        """Iterates over the coordinates and returns the value of each"""
        for c in self.coords:
            value = self.coords[c] * self.base_unit
            value = value.to(self.unit).magnitude
            print("%.2f" % value)
    
    @property
    def x(self):
        return self.coords['x']
    
    @x.setter
    def x(self, value):
        value = self.to_base_value(value)
        self.coords['x'] = value
    
    @property
    def y(self):
        return self.coords['y']
    
    @y.setter
    def y(self, value):
        value = self.to_base_value(value)
        self.coords['y'] = value

    @property
    def z(self):
        return self.coords['z']

    @z.setter
    def z(self, value):
        value = self.to_base_value(value)
        self.coords['z'] = value
    
    def set_unit(self, disp_unit):
        """Change the unit for the coordinates of the point.
        
            After you change the unit, the values are automatically updated
            
            Parameters
            ----------
            disp_unit : str
                The new unit. This name must exist in the Pint library!
            
            Exceptions
            ----------
            ValueError
                If the unit name is not found, an error is printed and the
                values/unit remain unchanged
            """
        
        while True:
            try:
                unit = (1 * self.base_unit).to(disp_unit).units
                for c in self.coords:
                    value = self.coords[c] * self.base_unit
                    value = value.to(self.unit).magnitude
                    value = value * unit
                    self.coords[c] = value.to(self.base_unit).magnitude
                self.unit = unit
                break
    
            except ValueError:
                print("Oops!  That was no valid unit.  Try again...")
                break

    def move(self, distance, direction):
        """Move the point by a distance in a direction
        
            Parameters
            ----------
            distance : float
                The magnitude of the change in length.
            direction : str
                A label for the direction based on x,y,z coordinates.
                For x, positive value is to the right, negative is left
                for y, positive = up, negative = down
                for z, positive = away from you, negative = toward you
                
        """
        
        self.coords[direction] += self.to_base_value(distance)
