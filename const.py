from aegis import Aegis

class Const(Aegis):
    """Class for creating constant data for a model.
        
        These objects are intended to be defined at run time
        but not changed after that point.
        
    Attributes
    ----------
    name : str
        What the object represents
    unit : str
        The type of unit used to define the data
    data : float
        The value of the data
    description : str
        A short description of the data (what does it represent?
    
    Methods
    -------
    set_data(value)
        set the value of the data without changing the unit
        
    print()
        Prints the value followed by the unit as a string
    """
    
    def __init__(self, data=0.0, **kwargs):
        """ Initialize the constant with zero data
        
        Parameters
        ----------
        name : str
            What the object represents. class name followed by
            id is the default
        data : float or list(float)
            The value of the data is initialized at zero
        unit : str
        description : str
        
        """
        
        Aegis.__init__(self)
        if('name' in kwargs ):
            self.name = kwargs['name']
        else:
            self.name = self.class_name + " " + str(self.id)
        if ('unit' in kwargs):
            self.unit = kwargs['unit']
        else:
            self.unit = None
        if ('description' in kwargs):
            self.description = kwargs['description']
        else:
            self.description = self.about
        self.data = data
        
    def print(self):
        return str(self.data) + " " + self.unit