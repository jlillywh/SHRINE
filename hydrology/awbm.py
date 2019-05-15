from validation import error_checks as ec
from water_manage.store import Store
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

    def __init__(self, depth_capacity=[0.04, 0.15, 0.3]):
        """Initialize the watershed with the depth capacities of the buckets.
            Parameters
            ----------
            depth_capacity : list of float
                The capacity (depth) of each bucket. Units are meters.
        """
        self.partial_area_fraction = [0.134, 0.433, 0.433]

        self.depth_comp_capacity = depth_capacity
        self.baseflow_index = 0.658
        self.surface_recession = 0.869
        self.surface = Store(0.0)
        self.baseflow_recession = 0.309
        self.base = Store(0.0)

        self.bucket_count = len(self.depth_comp_capacity)
        bucket_capacities = [0.0] * self.bucket_count
        for i in range(self.bucket_count):
            bucket_capacities[i] = self.partial_area_fraction[i] * self.depth_comp_capacity[i]

        self.buckets = StoreArray(self.bucket_count)
        self.buckets.set_quantities([0.0, 0.0, 0.0])
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
        ec.check_all_items_positive(inflow)
        ec.check_all_items_positive(outflow)

        sum_overflow = 0.0
        for i in range(self.bucket_count):
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
                Daily precipitation [m]
            et : float
                effective evapotranspiration [m]

            Returns
            -------
            outflow : float
                outflow from the catchment [m] on a per unit area basis

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
        self.surface.update(to_surface, (1.0 - self.surface_recession) * self.surface.quantity)

        # Baseflow outflow solved using recession outflow
        self.base.update(to_baseflow, (1.0 - self.baseflow_recession) * self.base.quantity)

        # Sum surface and baseflow
        return self.surface.outflow + self.base.outflow

    def set_partial_area_fraction(self, new_fractions):
        """Reset the partial area fractions used for the bucket stores

            These fractions are rarely changed. They must add up to 1.0"""
        ec.check_equal_length(self.partial_area_fraction, new_fractions)
        ec.check_values_add_to_1(new_fractions)

        # If these tests pass, reassign the array depths now
        self.partial_area_fraction = new_fractions
        bucket_capacities = [0.0] * self.bucket_count
        for i in range(self.bucket_count):
            bucket_capacities[i] = new_fractions[i] * self.depth_comp_capacity
        self.buckets.set_capacity(bucket_capacities)
        return "Array of fractions replaced."

    def set_comp_capacity(self, new_capacities):
        """Reset the capacities used for the buckets

            Parameters
            ----------
            new_capacities : list of floats
                Capacity for each bucket [mm]

            """
        ec.check_equal_values(self.bucket_count, len(new_capacities))

        # If this test passes, reassign the array depths now
        self.depth_comp_capacity = new_capacities
        bucket_capacities = [0.0] * self.bucket_count
        for i in range(self.bucket_count):
            bucket_capacities[i] = new_capacities[i] * self.partial_area_fraction[i]
        self.buckets.set_capacity(bucket_capacities)
        return "Array of fractions replaced."
