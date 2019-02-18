from data.fileman import FileManager
import pandas as pd
from inputs.const import Vector
from results.time_history import TimeHistory
from results.ts_chart import TimeHistoryChart
from global_attributes.clock import Clock


"""This is a test model. Used to test my library to see if I can build a model using
    its features and modules.
    
    This model replicates the work done in the IWRM SLC V9.111.gsm model."""
fm = FileManager('..\\data_external')
input_file = fm.add_file('data.xlsx')

xls_file = pd.ExcelFile(input_file)

monthly_data = pd.read_excel(xls_file, 'Monthly')
xls_file.close()
c = Clock()

evap_table = Vector('Evaporation', 'in', monthly_data['Evap'])
precip_table = Vector('Precipitation', 'in', monthly_data['Precip'])

e_ts = pd.Series(name='evaporation')
p_ts = pd.Series(name='precip')
th1 = TimeHistory('Climate Results', 'in', c)


while c.running:
    """Set up the run properties"""
    month = c.current_date.month_name()
    dayofyear = c.current_date.dayofyear
    
    """Define input variables"""
    evap_rate = evap_table[month]
    precip_rate = precip_table[month]
    
    """Append daily results to time series"""
    e_ts[c.current_date] = evap_rate
    p_ts[c.current_date] = precip_rate
    
    """Advance the simulation clock forward by a time step"""
    c.advance()
    
th1.add_series(e_ts)
th1.add_series(p_ts)

th1.show()
