import errorChecks as ec
from store import Store

class Awbm:
    """ A class used to represent a rainfall runoff object

        The AWBM object represents a rainfall-runoff process that
        carries it's hydrologic state properties, which are useful
        for simulating rainfall runoff for one or more watersheds.
        It is formulated to operate on a per area basis where the
        result is in units of length per time (i.e. mm/day) so that
        the object can be used as part of a larger model to estimate
        volumetric runoff from a watershed. In essence, you multiply
        the resulting runoff rate from the awbm object by the area
        of the watershed.

        Attributes
        ----------
        name : str
            the name of the store
        baseflow_index : float
            the fraction of total bucket overflow that
        surface_recession : float
            Surface runoff recession constant
        baseflow_recession : float
            Baseflow recession constant (for selected K_step)
        depth_comp_capacity : array[float]
            Storage capacity for each bucket
            This array contains the depth capacity for each bucket.
            represents the capacity of the surface to absorb
            precipitation, remove losses, and overflow the
            amount that is in excess of the capacity.
            Typically these values range from 10 mm to 400 mm

        Methods
        -------
        _store_overflow : float
            updates the state of the buckets and calculates overflow
            from each bucket and sums the total
        runoff : float
            this is the main output of AWBM. It represents the
            runoff discharge rate from the watershed on a per
            area basis.
        set_bucket_capacity :
            reset the capacity values for each bucket (mm)
    """

    def __init__(self):
        self.partial_area_fraction = [0.134, 0.433, 0.433]
        self.depth_comp_capacity = [0.0374, 0.324, 0.147]
        self.baseflow_index = 0.658
        self.surface_recession = 0.869
        self.surface = Store(0.0)
        self.baseflow_recession = 0.309
        self.base = Store(0.0)

        self.bucket_count = 3
        self.buckets = []
        for i in range(self.bucket_count):
            self.buckets.append(Store(0.0, self.partial_area_fraction[i] * self.depth_comp_capacity[i]))

    def _store_overflow(self, inflow, outflow):
        ''' Private method used to calculate overflow from the buckets

            Calculate the overflow rate from each bucket individually
            This represents the excess rainfall after initial losses
            in the soil and due to ET from plant life.

            Parameters
            ----------
            inflow, outflow : float
                within the context of awbm, the inflow is precipitation and
                outflow is the effective evapotranspiration

            Returns
            ----------
            sum_overflow : float
                the sum of overflows from all the buckets
        '''
        sum_overflow = 0.0
        for i in range(len(self.buckets)):
            self.buckets[i].update(inflow, outflow)
            sum_overflow += self.buckets[i].overflow
        return sum_overflow

    def runoff(self, precip, et):
        """Calculates runoff rate given precip and effective ET

                Runoff is the process of routing overflows from the buckets
                by splitting the flow into a surface store and a baseflow
                store. The split is a function of a constant supplied by the
                user. The quantity accumulated in both of these stores is
                subsequently removed using a recession flow that is also a
                function of constants supplied by the user. Recession flow is
                added together and becomes the resulting runoff rate from
                the awbm object. The flow rate is in terms of depth.

                Parameters
                ----------
                precip : float
                    fill in...
                et : float
                    fill in...

                Returns
                ----------
                runoff_rate : float
                    volumetric runoff from the catchment

                Raises
                ------
                NotImplementedError
                    Raise if either value is negative
                """
        overflow = self._store_overflow(precip, et)

        # Split flows to surface runoff and baseflow
        to_baseflow = overflow * self.baseflow_index
        to_surface = overflow * (1.0 - self.baseflow_index)

        # Surface runoff solved using recession outflow
        self.surface.update(to_surface, (1.0 - self.surface_recession) * self.surface.quantity)

        # Baseflow runoff solved using recession outflow
        self.base.update(to_baseflow, (1.0 - self.baseflow_recession) * self.base.quantity)

        # Sum surface and baseflow
        return self.surface.outflow + self.base.outflow

    def set_partial_area_fraction(self, new_fractions):
        """ Reset the partial area fractions used for the bucket stores

            These fractions are rarely changed. They must add up to 1.0"""
        ec.checkEqualLength(self.partial_area_fraction, new_fractions)
        ec.checkValuesAddTo1(new_fractions)

        # If these tests pass, reassign the array values now
        self.partial_area_fraction = new_fractions
        return "Array of fractions successfully replaced."

    def set_bucket_capacity(self, new_capacities):
        """ Reset the capacities used for the buckets

            Parameters
            ----------
            new_capacities : array of floats

            """
        ec.checkEqualLength(self.buckets, new_capacities)

        # If this test passes, reassign the array values now
        self.depth_comp_capacity = new_capacities
        return "Array of fractions successfully replaced."

    def set_baseflow_index(self, new_index):
        ec.checkInRange(new_index, 0.0, 1.0)

        self.baseflow_index = new_index
        return "Baseflow Index successfully updated."

    def set_baseflow_recession(self, new_index):
        ec.checkInRange(new_index, 0.0, 1.0)

        self.baseflow_recession = new_index
        return "Baseflow Recession constant successfully updated."

    def set_surface_recession(self, new_index):
        ec.checkInRange(new_index, 0.0, 1.0)

        self.surface_recession = new_index
        return "Surface Recession constant successfully updated."