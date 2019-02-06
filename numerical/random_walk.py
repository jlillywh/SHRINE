import numpy as np

class RandomWalk:
    def __init__(self, init_position=2.0):
        """Generates a random walk through time.
            
            The "walk" is the cumulative result of random steps
    
            Attributes
            ----------
            position : float
                The current point of the walk
            allow_negative : bool
                True if negative depths are allowed; false otherwise
        """
        
        self.position = init_position
        self.allow_negative = False
        
    def update(self):
        """Perform the walk by advancing 1 step.
        
        """
        rn = np.random.normal(0.0, 0.05)
        if self.position + rn < 0.0:
            self.position = 0.0
        else:
            self.position += rn
        
from clock import Clock
import pandas as pd
import matplotlib.pyplot as plt
c = Clock()
r = RandomWalk()
ts = pd.Series(0.0, index=pd.date_range(c.start_date, periods=365, freq='D'))

while c.running:
    r.update()
    ts[c.current_date] = r.position
    c.advance()

df = ts.to_frame()
df.plot()
plt.show()
