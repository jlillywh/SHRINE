from global_attributes.aegis import Aegis
from hydrology.awbm import Awbm
from global_attributes.constants import U


class Catchment(Aegis):
    """
    A class used to create watershed catchment objects.

    The catchment represents a portion of a watershed that
    accepts rainfall (less et) to produce an outflow.

    Attributes
    ----------
    area : float
        The land surface area of the catchment

    runoff_method : Aegis
        This is an Aegis object that represents the
        particular method used to calculate runoff

    outflow : float
        Store the runoff rate calculated based on input

    Methods
    -------
    update_runoff(precip, et)
        calculates the runoff rate based for the catchment
        updates the outflow attribute
    """

    def __init__(self, name="catchment1", area=100.0 * U.km**2):
        """

        Attributes
        ----------
        name : str
            The name of the catchment must start with 'C' or 'c'
        area : float
            Area of the catchment in km2
        runoff_method : Aegis
        outflow : float
            Runoff outflow from the catchment in terms of m3/d
            
        Methods
        -------
        update_runoff(precip, et)
        
        """

        Aegis.__init__(self)
        self.name = name
        self.area = area
        self.runoff_method = Awbm()
        self.outflow = 0.0 * U.m3/U.day

    def update_runoff(self, precip, et):
        """calculates the runoff rate based for the catchment
        updates the outflow attribute

        Parameters
        ----------
            precip: float
                Precipitation
            et: float
                Evapotranspiration

        Returns
        -------
            NA
        """

        self.outflow = self.runoff_method.runoff(precip, et) * self.area
