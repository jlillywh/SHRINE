from water_manage.store import Store
from utils.attr_setter import AttrMap
import numpy as np


class Reservoir(Store):
    """Class for creating a reservoir object.
    
        Attributes
        ----------
        volume : float
            The quantity of water in the reservoir
            
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
        volume()
            Returns the quantity of the reservoir
            
        spillway_flow()
            Calculate the spillway flow based on the depth of
            water above the spillway crest
            
    
        
    """
    volume = AttrMap('quantity')
    
    def __init__(self, init_vol=100.0):
        Store.__init__(self, quantity=init_vol)
        self.elevations = [0.0, 10.0, 20.0]
        self.areas = [0.0, 35.0, 48.0]
        self.volumes = [0.0, 176.0, 590.0]
        # TODO stage-storage as dataframe: self.geometry = pd.DataFrame([0.0,5.0,10.0], [0.0, 100.0, 120.0])
        self.spillway_crest = 10.0
        self.spillway_volume = np.interp(self.spillway_crest, self.elevations, self.volumes)
        self.spillway_type = 'broad'
        self.bottom = 0.0
        self.outlet_elevation = 3.75
        self.weir_coef = 3.2
        self.weir_length = 1.0

    def __repr__(self):
        return 'Reservoir(initial_volume=%s)' % (self.volume)

    @property
    def water_level(self):
        return np.interp(self.volume, self.volumes, self.elevations)

    @water_level.setter
    def water_level(self, new_water_level):
        #self._water_level = new_water_level
        self.quantity = np.interp(new_water_level, self.elevations, self.volumes)
        self.update(0, 0)
    
    def calc_overflow(self):
        """Calculate the spillway flow based on the weir equation
        
            For broad-crested weir:
            
            For sharp-crested weir:
            
            For ogee weir:
            
        """
        
        if self._water_level > self.spillway_crest:
            
            h = self._water_level - self.spillway_crest
            v = self.volume - self.spillway_volume
            # The Kindsvater-Carter: rectangular, sharp-crested weir (suppressed)
            # Ce * Le|ft| * He|ft|^(3/2) * 1 cfs
            # TODO change this to use base units
            Ce = self.weir_coef
            l = self.weir_length
            
            q = Ce * l * h**(3.0/2.0)
            q = min(q, v)
            
            # TODO put "q" in terms of display units before updating reservoir
            self.update(0.0, q)
            self.water_level = np.interp(self.volume,
                                         self.volumes, self.elevations)
