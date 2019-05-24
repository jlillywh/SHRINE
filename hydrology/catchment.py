from hydrology.awbm import Awbm


class Catchment:
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

    def __init__(self, area=1000.0, runoff_method='simple'):
        """

        Attributes
        ----------
        area : float
            Area of the catchment in m2
        runoff_method : Awbm
        outflow : float
            Runoff outflow from the catchment in terms of m3/d
            
        Methods
        -------
        update_runoff(precip, et)
        
        """

        self.area = area
        if runoff_method == 'simple':
            self.runoff_method = Rational()
        else:
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


class Rational:
    """A class used to represent a simple mass balance of inflow and outflow"""
    def __init__(self):
        self.loss = 0.35
    
    def runoff(self, precip, et):
        precip_excess = precip - et
        return precip_excess * (1 - self.loss)