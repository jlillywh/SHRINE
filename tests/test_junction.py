from hydrology.watershed import Watershed
from hydrology.catchment import Catchment

w = Watershed()
w.add_node(Catchment(), 'J1')
w.add_junction('J5')
w.add_node('J5', 'J1')
w.add_node(Catchment(), 'J5')
for i in range(0,10):
    precip = 500.0
    et = 0.0
    w.update(precip, et, w.sink_node)
    print(w.outflow)