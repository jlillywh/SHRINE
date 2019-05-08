from itertools import count
from pprint import pprint
from datetime import datetime
from global_attributes.constants import U
from validation import error_checks as ec


class Aegis:
    """Base class for all Aegis objects

        ...

        Attributes
        ----------
        name : str
            the name of the object
        description : str
            what does this object represent?
        display_unit : pint Quantity
            This is the base display_unit for any Aegis object
        base_unit : str
            The name of the base display_unit, which should be SI

        Methods
        -------
        about : str
            a formatted string to print out the store properties
        get_instance_count : int
            return the number of objects of this class created
        to_base_value()
            converts the object's value to its Aegis base_unit

        """

    _ids = count(1)

    def __init__(self, name=None, description=None, display_unit='m^3'):
        """
        Parameters
        ----------
        name : str, optional
            the name of the store
        description : str
            what does this object represent?
        display_unit : str
            The name of the display_unit for this object
        """
    
        self.id = next(self._ids)
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__
        if not description:
            self.description = "An object of " + str(self.name) + " type."
        else:
            self.description = description
        self.created_on = datetime.today()
        if type(display_unit) == str:
            self.display_unit = U.parse_expression(display_unit).units
        elif type(display_unit) == U.Unit:
            self.display_unit = (1.0 * display_unit).unit
        else:
            self.display_unit = U.Unit('m')
        self.base_unit = ((1 * self.display_unit).to_base_units()).units
        r = 4
        
    def to_base_value(self, value, type=1):
        if type == 1:
            unit = self.display_unit
        elif type == 2:
            unit = self.display_unit ** 2
        else:
            unit = self.display_unit
            assert ValueError('Display unit type not recognized')
        if isinstance(value,(float, int,)):
            ec.check_positive(value)
            value *= unit
            value = value.to_base_units()
            return value.magnitude
        elif isinstance(value,(list,)):
            ec.check_all_items_positive(value)
            new_list = []
            for i in range(len(value)):
                value[i] *= unit
                value[i] = value[i].to_base_units()
                new_list.append(value[i].magnitude)
            return new_list

    def value_at_unit(self, value):
        value *= self.base_unit
        value = value.to(self.display_unit)
        return value.magnitude
        
    def get_instance_count(self):
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
