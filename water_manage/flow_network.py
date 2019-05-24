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
        
    def add_source(self, node_name, downstream_name='Sink'):
        self.dg.add_edge('Source', node_name)
        self.dg.add_edge(node_name, downstream_name, capacity=0.0)
        self.dg.nodes[node_name]['node_type'] = Catchment()
        # self.dg.nodes[node_name]['capacity'] = 0.0
        
    def add_junction(self, node_name, downstream):
        self.dg.add_edge(node_name, downstream)
        self.dg.nodes[node_name]['node_type'] = 'Junction'
        
    def draw(self):
        network_copy = self.dg.copy()
        network_copy.remove_node(self.source)
        plt.subplot()
        nx.draw(network_copy, with_labels=True)
        plt.show()
        
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

        for u, v, a in self.dg.edges(data=True):
            try:
                if a['capacity'] < 9e9:
                    catchment = self.dg.nodes[u]['node_type']
                    catchment.update_runoff(10.0, 0.25)
                    a['capacity'] = catchment.outflow
            except KeyError:
                pass

        flow_value, flow_dict = nx.maximum_flow(self.dg, self.source, self.sink, capacity='capacity')
        return flow_value
    
    def load_from_file(self, filename):
        self.dg = nx.read_gml(filename)
        # catchments = [x for x, y in self.dg.nodes(data=True) if y['capacity'] > 0]
        for n in self.dg.copy():
            # self.dg.nodes[c]['catchment'] = Catchment()
            if 'C' in n:
                self.dg.add_edge(self.source, n)
