from data.fileman import FileManager
import pandas as pd
from inputs.const import Vector
from results.bar_chart import Bar
from results.ts_chart import TimeSeriesChart

dir_path = '..\data_external'
fileman = FileManager(dir_path)

file_name = 'data.xlsx'
fileman.add_file(file_name)
fileman.add_file('timeseries_data1.csv')

xls_file = pd.ExcelFile(fileman.file_list[file_name])

#table = xls_file.parse(sheet_name='Monthly', name='monthly data').to_dict()

df = pd.read_excel(xls_file, 'Monthly')

xls_file.close()
print(type(df['Evap']))

v1 = Vector('Evaporation', 'in', df['Evap'])

b = Bar('Evap')
b.add_output(v1)

b.show()

from inputs.time_series import TimeSeries


ts1 = TimeSeries('Rainfall')
ts1.load_csv(fileman.file_list['timeseries_data1.csv'])

th = TimeSeriesChart('Rainfall')



