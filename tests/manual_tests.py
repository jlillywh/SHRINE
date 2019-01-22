from watershed import Watershed

w = Watershed()
w.add_catchment('c2', 'J1')
w.add_catchment('c3', 'n2')
w.add_catchment('c4', 'n2')
w.add_catchment('c5', 'n3')
w.add_catchment('c6', 'n3')
w.add_junction('n3', 'n2')
w.add_junction('n2', 'J1')

for i in range(0,10):
    w.update(5.2, 0.2)
    print(w.outflow)

w.draw()