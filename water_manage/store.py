from validation import errorChecks as ec
from global_attributes.aegis import Aegis


class Store(Aegis):
    """A class used to represent a storage element

        ...

        Attributes
        ----------
        _quantity : float
            The amount in the store (base units)
        _capacity : float
            The upper bound on _quantity in base units
        _overflow : float
            Amount in excess of _capacity after applying inflow and outflow
            in base units
        _outflow : pint Quantity of a rate of quantity change
            requested outflow until store is empty

        Methods
        -------
        update(inflow, request)
            update _quantity after applying inflows and outflows
        set_quantity(amount)
            updates _quantity while ensuring bounds respected
    """

    def __init__(self, quantity=100.0, display_unit='gallon'):
        """
        Parameters
        ----------
        quantity : pint Quantity
            the amount in the store
        display_unit : str
            Name of the unit used for display purposes
        
        """
        Aegis.__init__(self, display_unit=display_unit)
        self._quantity = self.to_base_value(quantity)
        self._capacity = float("inf")
        self.inflow = 0.0
        self._overflow = 0.0
        self.request = 0.0
        self._outflow = 0.0
        
    @property  # when you do Store.quantity, it will call this function
    def quantity(self):
        return self.value_at_unit(self._quantity)

    @property
    def capacity(self):
        return self.value_at_unit(self._capacity)

    @property
    def overflow(self):
        return self.value_at_unit(self._overflow)

    @property
    def outflow(self):
        return self.value_at_unit(self._outflow)

    @quantity.setter  # when you do Store.quantity = x, it will call this function
    def quantity(self, amount):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            amount : float
                User defined amount to replace the existing _quantity
        """
        
        ec.check_positive(amount, "quantity")
        self._quantity = self.to_base_value(amount)
        self.update(0, 0)

    @capacity.setter  # when you do Store.capacity = x, it will call this function
    def capacity(self, new_capacity):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            new_capacity : float
                User defined amount to replace the existing _capacity
        """

        ec.check_positive(new_capacity, "capacity")
        new_capacity = self.to_base_value(new_capacity)
        
        if new_capacity < self._quantity:
            self._overflow = self._quantity - new_capacity
            self._capacity = new_capacity
            self._quantity = new_capacity
        else:
            self._overflow = 0.0
            self._capacity = new_capacity
        
    def update(self, inflow, request):
        """Updates the _quantity given inflow and request being applied

        If _quantity ends up out of bounds (upper or lower) then it is
        set to the bound and overflow or outflow is updated

        Parameters
        ----------
        inflow : float
            Inflowing material to the store assumed in terms of display units
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
        
        self.inflow = self.to_base_value(inflow)
        self.request = self.to_base_value(request)

        self._quantity += (self.inflow - self.request)

        if self._quantity > self._capacity:
            self._overflow = self._quantity - self._capacity
            self._quantity = self._capacity
        else:
            self._overflow = 0.0
        
        if self._quantity < 0.0:
            self._outflow = self.request + self._quantity
            self._quantity = 0.0
        else:
            self._outflow = self.request
