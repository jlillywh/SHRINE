"""This is a test model. Used to test my library to see if I can build a model using
    its features and modules."""

from data.fileman import FileManager
import pandas as pd
from inputs.const import Vector
from results.time_history import TimeHistory
from results.ts_chart import TimeHistoryChart
from global_attributes.clock import Clock


fm = FileManager('..\\data_external')
input_file = fm.add_file('data.xlsx')

xls_file = pd.ExcelFile(input_file)

monthly_data = pd.read_excel(xls_file, 'Monthly')
xls_file.close()
c = Clock()

evap_table = Vector('Evaporation', 'in', monthly_data['Evap'])
evap_ts = TimeHistory('Evaporation', 'in', c)



while c.running:
    month = c.current_date.month_name()
    e = evap_table[month]
    evap_ts.set_value(c.current_date, e)
    c.advance()
    
evap_ts.show()