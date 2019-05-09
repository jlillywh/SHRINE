from validation import error_checks as ec


class Store:
    """A class used to represent a storage element

        All attributes are in terms of SI units

        Attributes
        ----------
        _quantity : float
            The amount in the store
        _capacity : float
            The upper bound on quantity
        overflow : float
            Amount in excess of capacity after applying inflow and outflow
        outflow : float
            requested outflow until store is empty

        Methods
        -------
        update(inflow, request)
            update _quantity after applying inflows and outflows
        set_quantity(amount)
            updates _quantity while ensuring bounds respected
    """

    def __init__(self, quantity=100.0):
        """
        Parameters
        ----------
        quantity : float
            the amount in the store
        
        """
        self._quantity = quantity
        self._capacity = float("inf")
        self.inflow = 0.0
        self.overflow = 0.0
        self.request = 0.0
        self.outflow = 0.0
        
    @property  # when you do Store.quantity, it will call this function
    def quantity(self):
        return self._quantity

    @quantity.setter  # when you do Store.quantity = x, it will call this function
    def quantity(self, amount):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            amount : float
                User defined amount to replace the existing _quantity
        """
        
        ec.check_positive(amount, "quantity")
        self._quantity = amount
        self.update(0, 0)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter  # when you do Store.capacity = x, it will call this function
    def capacity(self, new_capacity):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            new_capacity : float
                User defined amount to replace the existing _capacity
        """
    
        ec.check_positive(new_capacity, "capacity")
        new_capacity = new_capacity
    
        if new_capacity < self._quantity:
            self.overflow = self._quantity - new_capacity
            self._capacity = new_capacity
            self._quantity = new_capacity
        else:
            self.overflow = 0.0
            self._capacity = new_capacity

    def update(self, inflow, request):
        """Updates the _quantity given inflow and request being applied

        If _quantity ends up out of bounds (upper or lower) then it is
        set to the bound and overflow or outflow is updated

        Parameters
        ----------
        inflow : float
            Inflowing material to the store assumed
        request : float
            Request to discharge from the store (if available)
            if available, then the request becomes outflow

        Raises
        ------
        NotImplementedError
            Raise if either value is negative
        """

        ec.check_positive(inflow, "inflow")
        ec.check_positive(request, "request")
        
        self.inflow = inflow
        self.request = request

        self._quantity += (self.inflow - self.request)

        if self._quantity > self._capacity:
            self.overflow = self._quantity - self._capacity
            self._quantity = self._capacity
        else:
            self.overflow = 0.0
        
        if self._quantity < 0.0:
            self.outflow = self.request + self._quantity
            self._quantity = 0.0
        else:
            self.outflow = self.request
