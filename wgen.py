import pandas as pd
import numpy as np
import math
from aegis import Aegis

class Wgen(Aegis):
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
                Station latitude in degrees
            rain_deterministic : float
                Used to override random numbers for verification purposes
                (default value < 0 enables random number)
                If deterministic is used, 0 <= value <= 1 must be true
                Deterministic value causes rain_gamma to use mean
            pww_array : list(float)
                Probability wet given wet
            pwd_array : list(float)
                Probability wet given dry
            alpha_array : list(float)
                Gamma distribution shape parameter
            beta_array : list(float)
                Gamma distribution scale parameter
            wet : bool
                wet/dry state for the current day (retains value from previous day)
            min_rain : float
                minimum rain threshold (in)
                daily rain below this threshold are thrown out
            rain : float
                daily rain amount (in)

            txmd : float
                Mean of Tmax (dry) aka "u", Fdeg
            txmw : float
                Mean of Tmax (wet) aka "u", Fdeg
            atx : float
                Amplitude of Tmax (wet or dry) aka "C", Fdeg
            cvtx : float
                Mean coefficient of variation of Tmax (wet or dry) aka "u"
            acvtx : float
                Amplitude of coefficient of variation of Tmax (wet or dry) aka "C"
            tn : float
                Mean of Tmin (wet or dry) aka "u", Fdeg
            atn : float
                Amplitude of Tmin (wet or dry) aka "C", Fdeg
            cvtn : float
                Mean of coefficient of variation of Tmin (wet or dry) aka "u"
            acvtn : float
                Amplitude of coefficient of variation of Tmin (wet or dry) aka "C"
            dt_day : float
                Middle of the year when days start to cool down (typically middle of July for northern hemisphere)


            Methods
            -------
    	"""

    def __init__(self):
        Aegis.__init__(self)
        self.lat = 40.76
        self.rain_deterministic = -1.0
        self.markov_deterministic = -1.0

        self.pww_array = [0.4113, 0.4026, 0.4585, 0.4826,
                          0.4537, 0.4714, 0.4468, 0.3464,
                          0.4268, 0.4122, 0.3511, 0.4259]
        self.pwd_array = [0.1775, 0.2214, 0.2747, 0.3162,
                          0.2819, 0.2744, 0.2361, 0.2099,
                          0.2077, 0.1907, 0.1663, 0.2118]
        self.alpha_array = [0.6374, 0.7084, 0.6939, 0.7728,
                            0.7843, 0.6843, 0.7157, 0.6589,
                            0.6125, 0.5743, 0.7, 0.7571]
        self.beta_array = [0.3098, 0.3099, 0.3478, 0.4125,
                           0.5401, 0.5888, 0.5996, 0.5701,
                           0.8209, 0.7203, 0.3651, 0.2659]
        self.wet = False
        self.min_rain = 0.01
        self.rain = 0.0

        # Temperature inputs
        self.txmd = 65.703
        self.txmw = 63.655
        self.atx = 25.58
        self.cvtx = 0.188
        self.acvtx = -0.136

    def precipitation(self, date=pd.Timestamp('1/1/2019')):
        """Generate daily precipitation values from monthly data

            The precipitation component of WGEN is a first-order Markov chain-gamma model.
            With the first-order Markov chain model, the probability of rain on a given
            day is conditioned on the wet or dry status of the previous day. For this
            application, a distribution with a minimum number of parameters was needed to
            minimize the problem of defining the parameters for a large number of
            locations. Richardson (1982a) has shown the two-parameter gamma distribution
            to be significantly better for describing daily precipitation amounts than
            the simple one-parameter exponential distribution. In WGEN, the precipitation
            parameters are constant for a given month but are varied from month to month.

            Parameters
            ----------
            date : Timestamp
        """

        month = date.month - 1
        alpha = self.alpha_array[month]  # also known as the shape factor
        beta = self.beta_array[month]  # also known as the scale factor

        if self.rain_deterministic < 0.0:
            rain_gamma = np.random.gamma(alpha, beta)
        else:
            rain_gamma = alpha * beta       #mean = alpha * beta for gamma distribution

        # Rain correction factor
        # TODO: implemennt correction factors in precip as function of "pw"
        rain_correction = 1.0

        rain_raw = rain_gamma * rain_correction

        pww = self.pww_array[month]
        pwd = self.pwd_array[month]

        pw = pwd / (1.0 - pww + pwd)
        prob = (pww if self.wet else pwd)

        if self.markov_deterministic < 0.0:
            rn = np.random.uniform()
        else:
            rn = self.markov_deterministic

        # Determine wet or dry day using Markov Chain model
        if self.wet:
            if rn - pww <= 0.0:
                self.wet = True
            else:
                self.wet = False
        else:
            if rn - pwd <= 0.0:
                self.wet = True
            else:
                self.wet = False

        gen_rain = self.wet and rain_raw >= self.min_rain

        sim_rain = (rain_raw if gen_rain else 0.0)

        # TODO implement overwrite with observed rain
        use_observed_rain = False
        self.rain = (0.0 if use_observed_rain else sim_rain)
        return self.rain