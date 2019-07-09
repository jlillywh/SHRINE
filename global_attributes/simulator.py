from global_attributes.aegis import Aegis
from global_attributes.clock import Clock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Simulator(Aegis):
    """Class for creating a new simulation.
    
        Attributes
        ----------
        time_basis : str
            Select between static, elapsed time, or calendar time basis for the simulation
            
    """
    def __init__(self, time_basis='elapsed time', duration=100, time_step='1 days'):
        Aegis.__init__(self)
        self.time_basis = time_basis
        self.c = Clock()
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
