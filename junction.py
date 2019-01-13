from aegis import Aegis

class Junction(Aegis):
    def __init__(self, name="J1"):
        Aegis.__init__(self)

        self.inflows = []
        self.name = name

    def add_inflow(self, node):
        """ Add an Aegis node to the junction"""
        self.inflows.append(node)

    @property
    def outflow(self):
        sum = 0.0
        for i in range(len(self.inflows)):
            sum += self.inflows[i].outflow
        return sum