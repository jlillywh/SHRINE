from itertools import count
from pprint import pprint
from datetime import datetime
import pint


class Aegis:
    """Base class for all Aegis objects

        ...

        Attributes
        ----------
        about : str
            a formatted string to print out the store properties
        name : str
            the name of the object
        description : str
            what does this object represent?
        unit : pint Quantity
            This is the base unit for any Aegis object

        Methods
        -------
        getInstanceCount : int
            return the number of objects of this class created
        to_base_unit()
            converts the object's unit to its Aegis base_unit
        """

    _ids = count(1)

    def __init__(self, name=None, description=None, unit='m^3'):
        """
        Parameters
        ----------
        name : str, optional
            the name of the store
        description : str
            what does this object represent?
        unit : str
            The name of the unit for this object
        base_unit : str
            The name of the base unit, which should be SI
        """
        
        if name == None:
            self.name = self.__class__.__name__
        else:
            self.name = name
        #self.class_name = self.name
        self.id = next(self._ids)
        if description == None:
            self.description = "An object of " + str(self.name) + " type."
        self.created_on = datetime.today()

        self.U = pint.UnitRegistry(auto_reduce_dimensions=True)
        self.unit = self.U.parse_expression(unit).units
        self.base_unit = ((1 * self.unit).to_base_units()).units
        
    def to_base_value(self, value, type=1):
        if type == 1:
            unit = self.unit
        elif type == 2:
            unit = self.unit **2
        if isinstance(value,(float,)):
            value *= unit
            value = value.to_base_units()
            return value.magnitude
        elif isinstance(value,(list,)):
            new_list = []
            for i in range(len(value)):
                value[i] *= unit
                value[i] = value[i].to_base_units()
                new_list.append(value[i].magnitude)
            return new_list

    def getInstanceCount(self):
        """Get the bucket_count of objects created by this class
        :return:
        """
        return self._ids

    def about(self):
        """Print a copy of the class documentation"""
        return self.__class__.__doc__

    def attributes(self):
        """Print a summary of all object attributes"""
        pprint(vars(self))
