import pandas as pd
from matplotlib import style
style.use('ggplot')
from global_attributes.aegis import Aegis



class Bowl(Aegis):
    """Class to create bowl objects used to represent the elevation-area-volume relationship for a reservoir.
    
        Attributes
        ----------
        elevation_units : Quantity Length unit
        area_units : Quantity Area unit
        volume_units : Quantity Volume unit
        
        elevations : list of flt
        areas : list of flt
        
        geometry : dataframe of elevations, area, and volume increments
        Methods
        -------
        plot_elevation_area() : show a plot of elevation-area
            show areas on x axis and elevations on y
        
    """
    def __init__(self, elevations, areas, unit='ft'):
        Aegis.__init__(self, unit=unit)
        self.elevations_name = 'Elevation'
        self.elevations = self.to_base_value(elevations)
        
        self.areas_name = 'Area'
        self.areas = self.to_base_value(areas, 2)
        
        self.volumes_name = 'Volume'
        self.volumes = [0.0] * len(self.elevations)
        
        volume = 0.0
        for i in range(len(self.elevations)):
            if i == 0:
                self.volumes[i] = 0.0
            else:
                elev_diff = self.elevations[i] - self.elevations[i-1]
                volume += elev_diff * (self.areas[i] + self.areas[i-1]) / 2.0
                self.volumes[i] = volume

        self.geometry = pd.DataFrame(list(zip(
            self.elevations,
            self.areas,
            self.volumes,
            )),
            columns=[self.elevations_name, self.areas_name, self.volumes_name])


    def plot_elevation_volume(self):
        #plt.figure()

        ax = self.geometry[['Area', 'Volume']].plot(secondary_y=['Volume'])
        ax.set_ylabel('Area [' + str(self.unit**2) + ']')
        ax.right_ax.set_ylabel('Volume')
        # set xticks to elev
        ax.set_xticks(self.geometry['Elevation'])
    
        #plt.show()
        