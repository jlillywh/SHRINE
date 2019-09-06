import os.path
import datetime


class File:
    """ File objects for the file manager
    
        Attributes
        ----------
        name
        file_type
        
        Methods
        -------
        name()
            returns the name of the file
            
        save()
            Saves the file to given directory
        
    """
    extensions = ['xlsx', 'xls', 'xlsm', 'csv', 'txt']
    
    def __init__(self, name):
        self.name = name
        self.file_type = name.split('.', 1)[1]
        self.validate_ext()
        self.save()
    
    def save(self, path):
        print(os.path.abspath('.'))

        with open(self.name, 'w') as f:
            f.write('Edited: ' + str(datetime.datetime.now()))
        
    def edit(self):
        os.system(self.name)
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, n):
        self._name = n
        ext = n.split('.', 1)[1]
        if self.validate_ext():
            self.file_type = ext
            self._name = n
        else:
            raise Exception('Invalid file type')
        
    def validate_ext(self):
        file_type = self._name.split('.', 1)[1]
        if file_type in self.extensions:
            return True
        else:
            return False
