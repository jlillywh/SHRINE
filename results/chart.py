import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from global_attributes.aegis import Aegis
from pandas import Series


class Chart(Aegis):
    """Class to create a generic charting object
    """
    def __init__(self, name):
        Aegis.__init__(self)
        self.update_title(name)
        self.ylabel = ''
        self.xlabel = ''
        self.unit = ''
        self.outputs = []
        self.output_names = []
        self.num_outputs = 0
        self.rotate_labels = 'horizontal'
        self.space_bottom = 0.1
        
    def show(self):
        self.num_outputs = len(self.values)
        self.y_pos = np.arange(self.num_outputs)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        
        plt.show()

    def update_title(self, new_title):
        self.title = new_title
        plt.title(new_title)
        
    def rotation(self, list_of_labels):
        """Determins rotation based on longest item
            in the list
        """
        try:
            lst_sorted = sorted(list_of_labels, key=len)
        except TypeError:
            list_of_labels = [str(item) for item in list_of_labels]
            lst_sorted = sorted(list_of_labels, key=len)

        char_length = len(lst_sorted[-1])
        if char_length > 4:
            self.rotate_labels = 60.0
            self.space_bottom = 0.25