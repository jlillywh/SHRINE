from watershed import Watershed
from catchment import Catchment

w = Watershed()
w.add_inflow(Catchment(), 'J1')
w.add_junction('J5')
w.add_inflow('J5', 'J1')
w.add_inflow(Catchment(), 'J5')
for i in range(0,10):
    precip = 500.0
    et = 0.0
    w.update(precip, et, w.outflow_node)
    print(w.outflow)