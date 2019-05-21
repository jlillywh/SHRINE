import networkx as nx
import matplotlib.pyplot as plt


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
        
    def add_source(self, node_name, capacity, downstream='Sink'):
        self.dg.add_edge('Source', node_name)
        self.dg.add_edge(node_name, downstream, capacity=capacity)
        
    def add_junction(self, node_name, downstream):
        self.dg.add_edge(node_name, downstream, capacity=9e9)
        
    def draw(self):
        network_copy = self.dg.copy()
        network_copy.remove_node(self.source)
        plt.subplot()
        nx.draw(network_copy, with_labels=True)
        plt.show()
        
    def outflow(self):
        flow_value, flow_dict = nx.maximum_flow(self.dg, self.source, self.sink, capacity='capacity')
        return flow_value
    
    def load_from_file(self, filename):
        self.dg = nx.read_gml(filename)
        #catchments = [x for x, y in self.dg.nodes(data=True) if y['capacity'] > 0]
        for n in self.dg.copy():
            # self.dg.nodes[c]['catchment'] = Catchment()
            if 'C' in n:
                self.dg.add_edge(self.source, n)
