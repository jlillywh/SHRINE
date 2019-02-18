from global_attributes.aegis import Aegis
import pandas as pd
import os


class FileManager(Aegis):
    """Class for creating a file manager for managing all
    external files in 1 place.
    
    Attributes
    ----------
    file : File object
        the name of the file
    """
    def __init__(self, dir_name=''):
        Aegis.__init__(self)
        self.dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), dir_name + '\\'))
        self.file_list = {}
        
    def add_file(self, name):
        """ Adds a new file to the list of files
        
            Parameters
            ----------
            name : str
                Must include the suffix of the file name
        
        """
        
        new_file = self.dir_path + name
        
        self.file_list.update({name: new_file})
        return new_file
        
    def get_file(self, name):
        return self.file_list[name]