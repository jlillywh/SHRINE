from numerical.random_walk import RandomWalk
from global_attributes.constants import WATER_DENSITY
import numpy as np
from global_attributes.constants import U

class Slurry:
    def __init__(self):
        """Estimate the water and solid demand components of
            slurry demand.
            
            This is often used for mining applications where
            the mine produces a slurry from the mining process
            and flows into a tailings facility. At this point,
            the solids in the demand settle into the pond and
            cleaner water comes to the top.
            
            Attributes
            ----------
            avg_feed_moisture : float
                Average moisture content of mine feed as a fraction
                Feed moisture does a random walk moving forward
                
            avg_feed_rate : float
                Feed from the mine in (metric tons / day)
                
            avg_product_rate : float
                Rate at which product is produced (tonne/day)
                
            avg_product_moisture : float
                Moisture content of product as a fraction
                
            solids_density : float
                Slurry density (percent solids by weight)
                
            dep_solids_density : float
                Density of deposited solids (assumed constant - no consolidation)
                in units of tonne / m3
            solids_sg : float
                Average specific gravity of solids (unitless)
            
        """
        
        self.avg_feed_moisture = 0.02
        self.feed_moisture = RandomWalk(self.avg_feed_moisture)
        self.avg_feed_rate = 5000.0 * U.tonne / U.day
        self.avg_product_rate = 10.0 * U.tonne / U.day
        self.avg_product_moisture = 0.08
        self.solids_density = 0.55
        self.dep_solids_density = 1.6 * U.tonne / U.m**3
        self.solids_sg = 2.8
        
    def update(self):
        """Calculate the demand of slurry along with its consituents.
        """
        
        self.feed_moisture.update()
        feed_rate = np.random.normal(self.avg_feed_rate, self.avg_feed_rate/10.0)
        product_rate = np.random.normal(self.avg_product_rate, self.avg_product_rate/10.0)
        product_moisture = np.random.triangular(7.5, self.avg_product_moisture, 15.0)
        
        # Rate at which solids are being added via the feed
        solid_feed_rate = feed_rate * (1.0 - self.feed_moisture)
        # Rate at which solids are leaving via product
        solid_product_rate = product_rate * (1.0 - product_moisture)
        
        # Mass inflow of solids in the slurry
        solids_flow = solid_feed_rate - solid_product_rate
        
        # Rate at which slurry water is required
        water_in_slurry = solids_flow * (1.0 - self.solids_density) / WATER_DENSITY
        
        # Current void ratio of the deposited tailings
        void_ratio = self.solids_sg * WATER_DENSITY / self.dep_solids_density - 1.0
        
        # Volume of entrained water per unit mass of solids
        entrained_water_unit = (void_ratio / self.solids_sg) / WATER_DENSITY
        
        # Water that stays with the deposited solids (leaves the water pool)
        entrained_water = entrained_water_unit * solids_flow
        
        # Solids flowing in on a volumetric basis
        solids_volume_flow = solids_flow / self.dep_solids_density
        