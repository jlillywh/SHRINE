from global_attributes.aegis import Aegis
from global_attributes.set_label import SetLabel
from inputs.constants import U


class Scalar(Aegis):
    """Class for creating constant data for a model.
        
        These objects are intended to be defined at run time
        but not changed after that point.
        
    Attributes
    ----------
    name : str
        What the object represents
    unit : pint unit
        The type of unit used to define the data
        TODO: Add pint units library usage
    data : pint Quantity
        The value of the data with units of measurement
    magnitude: float
        The value of the data only.
    description : str
        A short description of the data (what does it represent?
    
    Methods
    -------
    set_data(value)
        set the value of the data without changing the unit
        
    print()
        Prints the value followed by the unit as a string
    """
    
    def __init__(self, value=0.0, **kwargs):
        """ Initialize the constant with zero data
        
        Parameters
        ----------
        name : str
            What the object represents. class name followed by
            id is the default
        value : float or list(float) or dict(str : float)
            The value of the data is initialized at zero
        unit : str
        description : str
        
        """
        
        Aegis.__init__(self)
        self._value = value
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = self.class_name + " " + str(self.id)
        if 'unit' in kwargs:
            self._unit = U.parse_expression(kwargs['unit'])
            self.data = self._value * self._unit
        else:
            self._unit = None
            self.data = self._value
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = self.about

    def show(self):
        print(self.data)

    @property
    def magnitude(self):
        return self._value

    @magnitude.setter
    def magnitude(self, new_magnitude):
        self._value = new_magnitude
        self.data = self._value * self._unit

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        while True:
            try:
                self._unit = U.parse_expression(new_unit)
                break
            except ValueError:
                print("Oops!  That was no valid unit.  Try again...")
                break
        
        while True:
            try:
                self.data = self.data.to(self._unit)
                self._value = self.data.magnitude
                break
            except AttributeError:
                self.data = self.data * self._unit
                break
    
    def __mult__(self, other):
        new_data = (self.data * other.data).to_base_units()
        
    
class Vector(Aegis):
    """Class used to create objects that allow you to store
        constant data in a 1 dimensional array.
        
        Attributes
        ----------
        values : list(float)
        index : SetLabel
        
        Methods
        -------
        get_item(key name) : returns float
        
    """
    def __init__(self, name, unit='', value_list=[0] * 12, label_set='Months'):
        """Create a vector using list and array label set name
        
            The standard constructor takes a list of values and a named label set
            The label set must be in the list.
            Units are optional
            
            Parameters
            ----------
            name : str
            unit : str (optional)
            value_list : list
            label_set : str (default months of the year, "Months")
                Name of the label set used for the index
        """
        Aegis.__init__(self)
        self.name = name
        self.unit = unit
        self.listSet = label_set
        array_label_sets = SetLabel()
        self.index = array_label_sets.get_list(label_set)
        self.values = value_list
        
    def get_item(self, name):
        """Give the name of the index and return the value."""
        idx = self.index.index(name)
        return self.values[idx]

    def __getitem__(self, name):
        """Give the name of the index and return the value."""
        idx = self.index.index(name)
        return self.values[idx]
