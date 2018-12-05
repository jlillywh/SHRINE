from awbm import Awbm
area = 34.0
catchment = Awbm()

precip = 100.0
et = 0.0
runoff = 0.0

for x in range(3):
    catchment.runoff(precip, et)

runoff = catchment.runoff(0.0, 0.0)
print(runoff)

