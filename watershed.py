from aegis import Aegis
from catchment import Catchment
from junction import Junction

""" For now, we are just going to build a simple watershed that assumes
    a basic network configuration because we are not ready to tackle
    flow networks. This water assumes the following setup:
            C1          C2
             |           |
             \           /
              \         /
               \       /
                \     /
                 \   /
                  \ /
                  J1
                   |
      C3__         |
          \_______J2     

    Where C1, C2, and C3 are inflows that contribute outflow discharge 
    to the next downstream junction (J1 and J2). J2 is the outflow from
    the watershed.             
              
"""
class Watershed(Aegis):

    def __init__(self):
        Aegis.__init__(self)
        self.outflow = 0.0

        self.c1 = Catchment("C1", 12.6)
        self.c2 = Catchment("C2", 34.2)
        self.c3 = Catchment("C3", 22.0)
        self.j1 = Junction("J1")
        self.j1.add_inflow(self.c1)
        self.j1.add_inflow(self.c2)
        self.j2 = Junction("J2")
        self.j2.add_inflow(self.c3)
        self.j2.add_inflow(self.j1)
        self.catchments = [self.c1, self.c2, self.c3]

    def update(self, precip, et):
        total_runoff = 0.0
        for i in self.catchments:
            i.update_runoff(precip, et)

        #self.j1.outflow
        self.outflow = self.j2.outflow

    def outflow(self):
        return self.j2.outflow
