from data.fileman import FileManager
import pandas as pd
from inputs.const import Vector
from results.bar_chart import Bar

dir_path = '..\data'
fileman = FileManager(dir_path)

file_name = 'data.xlsx'
fileman.add_file(file_name)

xls_file = pd.ExcelFile(fileman.file_list[file_name])

#table = xls_file.parse(sheet_name='Monthly', name='monthly data').to_dict()

df = pd.read_excel(xls_file, 'Monthly')

xls_file.close()
print(type(df['Evap']))

v1 = Vector('Evaporation', 'in', df['Evap'])

b = Bar()
b.add_output(v1)

b.show()



