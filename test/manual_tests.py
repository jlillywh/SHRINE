import pandas as pd
import os
from data_external.fileman import FileManager
from inputs.const import Vector
from results.bar_chart import Bar

dir_path = '..\data_external'
fileman = FileManager(dir_path)

file_name = 'data.xlsx'
fileman.add_file(file_name)

xls_file = fileman.get_file(file_name)

table = xls_file.parse(sheet_name='Sheet1', name='evaporation', header=4, index_col=0)
xls_file.close()

v1 = Vector('evap', 'in', table.values[:,0], table.index)

b = Bar()
b.add_output(v1)

b.show()



