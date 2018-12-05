from awbm import Awbm
from store_array import StoreArray
area = 34.0
catchment = Awbm()

precip = 100.0
et = 0.0
runoff = 0.0

for x in range(3):
    catchment.runoff(precip, et)

runoff = catchment.runoff(0.0, 0.0)
print(runoff)


s = StoreArray()
inflow = [100.0, 50.0, 25.0]
outflow = [1.0, 10.0, 20.0]
s.update(inflow, outflow)
s.transfer(0,1,100.0)