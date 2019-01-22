from watershed import Watershed
import matplotlib.pylab as plt
import networkx as nx
from pathlib import Path

data_folder = Path("../data/")

fname = data_folder / "watershed_adj_input"
#fname = data_folder / "watershed_GML_input.xml"

with open(fname, 'r') as f:
    content = f.readlines()

g = nx.parse_adjlist(content)

plt.subplot()
nx.draw(g, with_labels=True)
plt.show()

w = Watershed()
w.add_catchment('c2', 'J1')
w.add_catchment('c3', 'n2')
w.add_catchment('c4', 'n2')
w.add_catchment('c5', 'n3')
w.add_catchment('c6', 'n3')
w.add_junction('n3', 'n2')
w.add_junction('n2', 'J1')

for i in range(0,10):
    w.update(5.2, 0.2)
    print(w.outflow)

w.draw()