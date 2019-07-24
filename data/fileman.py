import os.path
from dataclasses import make_dataclass
from pathlib import Path


class FileManager:
    """Class for creating a file manager for managing all
    external files in 1 place.
    
    Attributes
    ----------
    files : list(File objects)
        a list containing the path and name of each file
        
    Methods
    -------
    directory(new_directory)
        change the directory
    add_file
        Add an existing file to the manager
    get_file(file_path or nickname)
        Find and retrieve an existing file from the manager
    create_file
        Creates a new file and adds it to the list
        TODO: add this function
    drop_file
        Removes a file from the manager
    print_files
        Prints out a list of all the files in the manager
    is_empty
        Returns true if there are no files in the manager
    """
    def __init__(self, dir_name=''):
        # Check to make sure the directory exists
        new_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\' + dir_name + '\\'))
        if os.path.isdir(new_path):
            self._directory = new_path
        else:
            print('The directory {} does not exist.'.format(dir_name))
            self._directory = os.path.dirname(os.path.abspath(__file__))
            print("Directory set to " + self._directory)
        self.File = make_dataclass('File', ['id', 'name', 'path'])
        self.files = []
        
    @property
    def directory(self):
        return self._directory
    
    @directory.setter
    def directory(self, new_directory):
        """ Set the new directory.
            Parameters
            ----------
            new_directory: str
                name of the new directory. This is relative to the project path"""
        new_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\' + new_directory + '\\'))
        if os.path.isdir(new_path):
            self._directory = new_path
        else:
            print('The directory {} does not exist.'.format(new_directory))
            self._directory = os.path.abspath(__file__ + "/../../")
            print("Directory set to " + self._directory)
        
    def add_file(self, name):
        """ Adds an existing file to the list of files
            File must be existing. If not, throw error.
            TODO: prevent adding duplicates
        
            Parameters
            ----------
            name : str
                Must include the suffix of the file name
        """
        file_id = len(self.files)
        file_name = name
        path = self._directory + file_name
        # check if the file exists
        if os.path.exists(path):
            file = self.File(file_id, file_name, path)
            self.files.append(file)
            return file.name
        else:
            raise FileNotFoundError('The file, {} does not exist!'.format(file_name))
        
    def get_file(self, file):
        # first see if the file exists in the list
        if file in self.files:
            return self.files[file]
        else:
            raise KeyError('Not in list!')
        
    def drop_file(self, file):
        if file in self.files:
            self.files.remove(file)
            return True
        else:
            return False
        
    def is_empty(self):
        return self.files == []
        
    def print_files(self):
        for file in self.files:
            print(file)
