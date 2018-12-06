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


sa = StoreArray(4)
inflow = [2.5, 7.8, 23.65]
outflow = [11.0, 0.0, 2.2]
sa.update(inflow, outflow)