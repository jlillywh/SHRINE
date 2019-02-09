from global_attributes.aegis import Aegis
import pandas as pd

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
        Aegis.__init__(self)
        month_list = ['January', 'February', 'March', 'April',
                      'May', 'June', 'July', 'August',
                      'September', 'October', 'November', 'December']
        self.listSet = {'Months': month_list}
        
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
        
    