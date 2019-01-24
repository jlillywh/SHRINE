from watershed import Watershed

w = Watershed()

precip = 10.0
et = 0.1

for i in range(0,10):
    w.update(precip, et)
    print(w.outflow)
    
