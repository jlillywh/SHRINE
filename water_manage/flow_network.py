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
        self.dg.add_node('source')
        self.dg.add_node('sink')
        self.source = 'source'
        self.sink = 'sink'
        self.calc_method = 'max'
        
    def add_catchment(self, node_name, downstream_name='sink'):
        self.dg.add_node(node_name, node_type='Catchment')
        self.dg.add_edge(self.source, node_name)
        self.dg.add_edge(node_name, downstream_name, capacity=0.0)
    
    def add_junction(self, name, downstream_name='sink'):
        self.dg.add_node(name, node_type='Junction')
        self.dg.add_edge(name, downstream_name)
        
    def add_supply(self, name, downstream_name, capacity=0.0):
        self.dg.add_edge(name, downstream_name, capacity=capacity)
        
    def add_splitter(self, name, downstream_nodes, source='source'):
        """ Adds a node that distributes what it receives to multiple downstream nodes
        
            Parameters
            ----------
            downstream_nodes : list of str
                This list includes the names of all downstream nodes to connect to."""
        self.dg.add_edge(source, name)
        for i in range(len(downstream_nodes)):
            self.dg.add_edge(name, downstream_nodes[i])
        
    def add_demand(self, name, source='source', sink='sink', demand=None, cost=None):
        self.dg.add_edge(source, name, capacity=demand, weight=cost)
        self.dg.add_edge(name, sink)
        
           
    def draw(self):
        network_copy = self.dg.copy()
        network_copy.remove_node(self.source)
        plt.subplot()
        nx.draw(network_copy, with_labels=True)
        plt.show()
        
    def update_capacity(self, node_name, capacity):
        succ = list(self.dg.successors(node_name))[0]
        self.dg[node_name][succ]['capacity'] = capacity
        
    def link_capacity(self, upstream_name, downstream_name, capacity):
        self.dg[upstream_name][downstream_name]['capacity'] = capacity
    
    def update_all(self, capacity_dict):
        """Change this so the parameter is a simple dict of node: flow values
            Ex. capacity_dict = {'C1': 5.4, 'C2': 2.65, 'C3': 0.44}"""
        # build the edge tuples from the nodes
        for node_name, capacity in capacity_dict.items():
            self.update_capacity(node_name, capacity)
        # nx.set_edge_attributes(self.dg, capacity_dict)
    
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
        
        flow_dict = self.calc_flows()
        pred_list = list(self.dg.predecessors('sink'))
        pred = 0.0
        for i in pred_list:
            pred += flow_dict[i]['sink']
        return pred
    
    def calc_flows(self):
        """ Uses the method of choice to calculate the flows at all nodes.
        
            Returns
            -------
            flow dictionary
        """
        flow_dict = {}
        if self.calc_method == 'max':
            flow_value, flow_dict = nx.maximum_flow(self.dg, self.source, self.sink, capacity='capacity')
        elif self.calc_method == 'min_cost':
            flow_cost, flow_dict = nx.network_simplex(self.dg)
            
        return flow_dict
    
    def outflow_at_node(self, node_name):
        succ = list(self.dg.successors(node_name))[0]
        flow_dict = self.calc_flows()
        return flow_dict[node_name][succ]
    
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

