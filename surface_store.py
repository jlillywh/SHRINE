from store import Store

class SurfaceStore:

    def __init__(self, count=3):
        self.count = count
        self.partial_area_fraction = [0.134, 0.433, 0.433]
        self.depth_comp_capacity = [0.0374, 0.324, 0.147]

        self.buckets = []

        for i in range(self.count):
            self.buckets.append(Store("S", 0.0, self.partial_area_fraction[i] * self.depth_comp_capacity[i]))

    def overflow(self, inflow, outflow):
        sum_overflow = 0.0
        for i in range(len(self.buckets)):
            self.buckets[i].update(inflow, outflow)
            sum_overflow += self.buckets[i].overflow
        return sum_overflow