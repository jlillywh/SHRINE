

class Point:
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
    def __init__(self, x_value, y_value, z_value, unit='ft'):
        self.display_unit = unit
        self._x = x_value
        self._y = y_value
        self._z = z_value
        self.coords = {'x': self._x, 'y': self._y, 'z': self._z}
    
    def coordinates(self):
        """Iterates over the coordinates and returns the value of each"""
        for c in self.coords.values():
            print("%.2f" % c.value)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, new_value):
        self._x = new_value
        self.coords['x'] = new_value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, new_value):
        self._y = new_value
        self.coords['y'] = new_value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, new_value):
        self._z = new_value
        self.coords['z'] = new_value
    
    def set_unit(self, new_unit):
        """Change the unit for the coordinates of the point.
        
            After you change the unit, the values are automatically updated
            
            Parameters
            ----------
            new_unit : str
                The new unit. This name must exist in the Pint library!
            
            """
        self.display_unit = new_unit
        for c in self.coords.values():
            c.unit = new_unit

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
        old_location = self.coords[direction]
        self.coords[direction] = old_location + distance
        self.x = self.coords['x']
        self.y = self.coords['y']
        self.z = self.coords['z']
