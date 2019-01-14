from aegis import Aegis
from catchment import Catchment
from junction import Junction
from error import NodeNotFound
from error import NodeAlreadyExists
import networkx as nx
import matplotlib.pyplot as plt

class Watershed(Aegis):
    """ This class is used to create a watershed consisting of
        catchments and junctions.
        
        Precipitation and ET are passed as input to the catchments globally
        from the watershed. Each catchment in the watershed processes the
        excess rainfall into estimated runoff, which is passed to the
        junction it is connected to. From there, junctions add up all
        inflows and pass their outflow to the next junction it is
        connected to. This is done recursively starting from the outflow node
        and working upstream from there.
        
        You can add catchments and junctions then connect them together using
        the built-in methods on the watershed object.

        Attributes
        ----------
            junctions : Array(Junction)
            outflow_node : Junction
                This is the final junction in the model that discharges from
                all other nodes of the watershed.
            outflow : float
                Total outflow from the outlet_node. This property is updated
                when the update() method is called.
            network : networkx.DiGraph
                Represents the flow network of catchments and junctions using
                a bi-directional graph.

        Methods
        -------
            update(precipitation, et, outlet_node)
                Calculates runoff from all catchments and routes it down
                through the flow network
            outflow (@property)
                This is the resulting discharge from the watershed.
            add_junction(junct_name)
            add_node(node, junction)
            set_outflow_node
                Assign the junction within the watershed that
                is the outflow node.
                
            draw()
                This method will show a DiGraph from the networkx library that
                represents the schematic of the watershed and how catchments
                and junctions are connected.
    """

    def __init__(self):
        Aegis.__init__(self)
        self.outflow_node = Junction('J1')
        self.outflow = 0.0
        self.junctions = [self.outflow_node]
        self.network = nx.DiGraph()
        self.network.add_node(self.outflow_node.name)

    def update(self, precip, et, junction):
        """Calculates runoff from all catchments and routes it down
                through the flow network until the junction specified.
                
                For a typical update, the junction would be the outlet
                of the watershed. The flow rate is stored as a list of
                inflows within each junction.
                
            Parameters
            ----------
                precip : float
                et : float
                junction : Junction
        """
        
        for i in junction.inflows:
            if type(i) is Catchment:
                i.update_runoff(precip, et)
            elif type(i) is Junction:
                self.update(precip, et, i)
        self.outflow = self.outflow_node.outflow
    
    def add_junction(self, junct_name):
        """Adds a new junction to the watershed.
            
            Build a new junction object by name. This junction can be
            added to the flow network later.
        
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
            print("Node " + junct_name + " already exists! Cannot be added.")
    
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
            print("Junction " + junct_name + " does not exist!")
        
        
    def set_outflow_node(self, junct_name):
        try:
            outflow_junction = self.get_junction(junct_name)
            if outflow_junction == None:
                raise NodeNotFound
            else:
                self.outflow_node = outflow_junction
        except NodeNotFound:
            print("Cannot set because this junction " + junct_name + " does not exist!")
    
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
            print("Junction " + junct_name + " is not found!")

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