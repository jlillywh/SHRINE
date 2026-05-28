from math import pi
from numerical.root_zero import Root
from hydraulics.pressure_conduit_funcs import friction_loss
import scipy.constants as const


class Pipe:
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
    def __init__(self, length=1000.0, diameter=1.0, material='concrete', minor_loss=1.7):
        self.length = length
        self.diameter = diameter
        self._material = material
        self.hazen_williams = 120
        self.roughness = 0.2 / 1000.0
        self.k = minor_loss
        self.f = 0.02
    
    @property
    def material(self) -> str:
        return self._material
     
    @material.setter
    def material(self, new_material: str):
        self._material = new_material
        self.assign_roughness(new_material)
        
    @property
    def area(self) -> {'type': float, 'units': 'm2'}:
        return pi * self.diameter ** 2 / 4.0
    
    @property
    def wet_perim(self) -> {'type': float, 'units': 'm'}:
        return pi * self.diameter
        
    @property
    def hyd_radius(self) -> {'type': float, 'units': 'm'}:
        return self.area / self.wet_perim
    
    def assign_roughness(self, material):
        if material == 'concrete':
            self.hazen_williams = 130
            self.roughness = 0.5 / 1000    # m
        elif material == 'steel':
            self.hazen_williams = 120
            self.roughness = 0.1 / 1000    # m
        elif material == 'plastic':
            self.hazen_williams = 140
            self.roughness = 0.01 / 1000   # m
        else:
            self.hazen_williams = 125
            self.roughness = 0.2 / 1000    # m
    
    def minor_loss(self, flow_rate) -> {'type': float, 'units': 'm'}:
        """Calculate the minor loss in head loss
            Parameters
            ----------
            flow_rate : pint Quantity of volumetric flow (volume per time)
            
            Returns
            -------
            head loss in SI units : pint
        """
        
        velocity = flow_rate / self.area
        return self.k * (velocity ** 2 / (2.0 * const.g))
    
    def head_loss(self, flow_rate, method='HW') -> {'type': float, 'units': 'm'}:
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
        fl = friction_loss(self, flow_rate, method)
        ht = ml + fl
        return ht
    
    def compare_h(self, q, delta_elevation):
        """Determine if head loss is greater than delta elevation
            This is used internally for friction loss calculations.
            
            Parameters
            ----------
                delta_elevation : float
                    Difference in elevation
                q : float
                    Flow rate
        """
        return self.head_loss(q) > delta_elevation
    
    def gravity_flow(self, delta_elevation, method='HW') -> {'type': float, 'units': 'm3/d'}:
        """Calculates the flow rate given the known delta elevation
            
            Parameters
            ----------
            delta_elevation : pint Quantity as a length
            method : str
            
            Returns
            -------
            flow rate in terms of pint Quantity of 'cfs'
        """
        
        f = lambda q: self.head_loss(q, method) > delta_elevation
        func = Root()
        return func.binary_search(f)

