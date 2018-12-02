from awbm import AWBM
area = 34.0
catchment = AWBM(area)

precip = 13.54
et = 0.89
runoff = 0.0

for x in range(3):
    catchment.runoff(precip, et)

runoff = catchment.runoff(0.0, 0.0)
print(runoff)

