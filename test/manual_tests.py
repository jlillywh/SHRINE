import pandas as pd
import os
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data_external'))
print(dir_path)
xls_file = pd.ExcelFile(dir_path + '\data.xlsx')

table = xls_file.parse(sheet_name='Sheet1', header=4, index_col=0)

print(table)

