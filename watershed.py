from aegis import Aegis
from catchment import Catchment
from junction import Junction
from error import NodeNotFound
from error import NodeAlreadyExists
import networkx as nx
import matplotlib.pyplot as plt

class Watershed(Aegis):
    """ For now, we are just going to build a simple watershed that assumes
        a basic network configuration because we are not ready to tackle
        flow networks. This water assumes the following setup:
                C1          C2
                 |           |
                 \           /
                  \         /
                   \       /
                    \     /
                     \   /
                      \ /
                      J1
                       |
          C3__         |
              \_______J2

        Where C1, C2, and C3 are inflows that contribute outflow discharge
        to the next downstream junction (J1 and J2). J2 is the outflow from
        the watershed.

        Attributes
        ----------
            junctions : Array
            outflow_node : Junction
                This is the final junction in the model that discharges from
                all other nodes of the watershed.
            network : networkx.DiGraph
                Represents the flow network of catchments and junctions using
                a bi-directional graph.

        Methods
        -------
            update(precipitation, et)
            outlfow()
            add_junction(junct_name)
            add_node(node, junction)
            set_outflow_node
                Assign the junction within the watershed that
                is the outflow node.
    """

    def __init__(self):
        Aegis.__init__(self)
        self.outflow_node = Junction('J1')
        self.junctions = [self.outflow_node]
        self.network = nx.DiGraph()
        self.network.add_node(self.outflow_node.name)

    def update(self, precip, et, junction):
        for i in junction.inflows:
            if type(i) is Catchment:
                i.update_runoff(precip, et)
            elif type(i) is Junction:
                self.update(precip, et, i)
    
    @property
    def outflow(self):
        return self.outflow_node.outflow
    
    def add_junction(self, junct_name):
        """Adds a new junction to the watershed.
        
            Parameters
            ----------
                junct_name : str
                    Name of the new junction
        """
        
        try:
            if self.junction_exists(junct_name):
                raise NodeAlreadyExists
            else:
                self.junctions.append(Junction(junct_name))
                self.network.add_node(junct_name)
        except NodeAlreadyExists:
            print("Node already exists! Cannot be added.")
    
    def add_inflow(self, inflow_node, junct_name):
        """Adds a catchment or junction to a junction in the watershed.
        
            Parameters
            ----------
                junct_name : str
                    The name of the junction that accepts inflow
                inflow_node : Catchment or Junction
                    The catchment or junction that discharges
                    into the junction
        """
        try:
            junction = self.get_junction(junct_name)
            if type(inflow_node) is Catchment:
                junction.add_inflow(inflow_node)
                self.network.add_node(inflow_node.name)
                self.network.add_edge(inflow_node.name, junct_name)
            elif type(inflow_node) is str:
                junction.add_inflow(self.get_junction(inflow_node))
                self.network.add_node(inflow_node)
                self.network.add_edge(inflow_node, junct_name)
        except NodeNotFound:
            print("Junction does not exist!")
        
        
    def set_outflow_node(self, junct_name):
        try:
            outflow_junction = self.get_junction(junct_name)
            if outflow_junction == None:
                raise NodeNotFound
            else:
                self.outflow_node = outflow_junction
        except NodeNotFound:
            print("Cannot set because this junction does not exist!")
    
    def get_junction(self, junct_name):
        """Find the junction that matches the name provided.
        Return the junction node
        
        """
        found = False
        try:
            for j in self.junctions:
                if j.name == junct_name:
                    found = True
                    return j
                else:
                    continue
            if not found:
                raise NodeNotFound
        except NodeNotFound:
            print("This junction is not found!")

    def junction_exists(self, junct_name):
        """Find if the junction matches the name provided.
            Parameters
            ----------
                junct_name : str
                    The name of the junction we are checking for existence
            Returns
            -------
                found : bool
                    True if the junction is found; False if not

        """
        found = False
        for j in self.junctions:
            if j.name == junct_name:
                found = True
            else:
                continue
        return found
    
    def draw(self):
        plt.subplot()
        nx.draw(self.network, with_labels=True, font_weight='bold')
        plt.show()