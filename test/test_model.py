"""This is a test model. Used to test my library to see if I can build a model using
    its features and modules."""

from data.fileman import FileManager
import pandas as pd
from inputs.const import Const, Vector

fm = FileManager('..\\data_external')
input_file = fm.add_file('data.xlsx')

xls_file = pd.ExcelFile(input_file)

monthly_data = pd.read_excel(xls_file, 'Monthly')
xls_file.close()

evap_table = Vector('Evaporation', 'in', monthly_data['Evap'])


r = 2