from itertools import count
from pprint import pprint
from datetime import datetime

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

        Methods
        -------
        getInstanceCount : int
            return the number of objects of this class created
        """

    _ids = count(1)

    def __init__(self):
        """
        Parameters
        ----------
        name : str, optional
            the name of the store
        description : str
            what does this object represent?
        """

        self.name = self.__class__.__name__
        self.id = next(self._ids)
        self.description = "An object of " + str(self.name) + " type."
        self.created_on = datetime.today()

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
