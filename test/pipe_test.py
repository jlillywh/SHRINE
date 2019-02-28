from hydraulics.pipe import Pipe

p1 = Pipe(1000.0, 1.0, 'steel', 1.7)

print("Area is: " + str(p1.area))
q = p1.gravity_flow(30.0)
print("Flow rate is: " + str(q))

print("Head loss is: " + str(p1.head_loss(q)))