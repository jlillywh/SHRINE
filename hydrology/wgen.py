import pandas as pd
import numpy as np
import math
from global_attributes.aegis import Aegis

class Wgen(Aegis):
    """A class to create an object that generates weather data.

            WGEN is a stochastic weather generator originally developed
            in the 1980s in Fortran at the US Department of Agriculture
            Agricultural Research Service (Richardson and Wright 1984).
            The model can be used to generate daily depths of precipitation,
            maximum calc_temperature, minimum calc_temperature, and solar radiation.
            Precipitation is a first-order Markov chain-gamma model, where
            the probability of rain on a given day is conditioned on the
            wet or dry status of the previous day. The procedure for
            generating daily depths of tmax, tmin, and radiation is based
            on the weakly stationary generating process using a one-term
            Fourier series to model the seasonal variation in both
            calc_temperature and solar radiation. WGEN requires long time series
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
            rain_deterministic : bool, default False
                Used to override random numbers for verification purposes
                A true value will enable the deterministic override and
                False will allow random numbers to be generated (default)
                A deterministic value of 0.25 is used when set to true.
            markov_deterministic : bool default False
                Used to override the random state of wet vs. dry.
                A deterministic value of 0.177 is used when set to true
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
            rain_today : bool
                True if raining today; false otherwise

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
            x : Array[float]
                Coefficients used in Fourier smoothing for temperature.
                These are state variables remembered from one time step to the next.
            tmin : float
                daily min calc_temperature
            tmax : float
                daily max calc_temperature
            temp_determ : bool, default False
                If True, calculate temperature with determined Fourier coefficients
                instead of relying on random numbers, which is the default. This
                option is used for verification so that you can predict the outputs.
                If this variable is set to true, then the rain variables must also
                be deterministic. A markov_deterministic = 0.177 and
                rain_deterministic = 0.25 are used.

            Methods
            -------
            precipitation(date)
            calc_temperature(date)
            tavg
    	"""

    def __init__(self):
        Aegis.__init__(self)
        self.lat = 40.76

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
        self.rain_today = (False if self.rain < self.min_rain else True)
        self.rain_deterministic = False
        self.markov_deterministic = False

        # Temperature inputs
        self.txmd = 65.703
        self.txmw = 63.655
        self.atx = 25.58
        self.cvtx = 0.188
        self.acvtx = -0.136
        self.tn = 44.521
        self.atn = 23.387
        self.cvtn = 0.262
        self.acvtn = -0.222
        self.dt_day = 200

        self.temp_determ = False
        self.x = [0] * 3

        self.tmin = 0.0
        self.tmax = 0.0

    def update(self, date=pd.Timestamp('1/1/2019')):
        self.precipitation(date)
        self.calc_temperature(date)

    def precipitation(self, date=pd.Timestamp('1/1/2019')):
        """Generate daily precipitation depths from monthly data

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

            Returns
            -------
            none
        """

        month = date.month - 1
        alpha = self.alpha_array[month]  # also known as the shape factor
        beta = self.beta_array[month]  # also known as the scale factor

        if self.rain_deterministic:
            rain_gamma = 0.25
        else:
            rain_gamma = np.random.gamma(alpha, beta)

        # Rain correction factor
        # TODO: implemennt correction factors in precip as function of "pw"
        rain_correction = 1.0

        rain_raw = rain_gamma * rain_correction

        pww = self.pww_array[month]
        pwd = self.pwd_array[month]

        pw = pwd / (1.0 - pww + pwd)
        prob = (pww if self.wet else pwd)

        if self.markov_deterministic:
            rn = 0.177
        else:
            rn = np.random.uniform()

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
        self.rain_today = (False if self.rain < self.min_rain else True)

    def calc_temperature(self, date=pd.Timestamp('1/1/2019')):
        """Estimate calc_temperature based on time of year, wet day, and location
            The procedure that is used in WGEN for generating daily depths
            of tmax and tmin is based on the weakly stationary generating
            process given by Matalas (1967). A one-term Fourier series is
            used to model the seasonal variation in both calc_temperature and
            solar radiation. The coefficients of the Fourier term were
            determined throughout the locations tested and it was found that
            some of the coefficients were strongly location dependent
            (Richardson and Wright, 1984), thus limiting the application of
            this model to areas where these coefficients are available.

            Parameters
            ----------
                date = Timestamp
        """

        dayofyear = date.dayofyear
        """Calculate a one harmonic series"""
        self.x = self.harmonic()

        """Calculate calc_temperature factors tns and tnm"""
        d1 = self.txmd - self.txmw
        dt = math.cos(0.0172 * (dayofyear - self.dt_day))
        txm = self.txmd + self.atx * dt
        xcr1 = 0.06
        if self.cvtx + self.acvtx * dt >= 0.0:
            xcr1 = self.cvtx + self.acvtx * dt

        txs = txm * xcr1
        txm1 = txm - d1
        txs1 = txm1 * xcr1
        txxs = txs
        txxm = txm
        if self.rain_today:
            txxs = txs1
            txxm = txm1

        tnm = self.tn + self.atn * dt
        xcr2 = 0.06
        if self.cvtn + self.acvtn * dt >= 0.0:
            xcr2 = self.cvtn + self.acvtn * dt

        tns = tnm * xcr2

        """Generate calc_temperature min/max depths"""
        tmax1 = self.x[0] * txxs + txxm
        tmin1 = self.x[1] * tns + tnm

        """TODO add calc_temperature correlation factors"""
        cf_max = 0.0  # Max Temperature correlation factor
        cf_min = 0.0  # Min Temperature correlation factor
        self.tmax = max(tmax1, tmin1) + cf_max
        self.tmin = min(tmax1, tmin1) + cf_min

    @property
    def tavg(self):
        return (self.tmax + self.tmin) / 2.0

    def fourier(self):
        """Fourier routine"""
        deterministic = self.temp_determ
        v = 0.0
        e = np.zeros(3)
        rn1_determ = [0.25, 0.5, 0.75]
        rn2_determ = [0.75, 0.5, 0.25]
        for i in range(0, 3):
            j = 0
            out_bounds = True
            while out_bounds:
                rn1 = (rn1_determ[i] if deterministic else np.random.uniform())
                rn2 = (rn2_determ[i] if deterministic else np.random.uniform())
                v = min(math.sqrt(-2.0 * math.log(rn1)) * math.cos(6.283185 * rn2), 2.6)
                out_bounds = abs(v) > 2.5 and j < 100
                j += 1
            e[i] += v
        return e
        
    def harmonic(self):
        """Calculate a one harmonic series"""
        e = self.fourier()
        if self.temp_determ:
            self.x = [-0.3513, -1.754, 0.6244]
        else:
            self.x = [0] * 3
        x = self.x
        a = np.array([[0.567, 0.086, -0.002],
                      [0.253, 0.504, -0.05],
                      [-0.006, -0.039, 0.244]])
    
        b = np.array([[0.781, 0.000, 0.000],
                      [0.328, 0.637, 0.00],
                      [0.238, -0.341, 0.873]])
    
        r = np.zeros(3)
        rr = np.zeros(3)
    
        for i in range(0, 3):
            for j in range(0, 3):
                r[i] += b[i, j] * e[j]
                rr[i] += a[i, j] * x[j]
        return r + rr