import os.path


class File:
    """ File objects for the file manager
    
        Attributes
        ----------
        name
        file_type
        
        Methods
        -------
        
    """
    extensions = ['xlsx', 'xls', 'xlsm', 'csv', 'txt']
    
    def __init__(self, name):
        self.name = name
        self.file_type = name.split('.', 1)[1]
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, n):
        ext = n.split('.', 1)[1]
        if ext in self.extensions:
            self.file_type = ext
            self._name = n
        else:
            raise Exception('Invalid file type')
