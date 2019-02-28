import numpy as np
import matplotlib.pyplot as plt
from results.chart import Chart
from pandas import Series
from inputs.data import Vector


class Bar(Chart):
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
    
    def __init__(self, name):
        Chart.__init__(self, name)
        self.values = []
        self.y_pos = [0]

    def add_output(self, output):
        self.outputs.append(output)
        if type(output) == float:
            self.values.append(output.data)
            self.output_names.append(output.name)
        elif type(output) == list:
            for i in output.data:
                self.values.append(i)
                self.output_names.append(i)
            self.ylabel = "[" + str(self.outputs[0].unit) + "]"
        elif type(output) == Vector:
            self.update_title(output.name)
            self.values = output.values
            self.output_names = output.index
            self.xlabel = output.listSet
            self.ylabel = '[' + output.unit + ']'
        elif type(output) == dict:
            for key, value in output.data.items():
                self.output_names.append(key)
                self.values.append(value)
                self.xlabel = output.listSetName
                self.ylabel = "[" + str(self.outputs[0].unit) + "]"
        elif type(output) == Series:
            for key, value in output.data.items():
                self.output_names.append(key)
                self.values.append(value)
                self.xlabel = output.name
                self.ylabel = "[" + str(self.outputs[0].unit) + "]"
        else:
            raise TypeError(
                'Parameter should be a Scalar or list of Scalar')
        self.num_outputs = len(self.output_names)
        self.rotation(self.output_names)
        self.y_pos = np.arange(self.num_outputs)
    
    def show(self):
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(self.y_pos, self.output_names, rotation=self.rotate_labels)
        plt.subplots_adjust(bottom=self.space_bottom)
        plt.bar(self.y_pos, self.values, align='center')
        plt.show()
        plt.close()
        
    
        
    

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