from validation import errorChecks as ec
from global_attributes.aegis import Aegis
from inputs.constants import U
from validation.error import WrongUnits


class Store(Aegis):
    """A class used to represent a storage element

        ...

        Attributes
        ----------
        about_str : str
            a formatted string to print out the store properties
        name : str
            the name of the store
        quantity : pint Quantity (volume, mass, or length)
            the amount in the store. Prefixed with underscore because
            you should never redefine this value without using the
            "set_quantity" method to ensure bounds are not exceeded.
        capcity : pint Quantity
            the upper bound on _quantity. This must be compatible with
            the quantity unit
        overflow : pint Quantity of a rate of quantity change
            amount in excess of _capacity after applying inflow and outflow
        outflow : pint Quantity of a rate of quantity change
            requested outflow until store is empty

        Methods
        -------
        update(inflow, request)
            update _quantity after applying inflows and outflows
        set_quantity(amount)
            updates _quantity while ensuring bounds respected
    """

    def __init__(self, quantity=0.0 * U.m**3):
        """
        Parameters
        ----------
        quantity : pint Quantity
            the amount in the store
        _capacity : pint Quantity
            the upper bound on _quantity
        overflow : pint Quantity rate
            excess outflow when _quantity exceeds _capacity
        outflow : pint Quantity rate
            The actual amount discharged from the store
        """
        Aegis.__init__(self)
        self._quantity = quantity
        self.quantity_dim = quantity.dimensionality
        self._quantity_units = quantity.units
        self._rate_units = self._quantity_units / U.day
        self._capacity = float("inf") * self._quantity_units
        self.inflow = 0.0 * self._quantity_units
        self.overflow = max(quantity - self._capacity, 0.0 * self._quantity_units) / U.day
        self.request = 0.0 * self._quantity_units
        self.outflow = 0.0 * self._rate_units

    @property  # when you do Store.quantity_units, it will call this function
    def quantity_units(self):
        return self._quantity_units

    @quantity_units.setter  # when you do Store.quantity = x, it will call this function
    def quantity_units(self, new_unit):
        """Set the new quantity unit for the Store.
        
            Parameters
            ----------
            new_unit : str
                string representation of the unit.
        """
        
        try:
            new_unit = U.parse_expression(new_unit)
            if new_unit.check(self.quantity_dim):
                self._quantity_units = new_unit
                self._rate_units = self._quantity_units / U.day
                self._quantity = self._quantity.to(new_unit)
                self._capacity = self._capacity.to(new_unit)
                self.overflow = self.overflow.to(self._rate_units)
                self.outflow = self.outflow.to(self._rate_units)
            else:
                m = "Wrong dimension. Should be in terms of " + str(self.quantity_dim) + '.'
                raise WrongUnits(m)
        except AttributeError or U.errors.UndefinedUnitError:
            m = "Undefined unit dimension! Should be in terms of " + str(self.quantity_dim) + '.'
            raise WrongUnits(m)
        
    
    @property  # when you do Store.quantity, it will call this function
    def quantity(self):
        return self._quantity

    @quantity.setter  # when you do Store.quantity = x, it will call this function
    def quantity(self, amount):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            amount : Quantity
                user defined amount to replace the existing _quantity

            Returns
            -------
            self._quantity : Quantity
                The new _quantity of the store
        """
        
        try:
            if amount.check(self.quantity_dim):
                self._quantity = amount.to(self._quantity_units)
            else:
                m = "Wrong dimension. Should be in terms of " + str(self.quantity_dim) + '.'
                raise WrongUnits(m)
        except AttributeError:
            self._quantity = amount * self._quantity_units
        
        ec.checkPositive(amount, "quantity")
        
        
        self.update(0 * self._rate_units, 0 * self._rate_units)

        return self._quantity

    @property  # when you do Store.capacity, it will call this function
    def capacity(self):
        return self._capacity

    @capacity.setter  # when you do Store.capacity = x, it will call this function
    def capacity(self, new_capacity):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            new_capacity : Quantity
                user defined amount to replace the existing _capacity

            Returns
            -------
            self._capacity : Quantity
                The new _capacity of the store
        """
        
        try:
            if new_capacity.check(self.quantity_dim):
                new_capacity = new_capacity.to(self._quantity_units)
            else:
                m = "Wrong dimension. Should be in terms of " + str(self.quantity_dim) + '.'
                raise WrongUnits(m)
        except AttributeError:
            new_capacity = new_capacity * self._quantity_units

        ec.checkPositive(new_capacity, "capacity")
        
        if new_capacity < self._quantity:
            self.overflow = (self._quantity - new_capacity) / U.day
            self._capacity = new_capacity
            self._quantity = new_capacity
        else:
            self.overflow = 0.0 * self._quantity_units
            self._capacity = new_capacity
        return self._capacity

    def update(self, inflow, request):
        """Updates the _quantity given inflow and request being applied

        If _quantity ends up out of bounds (upper or lower) then it is
        set to the bound and overflow or outflow is updated

        Parameters
        ----------
        inflow : Quantity (rate)
            Inflowing material to the store
        request : Quantity (rate)
            Request to discharge from the store (if available)
            if available, then the request becomes outflow

        Raises
        ------
        NotImplementedError
            Raise if either value is negative
        """

        ec.checkPositive(inflow, "inflow")
        ec.checkPositive(request, "request")
        
        self.inflow = inflow
        self.request = request

        self._quantity += (self.inflow - self.request) * U.day

        self.calc_overflow()
        self.calc_outflow()
        
    def calc_overflow(self):
        if self._quantity > self._capacity:
            self.overflow = (self._quantity - self._capacity) / U.day
            self._quantity = self._capacity
        else:
            self.overflow = 0.0 * self._quantity_units / U.day
            
    def calc_outflow(self):
        if self._quantity < 0.0 * self._quantity_units:
            self.outflow = self.request + self._quantity / U.day
        else:
            self.outflow = self.request
