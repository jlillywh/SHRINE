from global_attributes.aegis import Aegis
from global_attributes.clock import Clock
from hydrology.watershed import Watershed
from hydrology.catchment import Catchment
from hydrology.wgen import Wgen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Simulator(Aegis):
    def __init__(self):
        Aegis.__init__(self)
        
        self.c = Clock()
        self.w = Watershed()
        self.w.link_catchment(Catchment('C1'), 'J1')
        self.w.link_catchment(Catchment('C3'), 'J1')
        self.w.add_junction('J5', 'J1')
        self.w.link_catchment(Catchment('C4'), 'J5')
        self.w.link_catchment(Catchment('C2'), 'J5')
        self.r = Wgen()
        self.ts = pd.Series(0, index=pd.date_range(self.c.start_date, periods=365, freq='D'))
    
    def run(self):
        while self.c.running:
            self.r.update(self.c.current_date)
            precip = self.r.rain * 25.4
            et = np.random.uniform()
            self.w.update(precip, et, self.w.sink_node)
            self.ts[self.c.current_date] = self.w.outflow
            
            self.c.advance()
        print("Simulation Complete!")
    
    def plot_ts(self):
        df = self.ts.to_frame()
        
        df.plot()
        
        plt.show()
