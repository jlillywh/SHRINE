
class Wgen:
    """A class to create an object that generates weather data.

        WGEN is a stochastic weather generator originally developed
        in the 1980s in Fortran at the US Department of Agriculture
        Agricultural Research Service (Richardson and Wright 1984).
        The model can be used to generate daily values of precipitation,
        maximum temperature, minimum temperature, and solar radiation.
        Precipitation is a first-order Markov chain-gamma model, where
        the probability of rain on a given day is conditioned on the
        wet or dry status of the previous day. The procedure for
        generating daily values of tmax, tmin, and radiation is based
        on the weakly stationary generating process using a one-term
        Fourier series to model the seasonal variation in both
        temperature and solar radiation. WGEN requires long time series
        of daily weather data to estimate parameters, limiting its use
        to regions of the world where sufficient data are available.

        Data is entered through the dashboard interface. Prepare the data
        using WGEN PAR found in our GoldSim library. Run the model
        as-is and view the "WGEN_Validation" to see how the results
        compare against those presented in the WGEN documentation.

        Attributes
        ----------
        lat : float

        Methods
        -------
"""

    def __int__(self):
        self.lat = 40.76
        #Rainfall inputs
        #   Probability wet given wet
        self.pww = [0.4113, 0.4026, 0.4585, 0.4826,
                    0.4537, 0.4714, 0.4468, 0.3464,
                    0.4268, 0.4122, 0.3511, 0.4259]
        #   Probability wet given dry
        self.pwd = [0.1775, 0.2214, 0.2747, 0.3162,
                    0.2819, 0.2744, 0.2361, 0.2099,
                    0.2077, 0.1907, 0.1663, 0.2118]
        #   Gamma distribution shape parameter
        self.alpha = [0.6374, 0.7084, 0.6939, 0.7728,
                      0.7843, 0.6843, 0.7157, 0.6589,
                      0.6125, 0.5743, 0.7, 0.7571]
        #   Gamma distribution scale parameter
        self.beta = [0.3098, 0.3099, 0.3478, 0.4125,
                     0.5401, 0.5888, 0.5996, 0.5701,
                     0.8209, 0.7203, 0.3651, 0.2659]

        #Temperature inputs
        #   Mean of Tmax (dry) aka "u", Fdeg
        self.txmd = 65.703
        #   Mean of Tmax (wet) aka "u", Fdeg
        self.txmw = 63.655
        self.atx = 25.58
        self.cvtx = 0.188
        self.acvtx = -0.136