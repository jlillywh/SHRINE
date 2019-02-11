from global_attributes.aegis import Aegis
import pandas as pd
import csv
import os

class SetLabel(Aegis):
    """Class for holding a group of lists
    
        By default, the set contains 2 lists. All lists
        get stored inside a pandas DataFrame
    
        Attributes
        ----------
            name : str
            
            items : list
                Default is an empty list
        
        Methods
        -------
        add_list(name, items)
        get_list(name)
            returns a list of items
        remove_list(name)
    
    """
    
    def __init__(self):
        data_dir = self.dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..\data'))
        csv_file = data_dir + '\\' + 'labelsets.csv'
        self.listSet = {}
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            self.listSet = {rows[0]: rows[1:] for rows in reader}
        
    # month_list = ['January', 'February', 'March', 'April',
    #               'May', 'June', 'July', 'August',
    #               'September', 'October', 'November', 'December']
    # listSet = {'Months': month_list}
    
    def add_list(self, name, items):
        self.listSet.update({name: items})
    
    def get_list(self, name):
        return self.listSet[name]
    
    def delete_list(self, name):
        del self.listSet[name]
    
    def print_list(self, name):
        d= {name: self.listSet[name]}
        p = pd.DataFrame.from_dict(d)
        return p
        
    