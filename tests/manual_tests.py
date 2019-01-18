from watershed import Watershed

w = Watershed()
w.add_catchment('c2', 'j1')
w.add_junction('j2', 'j1')
w.add_catchment('c3', 'j2')
w.add_catchment('c4', 'j2')
w.add_junction('j3', 'j2')

#n.edges['c3', 'j2']['runoff'] = 2.0
#print(n['c3'])

#flow_value, flow_dict = nx.maximum_flow(n, 'A', 'j1', capacity='runoff')
#print(flow_value)

#draw(n)
#walk = nx.bfs_tree(n, source='j1', reverse=True)
#print(nx.transitive_closure(n))

#sub = nx.bfs_tree(n, source='j3', reverse=True)
#for i in list(sub.nodes):
#    print(i)
#    n.remove_node(i)
#draw(n)




