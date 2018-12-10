import errorChecks as ec
from aegis import Aegis

class Store(Aegis):
    """A class used to represent a storage element

        ...

        Attributes
        ----------
        about_str : str
            a formatted string to print out the store properties
        name : str
            the name of the store
        quantity : float
            the amount in the store. Prefixed with underscore because
            you should never redefine this value without using the
            "set_quantity" method to ensure bounds are not exceeded.
        capcity : float
            the upper bound on _quantity
        overflow : float
            amount in excess of capacity after applying inflow and outflow
        outflow : float
            requested outflow until store is empty

        Methods
        -------
        update(inflow, request)
            update _quantity after applying inflows and outflows
        set_quantity(amount)
            updates _quantity while ensuring bounds respected
    """

    def __init__(self, quantity=100.0, capacity=float("inf")):
        """
        Parameters
        ----------
        name : str, optional
            the name of the object (inherited)
        description : str, optional
            describe what the store represents
        quantity : float, optional
            the amount in the store
        capacity : float, optional
            the upper bound on _quantity
        overflow : float
            excess outflow when _quantity exceeds capacity
        outflow : float
            The actual amount discharged from the store
        """
        Aegis.__init__(self)
        self.description = "An object that stores mass"
        self.__quantity = quantity
        self.capacity = capacity
        self.overflow = 0.0
        self.outflow = 0.0
        self.update(0.0, self.outflow)

    @property  # when you do Store.quantity, it will call this function
    def quantity(self):
        return self.__quantity

    @quantity.setter  # when you do Store.quantity = x, it will call this function
    def quantity(self, amount):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            amount : float
                user defined amount to replace the existing _quantity

            Returns
            -------
            self._quantity : float
                The new _quantity of the store
        """
        if amount > self.capacity:
            self.__quantity = self.capacity
        elif amount < 0.0:
            self.__quantity = 0.0
        else:
            self.__quantity = amount
        return self.__quantity

    def update(self, inflow, request):
        """Updates the _quantity given inflow and request being applied

        If _quantity ends up out of bounds (upper or lower) then it is
        set to the bound and overflow or outflow is updated

        Parameters
        ----------
        inflow : float
            Inflowing material to the store
        request : float
            Request to discharge from the store (if available)
            if available, then the request becomes outflow

        Raises
        ------
        NotImplementedError
            Raise if either value is negative
        """

        ec.checkPositive(inflow, "inflow")
        ec.checkPositive(request, "request")

        overflow = 0.0
        outflow = 0.0
        temp_quantity = self.quantity + inflow - request

        if temp_quantity > self.capacity:
            overflow = temp_quantity - self.capacity
            outflow = request
        elif temp_quantity < 0.0:
            outflow = request + temp_quantity
        else:
            outflow = request

        self.overflow = overflow
        self.outflow = outflow
        self.quantity = temp_quantity
