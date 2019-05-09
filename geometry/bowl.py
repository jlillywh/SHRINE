import pandas as pd
from matplotlib import style
style.use('ggplot')



class Bowl:
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
    def __init__(self, elevations, areas, base_unit='ft'):
        self.base_unit = base_unit
        self.elevations_name = 'Elevation'
        self.elevations = elevations
        
        self.areas_name = 'Area'
        self.areas = areas
        
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
        ax.set_ylabel('Area [' + self.base_unit + '2]')
        ax.right_ax.set_ylabel('Volume [' + self.base_unit + '3]')
        # set xticks to elev
        ax.set_xticks(self.geometry['Elevation'])
    
        #plt.show()
        