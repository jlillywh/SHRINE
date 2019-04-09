from global_attributes.aegis import Aegis
from global_attributes.set_label import SetLabel
from inputs.constants import U, ArrayLabelSet
import pandas as pd
import numpy as np
import copy


class Scalar(Aegis):
    """Class for creating constant data for a model.
        
        These objects are intended to be defined at run time
        but not changed after that point.
        
    Attributes
    ----------
    unit : pint Quantity unit
        The type of unit used to define the data
    data : pint Quantity
        The value of the data with units of measurement
    magnitude: float
        The value of the data only.
    description : str
        A short description of the data (what does it represent?
    
    Methods
    -------
    magnitude()
        setter function to set the value of the data without changing the unit
    unit()
        setter function to set the new unit. The magnitude of the value is
        converted automatically
    show()
        Prints the value followed by the unit as a string
    """
    
    def __init__(self, value=0.0, **kwargs):
        """ Initialize the constant with zero data
        
        Parameters
        ----------
        value : float
            Default is 0.0
        unit : str
        description : str
            What the object represents.
        
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
            self.data = self._valuen * self._unit
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
        unit : pint Quantity Unit
        data : pandas DataFrame
        magnitude : list(float)
        
        Methods
        -------
        unit
            setter method (vector.unit = 'm')
            
        magnitude
            set magnitude with ndarray
            
        get_item(key name) : returns float
    """
    
    def __init__(self, value_list=[0] * 12, unit=None, label_set='Months'):
        """Create a vector using list and array label set name
        
            The standard constructor takes a list of values and a named label set
            The label set must be in the list.
            Units are optional
            
            Parameters
            ----------
            unit : str (optional)
            value_list : list
            #TODO make sure value_list length == label_set_array length
            label_set : str (default months of the year, "Months")
                Name of the label set used for the index
        """
        
        Aegis.__init__(self)
        self.listSet = label_set
        self._magnitude = np.asarray(value_list)
        v = [0] * len(value_list)
        if unit:
            self._unit = U.parse_expression(unit)
            for i in range(value_list.shape[0]):
                v[i] = value_list[i] * self._unit
    
        self.data = ArrayLabelSet.get_list(label_set)
        self.data['Values'] = pd.Series(v, index=self.data.index)

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, new_magnitude):
        """Sets the magnitude of all values
        
            Parameters
            ----------
            new_magnitude : numpy array
        """
        
        self._magnitude = np.asarray(new_magnitude)
        v = [0] * len(new_magnitude)
        for i in range(len(new_magnitude)):
            v[i] = new_magnitude[i] * self._unit
        self.data['Values'] = pd.Series(v, index=self.data.index)

    @property
    def unit(self):
        """Unit of the vector values.
            Setter
            ------
                Set as str: vector.unit = 'meter'
            Getter
                returns a pint Quantity
        """
        
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
                for i in range(self._magnitude.shape[0]):
                    self.data.iloc[i, 1] = self.data.iloc[i, 1].to(self._unit)
                    x = self.data.iloc[i, 1]
                    y = copy.copy(x)
                    self._magnitude[i] = y.magnitude
                break
            except AttributeError:
                for i in range(len(self.magnitude)):
                    self.data.iloc[i, 1] = self.data.iloc[i, 1] * self._unit
                break
