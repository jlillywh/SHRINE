from awbm import Awbm
from store_array import StoreArray

catchment = Awbm()

precip = 10.0
et = 1.0
catchment.buckets.set_quantities([4.2, 140.4, 42.9])
catchment.base.set_quantity(10.0)
catchment.surface.set_quantity(10.0)
runoff = catchment.runoff(precip, et)

print("Bucket amounts = " + str(catchment.buckets.total_quantity()))
print("Bucket overflow = " + str(catchment.buckets.total_overflow()))
print("Surface Store amount = " + str(catchment.surface._quantity))
print("Baseflow Store amount = " + str(catchment.base._quantity))

print("Catchment runoff = " + str(runoff))

sa = StoreArray()
inflow = [2.5, 7.8, 23.65]
outflow = [11.0, 0.0, 2.2]
sa.update(inflow, outflow)