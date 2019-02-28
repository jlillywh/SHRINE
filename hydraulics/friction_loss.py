"""This file is used to calculate flow rate in a pipe using Bernoulli's
    energy equation
    
    For solving flow rate, use Bernoulli's energy equation at steady state
    between upstream and downstream points. Use Hazen-Williams formula for
    calculating head loss in the pipe due to friction.
    
    Units are in English: elev (ft), flow (cfs), dia (in), length (ft)"""
import math
from inputs.constants import G, U
from hydraulics.pipe import Pipe


G = G.to(U.ft / U.second**2)

# Set up input parameters
z1 = 40.0 * U.ft
z2 = 10.0 * U.ft

dia = 1.0 * U.ft
length = 1000.0 * U.ft
chw = 120
k = sum([0.4, 1.2, 0.1])
p1 = Pipe(1000.0, 1.0, 'steel', sum(k))

# Energy equation for orifice and pipe flow

# Set up initial guess values for binary search
a = math.pi * dia**2 / 4.0
p = math.pi * dia
r = a / p
low = 0.0 * U.cfs
high = 1.0e9 * U.cfs
mid = (high - low) / 2
converged = False
conv_error = 0.01
loop_count = 0

# Max number of loops before issuing convergence error
MaxLoops = 200

# Minor head losses
minor_head_loss = 0.0 * U.ft

# Friction headloss (emperical equation)
friction_head_loss = 0.0 * U.ft

# Total head loss
head_loss = minor_head_loss + friction_head_loss

# Friction, minor head losses plus the velocity head at the end
elevation_delta = z1 - z2

vel = mid / a
vel = vel.to(U.ft / U.second)

# Perform binary search algorithm to solve for flow rate
while not converged:
    mid = low + (high - low) / 2.0
    m_mag = mid.magnitude
    minor_head_loss = p1.minor_loss(m_mag)
    friction_head_loss = p1.friction_loss(m_mag) * U.ft
    head_loss = min(minor_head_loss + friction_head_loss, elevation_delta)
    
    # Bernoulli's Equation for Conservation of Energy
    #    Assume start and end points are open to atmospheric pressure
    #    Assume zero velocity in the lake
    q = ((elevation_delta - head_loss) * 2 * G) ** 0.5 * a
    
    # Contract the range based on whether the midpoint guess was too high or too low
    if q < mid:
        high = mid
    else:
        low = mid
    
    # Check for convergence
    if loop_count > MaxLoops:
        print("Flow solver did not converge after " + str(MaxLoops) + " iterations!")
        break
    
    converged = (high - low) / mid <= conv_error
    loop_count = loop_count + 1

# Energy grade slope
s = head_loss / length

# Check accuracy using Hazen-William's Head Loss Equation
# Double check the head loss using HW method and calculated flow rate
q_mag = q.magnitude
a_mag = a.magnitude
r_mag = r.magnitude
hL_HW = (q_mag**1.852 * l_mag / ( 1.67 * chw**1.852 * a_mag**1.852 * r_mag**1.17)) * U.ft

print("Flow is: " + str(q))
print("Head loss is: " + str(head_loss))