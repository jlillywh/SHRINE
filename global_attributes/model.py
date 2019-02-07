from global_attributes.aegis import Aegis
from global_attributes.simulator import Simulator
from global_attributes.clock import Clock
from global_attributes.list_set import ListSet


class Model(Aegis):
    def __init__(self):
        Aegis.__init__(self)
        self.clock = Clock()
        self.simulator = Simulator()
        self.listSet = ListSet()