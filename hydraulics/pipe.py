from global_attributes.aegis import Aegis
from math import pi
from inputs.constants import G, nu, U
from numerical.root_zero import Root
import math
from hydraulics.pressure_conduit_funcs import friction_loss


class Pipe(Aegis):
    """Class for creating pipe segments
    
        Attributes
        ----------
        length : pint Quantity (length)
        diameter : pint Quantity (length)
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
    
    def __init__(self, length=1000.0 * U.m, diameter=1.0 * U.m, material='concrete', k=1.7):
        """Input length, diameter, material as optional
        
            Parameters
            ----------
            length : pint Quantity of length
            diameter : pint Quantity of length
            material : str
                Choice of concrete, steel, plastic
                #TODO add more material options perhaps from a table in a file
            k : float
                Minor loss coefficient
            
        """
        
        Aegis.__init__(self)
        self.length = length
        self.diameter = diameter
        self._material = material
        self.hazen_williams = 125
        self.roughness = 0.0006562 * U.ft
        self.assign_roughness(material)
        self.k = k
        self.f = 0.02
    
    def assign_roughness(self, material):
        if material == 'concrete':
            self.hazen_williams = 130
            self.roughness = 0.00164 * U.ft
        elif material == 'steel':
            self.hazen_williams = 120
            self.roughness = 0.0003281 * U.ft
        elif material == 'plastic':
            self.hazen_williams = 140
            self.roughness = 3.28e-5 * U.ft
        else:
            self.hazen_williams = 125
            self.roughness = 0.0006562 * U.ft
    
    @property
    def material(self):
        return self._material
     
    @material.setter
    def material(self, new_material):
        self._material = new_material
        self.assign_roughness(new_material)
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
        """Calculate the minor loss in head loss
            Parameters
            ----------
            flow_rate : pint Quantity of volumetric flow (volume per time)
            
            Returns
            -------
            head loss in SI units : pint
        """
        
        velocity = flow_rate / self.area
        hm = self.k * (velocity ** 2 / (2.0 * G))
        return hm.to(U.ft)
    
    def head_loss(self, flow_rate, method='HW'):
        """Calculates the total head loss in the pipe section
        
            Parameters
            ----------
            flow_rate : pint Quantity of volumetric flow rate.
            method : str
                Choice of 'HW' for Hazen-Williams or
                'DW' for Darcy-Weisbach
                
            Returns
            -------
            head loss in terms of Quantity feet
        """
        
        ml = self.minor_loss(flow_rate)
        fl = friction_loss(self, flow_rate, method).to(U.ft)
        ht = ml + fl
        return ht
    
    def compare_h(self, q, delta_elevation):
        """Determine if head loss is greater than delta elevation
            This is used internally for friction loss calculations.
            
            Parameters
            ----------
                delta_elevation : pint Quantity in length
        """
        return self.head_loss(q) > delta_elevation
    
    def gravity_flow(self, delta_elevation, method='HW'):
        """Calculates the flow rate given the known delta elevation
            
            Parameters
            ----------
            delta_elevation : pint Quantity as a length
            
            Returns
            -------
            flow rate in terms of pint Quantity of 'cfs'
            #TODO fix this method. Units error
        """
        
        f = lambda q: self.head_loss(q, method) > delta_elevation
        func = Root()
        return func.binary_search(f)

