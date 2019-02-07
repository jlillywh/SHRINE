from global_attributes.aegis import Aegis
from hydrology.catchment import  Catchment

class Junction(Aegis):
    def __init__(self, name="J1"):
        """A junction combines 1 or more inflows to output the sum
        
            This is often used for adding up multiple inflows.
            
            Attributes
            ----------
            name : str
                The name must start with the character 'J' or 'j'
                
            inflows : list
                list of inflow objects, which can be 1 or more Catchment
                or other Junction objects.
                
            Methods
            -------
            add_inflow(node)
                Appends an inflow node to the list of inflows for this
                Junction
            delete_inflow(node)
                Remove item from list of inflows recursively
                
            outflow()
                Calculates the total outflow from the Junction, which
                is the sum of all inflows.
                
        """
        Aegis.__init__(self)

        self.inflows = []
        self.name = name

    def add_inflow(self, node):
        """ Add an Aegis node to the junction"""
        self.inflows.append(node)
        
    def delete_inflow(self, node):
        """Remove an existing inflow from the junction"""
        if type(node) is Catchment:
            self.inflows.remove(node)
        elif type(node) is Junction:
            self.delete_inflow(node)

    @property
    def outflow(self):
        sum = 0.0
        for i in range(len(self.inflows)):
            sum += self.inflows[i].outflow
        return sum