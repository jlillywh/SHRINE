from global_attributes.aegis import Aegis
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re       # import regex


class Table(Aegis):
    """Class for creating and using 1D lookup tables
    
        Parameters
        ----------
        x : list(float)
        x_name : str
        y : list(float)
        y_name : str
        
        Methods
        -------
        lookup(value)
            Returns interpolated value
        load_from_excel()
            Store data from excel into x and y arrays
        
    """
    def __init__(self, x=[1, 2, 3], y=[0, 2, 5]):
        Aegis.__init__(self)
        self.x = x
        self.x_name = 'x'
        self.y = y
        self.y_name = 'y'
        
    def lookup(self, lookup_value):
        return np.interp(lookup_value, self.x, self.y)
    
    def load_from_excel(self, filename, sheet, begin_cell):
        """Loads data from Excel file
        
            Parameters
            ----------
            filename : str
                Path and file name
            sheet : str
                Name of the sheet to look in
            begin_cell : str
                Cell that represents the top left corner of the table
        """
        header_row = int(re.findall('\d+', begin_cell)[0]) - 1
        index_col = ord(re.findall('^[A-Za-z]+', begin_cell)[0]) - 97
        df = pd.read_excel(filename, sheet_name=sheet, header=header_row)
        print(df)
        self.x = df['Area']
        self.y = df['Elevation']
        self.x_name = df.columns.values[1]
        self.y_name = df.columns.values[0]
    
    def plot(self):
        plt.scatter(self.x, self.y)
        plt.suptitle(self.name)
        plt.xlabel(self.x_name)
        plt.ylabel(self.y_name)
        plt.show()
