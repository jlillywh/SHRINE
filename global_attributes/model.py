from global_attributes.aegis import Aegis
from global_attributes.simulator import Simulator
from global_attributes.clock import Clock
from global_attributes.set_label import SetLabel
from data.fileman import FileManager


class Model(Aegis):
    def __init__(self):
        Aegis.__init__(self)
        self.clock = Clock()
        self.simulator = Simulator()
        self.listSet = SetLabel()
        
        dir_path = '..\data_external'
        file_name = 'data.xlsx'
        
        fileman = FileManager(dir_path)
        fileman.add_file(file_name)
    
        xls_file = fileman.get_file(file_name)
