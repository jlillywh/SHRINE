from data.fileman import FileManager
from inputs.time_series import TimeSeries
import pandas as pd
from inputs.data import Vector
from results.bar_chart import Bar
from results.ts_chart import TimeHistoryChart

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

ts1 = TimeSeries('Rainfall')
ts1.load_csv(fileman.file_list['timeseries_data1.csv'])
ts2 = ts1

th1 = TimeHistoryChart('Rainfall')
th1.add_result(ts1)
th1.add_result(ts2)



b.show()
th1.show()



