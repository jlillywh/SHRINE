from data.fileman import FileManager
from inputs.table import Table


fm = FileManager('..\\data_external')
filename = 'data.xlsx'
fm.add_file(filename)
input_file = fm.file_list[filename]

t = Table()
t.load_from_excel(input_file, 'Table', 'a4')
t.plot()