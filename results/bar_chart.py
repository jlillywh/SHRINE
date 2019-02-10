import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from global_attributes.aegis import Aegis
from pandas import Series

class Bar(Aegis):
    """Bar chart class
    
        Properties
        ----------
        rotate_labels : str (default = 'horizontal')
            A flag used to rotate the labels on the x axis
            This is set to true if crowding occurs.
        space_bottom : float (default = 0.1)
            Increase this value to provide more space at
            the bottom of the chart for rotated xaxis labels
    """
    
    def __init__(self):
        Aegis.__init__(self)
        #self.bar_width = 0.35
        self.title = "Bar Chart"
        self.result = []
        self.ylabel = ''
        self.xlabel = 'Items'
        self.unit = ''
        self.output_names = []
        self.values = []
        self.rotate_labels = 'horizontal'
        self.space_bottom = 0.1

    def add_output(self, output):
        self.result.append(output)
        if type(output.data) == float:
            self.values.append(output.data)
            self.output_names.append(output.name)
        elif type(output.data) == list:
            for i in output.data:
                self.values.append(i)
                self.output_names.append(i)
        elif type(output.data) == dict:
            for key, value in output.data.items():
                self.output_names.append(key)
                self.values.append(value)
                self.xlabel = output.listSetName
        elif type(output.data) == Series:
            for key, value in output.data.items():
                self.output_names.append(key)
                self.values.append(value)
                self.xlabel = output.name
        else:
            raise TypeError(
                'Parameter should be a Const or list of Const')
        self.rotation(self.output_names)
        self.ylabel = "[" + str(self.result[0].unit) + "]"
        self.unit = self.result[0].unit
        self.num_outputs = len(self.values)
        self.y_pos = np.arange(self.num_outputs)
    
    def show(self):
        self.num_outputs = len(self.values)
        self.y_pos = np.arange(self.num_outputs)
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(self.y_pos, self.output_names, rotation=self.rotate_labels)
        plt.subplots_adjust(bottom=self.space_bottom)
        plt.bar(self.y_pos, self.values, align='center')
        plt.show()
        
    def rotation(self, list_of_labels):
        """Determins rotation based on longest item
            in the list
        """
        try:
            lst_sorted = sorted(list_of_labels, key=len)
        except TypeError:
            list_of_labels = [str(item) for item in list_of_labels]
            lst_sorted = sorted(list_of_labels, key=len)
        finally:
            print("1 or more list values not correct type!")
            
        char_length = len(lst_sorted[-1])
        if char_length > 4:
            self.rotate_labels = 60.0
            self.space_bottom = 0.25
        
    

# bar_width = 0.35
#
# chart_title = 'Water depth from surface'
#
# well_names = ['Well A', 'Well B', 'Well C']
# means_exist = [3, 10, 7]
# means_future = [4, 8.5, 10]
# # data to plot
#
# x_label = 'Wells'
# y_label = 'Depth (m)'
# scenarios = ['Existing Conditions', 'Future']
#
#
# num_outputs = len(well_names)
# y_pos = np.arange(num_outputs)
# index = np.arange(num_outputs)
#
# plt.bar(y_pos, means_exist, bar_width, align='center')
# plt.xticks(y_pos, well_names)
# plt.ylabel(y_label)
# plt.title(chart_title)
#
# plt.show()
#
#
# # create plot
# fig, ax = plt.subplots()
#
# rects1 = plt.bar(index, means_exist, bar_width, label=scenarios[0])
#
# rects2 = plt.bar(index + bar_width, means_future, bar_width, label=scenarios[1])
#
# plt.xlabel(x_label)
# plt.ylabel(y_label)
# plt.title(chart_title)
# plt.xticks(index + bar_width, well_names)
# plt.legend()
#
# plt.tight_layout()
# plt.show()