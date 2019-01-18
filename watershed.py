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
            sink_node : Junction
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
        self.source_node = 'A'
        self.network.add_node(self.source_node, type='Atmosphere')
        self.sink_node = Junction('J1')
        self.outflow = 0.0
        self.network.add_node(self.sink_node.name, type='Junction')
        self.network.add_node('C1', type=Catchment('C1'))
        self.network.add_edge(self.source_node, 'C1')
        self.network.add_edge('C1', 'J1', runoff=99.0)

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

        # Calculate runoff then assign to edge one at a time
        runoff_c1 = self.network.nodes['C1']['type'].outflow
        self.network.edges['C1', 'J1']['runoff'] = runoff_c1

        # or do it all at once using an attribute hash
        runoff_hash = {('C1', 'J1'): runoff_c1, ('A', 'C1'): 2.6}
        nx.set_edge_attributes(self.network, runoff_hash, 'runoff')

        # Use the max_flow algorithm to calculate the total flow from the watershed
        flow_value, flow_dict = nx.maximum_flow(self.network, self.source_node, self.sink_node, capacity='runoff')
        self.outflow = flow_value
    
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
        self.network.add_edge(junct_name, receiving_junction)
            
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

        self.network.add_node(catchment_name, type=Catchment(catchment_name))
        self.network.add_edge(catchment_name, receiving_junction, runoff=99.0)
        self.network.add_node(self.source_node, type=self.source_node)
        self.network.add_edge(self.source_node, catchment_name)

    def delete_node(self, node_name):
        sub = nx.bfs_tree(self.network, source=node_name, reverse=True)
        for i in list(sub.nodes):
            self.network.remove_node(i)

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
        self.sink_node = junct_name

    def get_node(self, node_name):
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
        return self.network.nodes[node_name]

    def draw(self):
        plt.subplot()
        nx.draw(self.network, with_labels=True)
        plt.show()