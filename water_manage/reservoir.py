from water_manage.store import Store
import numpy as np
import math
from inputs.constants import WATER_DENSITY, G
from inputs.constants import U


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
            
        _water_level : float
            Elevation of the water surface
        
        Methods
        -------
        spillway_flow()
            Calculate the spillway flow based on the depth of
            water above the spillway crest
            
    
        
    """
    def __init__(self):
        Store.__init__(self)
        self.elevations = [0.0,5.0,20.0] * U.m
        self.volumes = [0.0, 10000.0, 520000.0] * U.m**3
        #self.geometry = pd.DataFrame([0.0,5.0,10.0], [0.0, 100.0, 120.0])
        self.spillway_crest = 10.0 * U.m
        self.spillway_volume = np.interp(self.spillway_crest, self.elevations, self.volumes) * self._quantity_units
        self.spillway_type = 'broad'
        self.bottom = 0.0 * U.m
        self._water_level = 0.0 * U.m
        self.outlet_elevation = 3.75 * U.m
        self.weir_coef = 3.2
        self.weir_length = 1.0 * U.m

    @property
    def water_level(self):
        return self._water_level

    @water_level.setter
    def water_level(self, new_water_level):
        self._water_level = new_water_level
        self._quantity = np.interp(self._water_level, self.elevations, self.volumes) * U.m**3
        self.update(0 * self._rate_units, 0 * self._rate_units)
    
    def calc_overflow(self):
        """Calculate the spillway flow based on the weir equation
        
            For broad-crested weir:
            
            For sharp-crested weir:
            
            For ogee weir:
            
        """
        
        if self._water_level > self.spillway_crest:
            
            h = self._water_level - self.spillway_crest
            v = self._quantity - self.spillway_volume
            # The Kindsvater-Carter: rectangular, sharp-crested weir (suppressed)
            # Ce * Le|ft| * He|ft|^(3/2) * 1 cfs
            Ce = 3.28
            l = self.weir_length.to(U.ft).magnitude
            h = h.to(U.ft).magnitude
    
            self.overflow = (self.weir_coef * l * h**(3.0/2.0) *
                             U.cfs).to(U.m3/U.day)
            self.overflow = min(self.overflow, v/U.day)
    
            self._quantity -= self.overflow * U.day
            self.water_level = np.interp(self._quantity,
                                         self.volumes, self.elevations) * U.m


