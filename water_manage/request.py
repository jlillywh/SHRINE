from global_attributes.aegis import Aegis
from inputs.constants import U


class Request(Aegis):
    
    def __init__(self, name="request1", amount=10 * U.m3 / U.day, priority=1):
        Aegis.__init__(self)
        self.name = name
        self.amount = amount
        self.priority = priority
