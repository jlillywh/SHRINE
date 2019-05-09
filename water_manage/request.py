

class Request:
    """Class for creating request objects that have an amount and priority
    
        Attributes
        ----------
        name : str
            Name of the request
        amount : float
            This is the amount being requested, which is typically in terms of a flow rate
        priority : int
            The priority number where a lower number indicates higher priority
            The lowest possible priority is 1
        TODO add a delivery attribute that is changed after allocation
    """
    def __init__(self, name, amount=10, priority=1):
        self.name = name
        self.amount = amount
        self.priority = priority
        self.delivery = amount
