import networkx as nx
import matplotlib.pyplot as plt
from data.fileman import FileManager
from hydrology.watershed import Watershed


fm = FileManager('..\\data_external')
filename = 'watershed_GML_input.gml'
fm.add_file(filename)
watershed_input_file = fm.file_list[filename]

# Create a new watershed from file
w = Watershed()
w.load_from_file(watershed_input_file)
w.draw()

G = nx.read_gml(watershed_input_file)
print(G.nodes)
plt.subplot()
nx.draw(G, with_labels=True)
plt.show()



