from store import Store

class StoreArray:
    """Create an array of store objects"""

    def __init__(self, count=3):
        """The default is 3 stores only because this was initially
        used in the AWBM implementation.
        """
        self.stores = []
        self.count = count

        i = 0
        while i < self.count:
            self.stores.append(Store())
            i += 1

    def __getitem__(self, index):
        """Access to individual stores within the array"""
        return self.stores[index]

    def set_capacity(self, capacity_array):
        """Set the capacity of all items"""
        i = 0
        while i < self.count:
            self.stores[i].capacity = capacity_array[i]
            i += 1

    def set_quantities(self, quantity_array):
        """Set the quantities all at once using an array input.

            Parameters
            ----------
            quantity_array : Array[float]
        """
        for i in range(self.count):
            self.stores[i].quantity = quantity_array[i]

    def update(self, inflow, outflow):
        """Update the state of the store array by accumulating inflow
        and applying requested outflow.

        Parameters
        ----------
        inflow, outflow : array
        """
        i = 0
        while i < self.count:
            self.stores[i].update(inflow[i], outflow[i])
            i += 1

    def total_quantity(self):
        """Return the total _quantity by adding all store quantities"""
        sum_quantity = 0.0
        for i in range(self.count):
            sum_quantity += self.stores[i].quantity
        return sum_quantity

    def total_overflow(self):
        """Sum of overflows for all stores"""
        sum_overflow = 0.0
        i = 0
        while i < self.count:
            sum_overflow += self.stores[i].overflow
            i += 1
        return sum_overflow

    def total_outflow(self):
        """Sum of all outflows from the stores"""
        sum_outflow = 0.0
        i = 0
        while i < self.count:
            sum_outflow += self.stores[i].outflow
            i += 1
        return sum_outflow

    def transfer(self, from_index, to_index, amount):
        """Used to transfer material from one store in the array to another

            Parameters
            ----------
            from_index : int
                The index of the array of the store that you want to move
                material from
            to_index : int
                The index that you want material moved to."""
        i = 0
        while i < self.count:
            if i == from_index:
                from_store = self.stores[from_index]
                from_store.update(0.0, amount)
                self.stores[to_index].update(from_store.outflow, 0.0)
                break
            else:
                i += 1
