import pandas as pd
import os


class SetLabel:
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
        self.df = pd.read_csv(csv_file)
        
        frames = []
        for col in self.df.columns.values:
            frames.append(pd.DataFrame(self.df[col]))
            
        self.list_set = {}
        keys = self.df.columns.values
        self.list_set = dict(zip(keys, frames))
        
        for key, value in self.list_set.items():
            self.list_set[key] = value.dropna()
        
    # month_list = ['January', 'February', 'March', 'April',
    #               'May', 'June', 'July', 'August',
    #               'September', 'October', 'November', 'December']
    # list_set = {'Months': month_list}
    
    def add_list(self, name, items):
        self.list_set.update({name: items})
    
    def get_list(self, name):
        return self.list_set[name]
    
    def delete_list(self, name):
        del self.list_set[name]
    
    def print_list(self, name):
        d= {name: self.list_set[name]}
        p = pd.DataFrame.from_dict(d)
        return p
        
    