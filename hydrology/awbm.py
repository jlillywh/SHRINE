from validation import errorChecks as ec
from water_manage.store import Store
from inputs.constants import U
from water_manage.store_array import StoreArray


class Awbm:
    """A class used to represent a rainfall outflow object

        The AWBM object represents a rainfall-outflow process that
        carries it's hydrologic state properties, which are useful
        for simulating rainfall outflow for one or more watersheds.
        It is formulated to operate on a per area basis where the
        outputs is in units of length per time (i.e. mm/day) so that
        the object can be used as part of a larger model to estimate
        volumetric outflow from a catch01. In essence, you multiply
        the resulting outflow rate from the awbm object by the area
        of the catch01.

        Attributes
        ----------
        name : str
            the name of the store
        baseflow_index : float
            the fraction of total bucket overflow that
        surface_recession : float
            Surface outflow recession constant
        baseflow_recession : float
            Baseflow recession constant (for selected K_step)
        depth_comp_capacity : array[float]
            Storage capacity for each bucket [mm]
            This array contains the depth capacity for each bucket.
            represents the capacity of the surface to absorb
            precipitation, remove losses, and overflow the
            amount that is in excess of the capacity.
            Typically these depths range from 10 mm to 400 mm

        Methods
        -------
        _bucket_overflow : float
            updates the state of the buckets and calculates overflow
            from each bucket and sums the total [mm]
        outflow : float
            this is the main output of AWBM. It represents the
            outflow discharge rate from the catch01 on a per
            area basis [mm]
        set_bucket_capacity :
            reset the capacity depths for each bucket [mm]
    """

    def __init__(self):
        self.partial_area_fraction = [0.134, 0.433, 0.433]

        self.depth_comp_capacity = [37.44, 324.4, 146.6] * U.mm
        self.baseflow_index = 0.658
        self.surface_recession = 0.869
        self.surface = Store(0.0 * U.mm)
        self.baseflow_recession = 0.309
        self.base = Store(0.0 * U.mm)

        self.bucket_count = 3
        bucket_capacities = [0.0 * U.mm] * self.bucket_count
        for i in range(self.bucket_count):
            bucket_capacities[i] = self.partial_area_fraction[i] * self.depth_comp_capacity[i]

        self.buckets = StoreArray(self.bucket_count)
        self.buckets.set_quantities([0.0, 0.0, 0.0] * U.mm)
        self.buckets.set_capacity(bucket_capacities)

    def _bucket_overflow(self, inflow, outflow):
        """Private method used to calculate overflow from the buckets

            Calculate the overflow rate from each bucket individually
            This represents the excess rainfall after initial losses
            in the soil and due to ET from plant life.

            Parameters
            ----------
            inflow, outflow : Array[float]
                within the context of awbm, the inflow is precipitation and
                outflow is the effective evapotranspiration

            Returns
            ----------
            sum_overflow : float
                the sum of overflows from all the buckets
        """
        sum_overflow = 0.0 * U.mm/U.day
        for i in range(len(self.buckets)):
            self.buckets[i].update(inflow[i], outflow[i])
            sum_overflow += self.buckets[i].overflow
        return sum_overflow

    def runoff(self, precip, et):
        """Calculates outflow rate given precip and effective ET

            Runoff is the process of routing overflows from the buckets
            by splitting the demand into a surface store and a baseflow
            store. The split is a function of a constant supplied by the
            user. The _quantity accumulated in both of these stores is
            subsequently removed using a recession demand that is also a
            function of constants supplied by the user. Recession demand is
            added together and becomes the resulting outflow rate from
            the awbm object. The demand rate is in terms of depth.

            Parameters
            ----------
            precip : float
                Daily precipitation [mm]
            et : float
                effective evapotranspiration [mm]

            Returns
            -------
            outflow : float
                outflow from the catchment [mm] on a per unit area basis

            Raises
            ------
            NotImplementedError
                .....
            """
        # Distribute precip and et over each bucket
        precip_a = [a * precip for a in self.partial_area_fraction]
        et_a = [a * et for a in self.partial_area_fraction]
        self.buckets.update(precip_a, et_a)
        overflow = self.buckets.total_overflow()

        # Split flows to surface outflow and baseflow
        to_baseflow = overflow * self.baseflow_index
        to_surface = overflow * (1.0 - self.baseflow_index)

        # Surface outflow solved using recession outflow
        self.surface.update(to_surface, (1.0 - self.surface_recession) * self.surface.quantity / U.day)

        # Baseflow outflow solved using recession outflow
        self.base.update(to_baseflow, (1.0 - self.baseflow_recession) * self.base.quantity / U.day)

        # Sum surface and baseflow
        return self.surface.outflow + self.base.outflow

    def set_partial_area_fraction(self, new_fractions):
        """Reset the partial area fractions used for the bucket stores

            These fractions are rarely changed. They must add up to 1.0"""
        ec.checkEqualLength(self.partial_area_fraction, new_fractions)
        ec.checkValuesAddTo1(new_fractions)

        # If these tests pass, reassign the array depths now
        self.partial_area_fraction = new_fractions
        bucket_capacities = [0.0 * U.mm] * self.bucket_count
        for i in range(self.bucket_count):
            bucket_capacities[i] = new_fractions[i] * self.depth_comp_capacity
        self.buckets.set_capacity(bucket_capacities)
        return "Array of fractions replaced."

    def set_comp_capacity(self, new_capacities):
        """Reset the capacities used for the buckets

            Parameters
            ----------
            new_capacities : array of floats
                Capacity for each bucket [mm]

            """
        ec.checkEqualValues(self.bucket_count, len(new_capacities))

        # If this test passes, reassign the array depths now
        self.depth_comp_capacity = new_capacities
        bucket_capacities = [0.0 * U.mm] * self.bucket_count
        for i in range(self.bucket_count):
            bucket_capacities[i] = new_capacities[i] * self.partial_area_fraction[i]
        self.buckets.set_capacity(bucket_capacities)
        return "Array of fractions replaced."