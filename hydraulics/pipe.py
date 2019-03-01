from global_attributes.aegis import Aegis
from math import pi
from inputs.constants import G_english, U
from numerical.root_zero import Root
from hydraulics.pressure_conduit_funcs import friction_loss


class Pipe(Aegis):
    """Class for creating pipe segments
    
        Attributes
        ----------
        length : float
        diameter : float
        material : str
            The material of the pipe segment
            Choices are: concrete, steel, plastic
        
        Methods
        -------
        area()
        wet_perim()
        hyd_radius()
        
        friction_loss(flow_rate)
            Returns the head loss due to friction only
            
        minor_loss(flow_rate)
            Returns the sum of all minor losses in this pipe section
            as a function of obstructions or changes such as
            bends, valves, meters, etc.
        
        head_loss()
            Returns the head loss from pressure flow due to
            friction and minor losses
            
        gravity_flow(delta_elevation)
            Returns flow rate by gravity if upstream head > downstream
            based on Bernoulli's energy equation
            Assume start and end points are open to atmospheric pressure
            and zero velocity upstream
        
    """
    
    def __init__(self, length=1000.0, diameter=1.0, material='concrete', k=1.7):
        Aegis.__init__(self)
        self.length = length
        self.diameter = diameter
        self.type = material
        
        if material == 'concrete':
            self.hazen_williams = 130
        elif material == 'steel':
            self.hazen_williams = 120
        elif material == 'plastic':
            self.hazen_williams = 140
        else:
            self.hazen_williams = 100
        
        self.k = k
     
    @property
    def area(self):
        return pi * self.diameter ** 2 / 4.0
    
    @property
    def wet_perim(self):
        return pi * self.diameter
        
    @property
    def hyd_radius(self):
        return self.area / self.wet_perim
    
    def minor_loss(self, flow_rate):
        velocity = flow_rate / self.area
        hm = self.k * (velocity ** 2 / (2.0 * G_english))
        return hm
    
    def head_loss(self, flow_rate):
        return friction_loss(self, flow_rate) + self.minor_loss(flow_rate)
    
    def compare_h(self, q, delta_elevation):
        return self.head_loss(q) > delta_elevation
    
    def gravity_flow(self, delta_elevation):
        f = lambda q: self.head_loss(q) > delta_elevation
        func = Root()
        return func.binary_search(f)

