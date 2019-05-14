from itertools import count
from pprint import pprint
from datetime import datetime


class Aegis:
    """Base class for all Aegis objects

        ...

        Attributes
        ----------
        name : str
            the name of the object
        description : str
            what does this object represent?

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

    def __init__(self, name=None, description=None):
        """
        Parameters
        ----------
        name : str, optional
            the name of the store
        description : str
            what does this object represent?
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
