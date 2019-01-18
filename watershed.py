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
            catchments : Array(Catchments)
            outflow_node : Junction
                This is the final junction in the model that discharges from
                all other nodes of the watershed.
            outflow : float
                Total outflow from the outlet_node. This property is updated
                when the update() method is called.
            network : networkx.DiGraph
                Represents the demand network of catchments and junctions using
                a bi-directional graph.

        Methods
        -------
            update(precipitation, et, outlet_node)
                Calculates runoff from all catchments and routes it down
                through the demand network
            outflow (@property)
                This is the resulting discharge from the watershed.
            add_junction(junct_name, receiving_junction)
            add_catchment(catchment_name, receiving_junction)
            move_node(from_node, to_node)
            delete_node(node_name)
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
        self.network = nx.DiGraph()
        self.outflow_node = Junction('J1')
        self.outflow = 0.0
        self.network.add_node(self.outflow_node.name, type=self.outflow_node.class_name, flow=self.outflow)
        self.junctions = [self.outflow_node]
        self.catchments = []
        self.add_catchment('C1', self.outflow_node.name)

    def update(self, precip, et, junction):
        """Calculates runoff from all catchments and routes it down
                through the demand network until the junction specified.
                
                For a typical update, the junction would be the outlet
                of the watershed. The demand rate is stored as a list of
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
    
    def add_junction(self, junct_name, receiving_junction):
        """Adds a new junction to the watershed.
            
            Build a new junction object by name. This junction can be
            added to the demand network later.
        
            Parameters
            ----------
            junct_name : str
                Name of the new junction
            receiving_junction : str
                Name of the receiving junction
        """
        
        try:
            outlet_node = self.get_node(receiving_junction, self.junctions)
            if self.node_exists(junct_name, self.junctions):
                raise NodeAlreadyExists
            elif not self.node_exists(receiving_junction, self.junctions):
                raise NodeNotFound
            else:
                j = Junction(junct_name)
                outlet_node.add_inflow(j)
                self.junctions.append(j)
                self.network.add_node(junct_name)
                self.network.add_edge(junct_name, receiving_junction)
        except NodeAlreadyExists:
            print("Node " + junct_name + " already exists! Cannot be added.")
        except NodeNotFound:
            print("Node " + junct_name + " not found.")
            
    def add_catchment(self, catchment_name, receiving_junction):
        """Adds a new catchment to the watershed.

            Build a new junction object by name. This junction can be
            added to the demand network later.

            Parameters
            ----------
            catchment_name : str
                Name of the new catchment
            receiving_junction : str
                Name of the receiving junction
        """
    
        try:
            outlet_node = self.get_node(receiving_junction, self.junctions)
            if self.node_exists(catchment_name, self.catchments):
                raise NodeAlreadyExists
            elif not self.node_exists(receiving_junction, self.junctions):
                raise NodeNotFound
            else:
                c = Catchment(catchment_name)
                outlet_node.add_inflow(c)
                self.catchments.append(c)
                self.network.add_node(catchment_name, type=c.class_name)
                self.network.add_edge(catchment_name, receiving_junction)

        except NodeAlreadyExists:
            print("Node " + catchment_name + " already exists! Cannot be added.")

    # TODO add ability to move a node if an existing node is added.
    def delete_node(self, node_name):
        # TODO add a method to determine what junction a catchment is connected to
        
        # Iterate over the list of nodes
        sub = nx.bfs_tree(self.network, source=node_name, reverse=True)
        for i in list(sub.nodes):
            self.junctions.remove(i)
            self.network.remove_node(i)
            
    def get_connected_node(self, node_name):
        self.network.neighbors(self.network)
    def move_node(self, from_node, to_node):
        """Move existing node to another existing node
        """
        
    
        
    def set_outflow_node(self, junct_name):
        """Sets the outflow node for the watershed.
        
            This node must be an existing junction object. If not, then an error
            will be raised.
            
            Parameters
            ----------
            junct_name : str
                The name of the junction that you want to assign to be
                the outflow node for the watershed.
                
        """
        
        try:
            outflow_junction = self.get_node(junct_name, self.junctions)
            if outflow_junction == None:
                raise NodeNotFound
            else:
                self.outflow_node = outflow_junction
        except NodeNotFound:
            print("Cannot set because this junction " + junct_name + " does not exist!")
    
    def get_node(self, node_name, node_list):
        """Find the junction that matches the name provided.
        Return the junction node
        
        Parameters
        ----------
        node_name : str
            The name of the node we are checking for existence
        node_list : list(Aegis objects)
        
        Returns
        -------
        node : Aegis object
            Return the node if found; None if not found

        """
        found_node = None
        try:
            found = self.node_exists(node_name, node_list)
            if len(node_list) > 0 and found:
                for node in node_list:
                    if node.name == node_name:
                        found = True
                        found_node = node
                        break
                    else:
                        continue
            if not found:
                raise NodeNotFound
            else:
                return found_node
        except NodeNotFound:
            print("Junction " + node_name + " is not found!")

    def node_exists(self, node_name, node_list):
        """Find if the node matches the name provided.
            Parameters
            ----------
                node_name : str
                    The name of the node we are checking for existence
                node_list : list(Aegis objects)
            Returns
            -------
                found : bool
                    True if the node is found; False if not

        """
        found = False
        if len(node_list) > 0:
            for node in node_list:
                if node.name == node_name:
                    found = True
                else:
                    continue
        return found
    
    def draw(self):
        plt.subplot()
        nx.draw(self.network, with_labels=True)
        plt.show()