from store import Store

class AWBM:

    def __init__(self, catchment_area=100.0):
        self.area = catchment_area
        self.partial_area_fraction = [0.134, 0.433, 0.433]
        self.depth_comp_capacity = [0.0374, 0.324, 0.147]
        self.baseflow_index = 0.658
        self.surface_recession = 0.869
        self.baseflow_recession = 0.309
        self.surface = Store(0.0)
        self.base = Store(0.0)

        self.bucket_count = 3
        self.buckets = []
        for i in range(self.bucket_count):
            self.buckets.append(Store(0.0, self.partial_area_fraction[i] * self.depth_comp_capacity[i]))

    def _store_overflow(self, inflow, outflow):
        sum_overflow = 0.0
        for i in range(len(self.buckets)):
            self.buckets[i].update(inflow, outflow)
            sum_overflow += self.buckets[i].overflow
        return sum_overflow

    def runoff(self, precip, et):
        """Calculates runoff rate given precip and effective ET

                to be completed...

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
        runoff_rate = self.surface.outflow + self.base.outflow

        # Volumetric runoff
        return runoff_rate * self.area