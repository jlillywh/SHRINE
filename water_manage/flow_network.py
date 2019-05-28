import networkx as nx
import matplotlib.pyplot as plt
from hydrology.catchment import Catchment


class Network:
    """Class for creating flow networks to route flows through a system of source, routes, stores, and sinks
    
        Attributes
        ----------
        source
        sink
        dg : DiGraph
        
        Methods
        -------
        add_source()
        add_junction()
        draw() : Draw the network
        outflow() : calculates the total discharge from the network to the sink node
        load_from_file()
    
    """
    def __init__(self):
        self.dg = nx.DiGraph()
        self.dg.add_node('Source')
        self.dg.add_node('Sink')
        self.source = 'Source'
        self.sink = 'Sink'
        
    def add_catchment(self, node_name, downstream_name='Sink'):
        self.dg.add_node(node_name, node_type='Catchment')
        self.dg.add_edge(self.source, node_name)
        self.dg.add_edge(node_name, downstream_name, capacity=0.0)
    
    def add_junction(self, name, downstream_name):
        self.dg.add_node(name, node_type='Junction')
        self.dg.add_edge(name, downstream_name)
           
    def draw(self):
        network_copy = self.dg.copy()
        network_copy.remove_node(self.source)
        plt.subplot()
        nx.draw(network_copy, with_labels=True)
        plt.show()
        
    def update_capacity(self, node_name, capacity):
        succ = list(self.dg.successors(node_name))[0]
        self.dg[node_name][succ]['capacity'] = capacity
        
    def update_all(self, capacity_dict):
        nx.set_edge_attributes(self.dg, capacity_dict)
    
    def outflow(self):
        """This function will first walk over all nodes in the graph and call their respective
            update() function.
            
            Parameters
            ----------
            self  (this DiGraph)
            TODO: Make sure all classes used to create node objects have a function called outflow() that updates
                the state of the object and returns the outflow
            
            Returns
            -------
            Flow (calculated using the Maximum_Flow algorithm of Networkx)
        """
        
        #nx.set_edge_attributes(self.dg, flow_dict, 'capacity')
        # for u, v, a in self.dg.edges(data=True):
        #     try:
        #         if a['capacity'] < float('inf'):
        #             a['capacity'] = flow
        #     except KeyError:
        #         pass

        flow_value, flow_dict = nx.maximum_flow(self.dg, self.source, self.sink, capacity='capacity')
        return flow_value
    
    def load_from_file(self, filename):
        self.dg = nx.read_gml(filename)
        # Convert catchment labels to Catchment objects
        for node in self.dg.copy().nodes():
            try:
                if self.dg.nodes[node]['node_type'] == 'Catchment':
                    self.dg.add_edge(self.source, node)
            except KeyError:
                pass

        # nx.set_node_attributes(self.dg, labels, 'labels')

