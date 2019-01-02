from aegis import Aegis
from awbm import Awbm

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

    def __init__(self, name="catchment1", area = 100.0):
        """

        Parameters
        ----------
            area : float
            runoff_method : Aegis
            outflow : float
        """

        Aegis.__init__(self)
        self.area = area
        self.runoff_method = Awbm()
        self.outflow = 0.0

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
