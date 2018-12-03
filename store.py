import errorChecks as ec
from aegis import Aegis

class Store(Aegis):
    """
        A class used to represent a storage element

        ...

        Attributes
        ----------
        about_str : str
            a formatted string to print out the store properties
        name : str
            the name of the store
        quantity : float
            the amount in the store
        capcity : float
            the upper bound on quantity
        overflow : float
            amount in excess of capacity after applying inflow and outflow
        outflow : float
            requested outflow until store is empty

        Methods
        -------
        update : float
            update quantity after applying inflows and outflows
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
            the upper bound on quantity
        overflow : float
            excess outflow when quantity exceeds capacity
        outflow : float
            The actual amount discharged from the store
        """
        self.name = "Store"

        Aegis.__init__(self)

        self.quantity = quantity
        self.capacity = capacity
        self.overflow = 0.0
        self.outflow = 0.0
        self.update(0.0, self.outflow)

    def update(self, inflow, request):
        """Updates the quantity given inflow and request being applied

        If quantity ends up out of bounds (upper or lower) then it is
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
        quantity = self.quantity + inflow - request

        if quantity > self.capacity:
            overflow = quantity - self.capacity
            quantity = self.capacity
            outflow = request
        elif quantity < 0.0:
            outflow = request + quantity
            quantity = 0.0
        else:
            outflow = request

        self.overflow = overflow
        self.outflow = outflow
        self.quantity = quantity