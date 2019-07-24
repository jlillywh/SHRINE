from global_attributes.constants import U
from hydrology.watershed import Watershed
from data.fileman import FileManager

fm = FileManager('.\\data_external')
fm = FileManager('..\\data_external')
filename = 'watershed_GML_input.gml'
fm.add_file(filename)
w = Watershed()
w.load_from_file(fm.files[filename])
n = w.network

n.adj['J1']['J2']['runoff'] = 99 * U.m3 / U.day

print(n.adj['J1']['J2']['runoff'] )