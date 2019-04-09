from results.live_plotter import live_plotter
import numpy as np
import datetime

base = datetime.datetime.today()
size = 10
date_list = [base - datetime.timedelta(days=x) for x in range(0, size)]

#x_vec = np.linspace(0,1,size+1)[0:-1]
x_vec = date_list
y_vec = np.random.randn(len(date_list))
line1 = []
while True:
    rand_val = np.random.randn(1)
    y_vec[-1] = rand_val
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)