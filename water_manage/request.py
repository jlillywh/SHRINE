from global_attributes.aegis import Aegis
from inputs.constants import U


class Request(Aegis):
    """Class for creating request objects that have an amount and priority
    
        Attributes
        ----------
        name : str
        amount : Quantity
            This is the amount being requested, which is typically in terms of a flow rate
        priority : int
            The priority number where a lower number indicates higher priority
            The lowest possible priority is 1
    """
    def __init__(self, name="request1", amount=10 * U.m3 / U.day, priority=1):
        Aegis.__init__(self)
        self.name = name
        self.amount = amount
        self.priority = priority
