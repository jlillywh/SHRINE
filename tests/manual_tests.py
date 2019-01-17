import networkx as nx
import matplotlib.pyplot as plt

def draw(graph):
    plt.subplot()
    nx.draw(graph, with_labels=True)
    plt.show()

n = nx.DiGraph()
n.add_edge('A', 'c1')
n.add_edge('A', 'c2')
n.add_edge('A', 'c3')
n.add_edge('A', 'c4')
n.add_edge('A', 'c5')
n.add_edge('A', 'c6')
n.add_node('c1', type='catchment')
n.add_node('c2', type='catchment')
n.add_node('c3', type='catchment')
n.add_node('c4', type='catchment')
n.add_node('c5', type='catchment')
n.add_node('c6', type='catchment')
n.add_node('j1', type='catchment')
n.add_node('j2', type='catchment')
n.add_node('j3', type='catchment')
n.add_edge('c1', 'j1', runoff=1.0)
n.add_edge('c2', 'j1', runoff=1.0)
n.add_edge('j2', 'j1')
n.add_edge('c3', 'j2', runoff=1.0)
n.add_edge('c4', 'j2', runoff=1.0)
n.add_edge('j3', 'j2')
n.add_edge('c5', 'j3', runoff=1.0)
n.add_edge('c6', 'j3', runoff=1.0)

n.edges['c3', 'j2']['runoff'] = 2.0

flow_value, flow_dict = nx.maximum_flow(n, 'A', 'j1', capacity='runoff')
print(flow_value)

draw(n)
walk = nx.bfs_tree(n, source='j1', reverse=True)
print(nx.transitive_closure(n))

sub = nx.bfs_tree(n, source='j3', reverse=True)
for i in list(sub.nodes):
    print(i)
    n.remove_node(i)
draw(n)




