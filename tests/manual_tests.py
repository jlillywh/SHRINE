from watershed import Watershed
from catchment import Catchment

import networkx as nx

w = Watershed()
w.add_catchment('c2', 'J1')
w.add_junction('j2', 'J1')
w.add_catchment('c3', 'j2')
w.add_catchment('c4', 'j2')
w.add_junction('j3', 'j2')
w.add_catchment('c5', 'j3')
w.add_catchment('c6', 'j3')

runoff = 0.0
for i in w.network.nodes:
    #print("node is type " + str(w.network.nodes[i]['type']))
    if w.network.nodes[i]['type'] == Catchment:
        
        w.network.nodes[i]['type'].update_runoff(10.0, 1.0)
        runoff = w.network.nodes[i]['type'].outflow
    print(runoff)

w.draw()

#n.edges['c3', 'j2']['runoff'] = 2.0
#print(n['c3'])

flow_value, flow_dict = nx.maximum_flow(w.network, 'A', 'J1', capacity='runoff')
print(flow_value)

#draw(n)
#walk = nx.bfs_tree(n, source='j1', reverse=True)
#print(nx.transitive_closure(n))

#sub = nx.bfs_tree(n, source='j3', reverse=True)
#for i in list(sub.nodes):
#    print(i)
#    n.remove_node(i)
#draw(n)




