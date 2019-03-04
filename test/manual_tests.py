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

for i in range(10):
    w.update(10.0, 1.4)

print(w.outflow)



