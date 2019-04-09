from global_attributes.aegis import Aegis
from hydrology.catchment import Catchment
from hydrology.junction import Junction
import networkx as nx
import matplotlib.pyplot as plt
from inputs.constants import U


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
            source_node : Atmosphere
                node_type = 100
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
                
            get_catchment(catchment_name)
                Retrieves a catchment from the watershed after first determining
                if it exists. If so, it returns the catchment
                
            load_from_file(file_name)
                Loads a new watershed from a file, overwriting any existing nodes
    """

    def __init__(self):
        Aegis.__init__(self)
        self.network = nx.DiGraph()
        self.source_node = 'A'
        self.network.add_node(self.source_node, node_type=100)
        # self.network.add_node(self.source_node, node_type=100)
        self.sink_node = Junction('J1')
        self.outflow = 0.0 * U.m3/U.day
        self.network.add_node(self.sink_node.name, node_type=300)
        self.network.add_node('C1', node_type=200)
        self.network.add_edge(self.source_node, 'C1')
        self.network.add_edge('C1', 'J1', runoff=99.0 * U.m3/U.day)

    def update(self, precip, et):
        """Calculates runoff from all catchments and routes it down
                through the demand network until the junction specified.
                
                For a typical update, the junction would be the outlet
                of the watershed. The demand rate is stored as a list of
                inflows within each junction.
                
            Parameters
            ----------
                precip : float
                et : float
        """
        for node in self.network.nodes:
            if self.network.nodes[node]['node_type'] == 200:
                catchment = self.network.nodes[node]['catchment']
                catchment.update_runoff(precip, et)
                scr = list(self.network.successors(node))[0]
                self.network.edges[node, scr]['runoff'] = catchment.outflow

        # Use the max_flow algorithm to calculate the total flow from the watershed
        flow_value, flow_dict = nx.maximum_flow(self.network, self.source_node, self.sink_node.name, capacity='runoff')
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
        self.network.add_node(junct_name, type='Junction')
        self.network.add_edge(junct_name, receiving_junction)
            
    def link_catchment(self, catchment_name, receiving_junction):
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
        self.network.add_edge(catchment_name, receiving_junction, runoff=99.0 * U.m3 / U.day)
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
        try:
            return self.network.nodes[node_name]
        except KeyError:
            print("The node " + node_name + " does not exist!")

    def draw(self):
        network_copy = self.network.copy()
        network_copy.remove_node(self.source_node)
        plt.subplot()
        nx.draw(network_copy, with_labels=True)
        plt.show()
        
    def load_from_file(self, filename):
        self.network = nx.read_gml(filename)
        catchments = [x for x, y in self.network.nodes(data=True) if y['node_type'] == 200]
        self.network.add_node('A', node_type=100)
        self.source_node = 'A'
        self.sink_node = Junction('J3')

        for c in catchments:
            self.network.nodes[c]['catchment'] = Catchment()
            self.network.add_edge(self.source_node, c)
