from aegis import Aegis
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

class Junction(Aegis):
    def __init__(self, name="J"):
        Aegis.__init__(self)

        self.inflows = []
        self.name = name
        G.add_node(self.id)

    def add_inflow(self, node):
        """ Add an Aegis node to the junction"""
        self.inflows.append(node)
        G.add_node(node.id)
        G.add_edge(node.id, self.id)
        
    def draw(self):
        plt.subplot(121)
        nx.draw(G, with_labels=True, font_weight='bold')
        nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
        plt.show()
        

    @property
    def outflow(self):
        sum = 0.0
        for i in range(len(self.inflows)):
            sum += self.inflows[i].outflow
        return sum