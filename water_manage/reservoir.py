from water_manage.store import Store
import pandas as pd
import math
from inputs.constants import WATER_DENSITY, G


class Reservoir(Store):
    """Class for creating a reservoir object.
    
        Attributes
        ----------
        geometry : DataFrame (pandas)
            A lookup table to relate water depth to volume
        
        outlet_elevation : float
            Elevation of the outlet intake (water level
            above this will cause outflow to occur. If
            water is below this elevation, then no discharge
            through the outlet is possible.
            
        spillway_crest : float
            Elevation of the spillway crest. When the
            water level rises above this, overflow begins
            
        spillway_type : str
            Describes the type of spillway from a list:
            broad, sharp, ogee (default is broad)
        
        bottom : float
            Elevation of the bottom of the reservoir
            
        water_level : float
            Elevation of the water surface
        
        Methods
        -------
        spillway_flow()
            Calculate the spillway flow based on the depth of
            water above the spillway crest
            
    
        
    """
    def __init__(self):
        Store.__init__(self)
        self.geometry = pd.DataFrame([0.0,5.0,10.0], [0.0, 100.0, 120.0])
        self.spillway_crest = 10.0
        self.spillway_type = 'broad'
        self.bottom = 0.0
        self.water_level = 7.5
        self.outlet_elevation = 3.75
    
    @property
    def update_water_level(self):
        """Return the water level that corresponds to the current
            water quantity in the reservoir
            
            Currently, this is a simple exponential relationship
            between depth and volume. Later, we need to perform
            interpolation on a lookup table (DataFrame)
        """
        
        self.water_level = 0.0104 * math.exp(0.059 * self.__quantity)
        
    def spillway_flow(self):
        """Calculate the spillway flow based on the weir equation
        
            For broad-crested weir:
            
            For sharp-crested weir:
            
            For ogee weir:
            
        """
        spill_flow = 0.0
        spillway_volume = 16.864 * math.log(self.__quantity) + 77.23
        
        if self.water_level > self.spillway_crest:
            h = self.water_level - self.spillway_crest
            v = self.__quantity - spillway_volume
            spill_flow = h * G / WATER_DENSITY #Broad crested weir (needs to be fixed!)
            spill_flow = min(spill_flow, v)
            
            self.__quantity -= spill_flow
            self.update_water_level()
        
        return spill_flow
    

