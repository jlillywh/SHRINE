import math
# This is the Sacramento Soil Moisture Accounting Model implemented in Python


class Sacramento:
    # Class constants
    DT = 1.0        # Length of time interval in days
    IFRZE = False       # Flag to incorporate frost calculations. True = use calculations
    
    def __init__(self, init_state, params, globals):
        # Initial values of state variables
        self.uztwc = init_state['uztwc']    # Upper zone tension water storage
        self.uzfwc = init_state['uzfwc']    # Upper zone free water storage
        self.lztwc = init_state['lztwc']    # Lower zone tension water storage
        self.lzfsc = init_state['lzfsc']    # Lower zone supplementary free water storage
        self.lzfpc = init_state['lzfpc']    # Upper zone primary free water storage
        self.adimc = init_state['adimc']    # Additional impervious area storage
        self.fgix = 0.0                     # Initial value of the frost index, units of Cdeg

        # Params yet to be incorporated:
        self.sasc_input_option = True      # Option to use the SASC time series
        self.runoff_component_interval = 24
        #   Runoff component time series (ROCL) interval. Must be multiple of the input RAIM time series interval
        self.smzc_interval = 24
        #   Soil moisture storages time series (SMZC) interval. Must be multiple of the input RAIM time
        #   series interval
        self.mape_input = False         # Option to use the MAPE time series
        self.frozen_ground_calc_option = False
        self.et_demand_curve = [0.65, 0.65, 0.67, 0.73, 0.89, 1.05, 1.09, 1.04, 0.9, 0.78, 0.73, 0.7]
        """ ET-demand or PE-adjustment factor (the table contains 12 values). If PE data used
        (i.e. MAPE_INPUT is “Yes”), then values are PEadjustments; if PE data not used, then values
        represent ET-demand. Both 16th of each month (Jan. through Dec.; units of MM/day); daily
        values are computed by linear interpolation."""
        self.pxadj = 1.0                # Precipitation adjustment factor
        self.peadj = 1.0                # ET-demand adjustment factor
        self.efc = 0.0                  # Effective forest cover
        
        # Model parameters
        self.uztwm = params['uztwm']  # Upper zone tension water capacity [mm]
        self.uzfwm = params['uzfwm']  # Upper zone free water capacity [mm]
        self.lztwm = params['lztwm']
        self.lzfpm = params['lzfpm']  # Lower zone primary free water capacity [mm]
        self.lzfsm = params['lzfsm']  # Lower zone supplementary free water capacity [mm]
        self.uzk = params['uzk']  # Upper zone free water lateral depletion coefficient [1/day]
        self.lzpk = params['lzpk']  # Lower zone primary free water depletion rate [1/day]
        self.lzsk = params['lzsk']  # Lower zone supplementary free water depletion rate [1/day]
        self.zperc = params['zperc']  # Percolation demand scale parameter [-]
        self.rexp = params['rexp']  # Percolation demand shape parameter [-]
        self.pfree = params['pfree']  # Percolating water split parameter (decimal fraction)
        self.pctim = params['pctim']  # Impervious fraction of the watershed area (decimal fraction)
        self.adimp = params['adimp']  # Additional impervious areas (decimal fraction)
        self.riva = params['riva']  # Riparian vegetation area (decimal fraction)
        self.side = params['side']  # The ratio of deep recharge to channel base flow [-]
        self.rserv = params['rserv']  # Fraction of lower zone free water not transferrable (decimal fraction)

        self.pxv = globals['pxv']  # Precip for the time interval
        self.lwe = globals['lwe']
        self.we = globals['we']
        self.isc = globals['isc']
        self.aesc = globals['aesc']

        self.roimp = 0.0
        self.lzdefr = 0.0
        self.fr = 0.0
        self.fi = 0.0

        self.sif = 0.0
        self.sperc = 0.0
        self.spbf = 0.0
        self.sett = 0.0
        self.se1 = 0.0
        self.se3 = 0.0
        self.se4 = 0.0
        self.se5 = 0.0
        self.tci = 0.0
        
        self.bf = 0.0                   # baseflow

    def update(self, p, et):
        # Carryover state variables and update runoff amounts
        self.evapotrans(et)
        return None
    
    def evapotrans(self, ep):
        """Compute evapotranspiration loss for the time interval."""
        # epdist = list(range(0, 24))
        # edmnd is the et-demand for the time interval
        edmnd = ep      # * epdist[self.kint] --this was removed for constant ep over the day
        
        # Compute ET from the upper zone
        e1 = edmnd * (self.uztwc / self.uztwm)
        
        # Residual evaporation demand
        red = edmnd - e1
        
        self.uztwc -= e1
        
        if self.uztwc < 0.0:
            e1 += self.uztwc
            self.uztwc = 0.0
            red = edmnd - e1
            
        if self.uzfwc < red:
            e2 = self.uzfwc
            self.uzfwc = 0.0
            red -= e2
        else:
            e2 = red
            self.uzfwc -= e2
            red = 0.0

            if (self.uztwc / self.uztwm) < (self.uzfwc / self.uzfwm):
                uzrat = (self.uztwc + self.uzfwc) / (self.uztwm + self.uzfwm)
                self.uztwc = self.uztwm * uzrat
                self.uzfwc = self.uzfwm * uzrat
        
        if self.uztwc < 0.00001:
            self.uztwc = 0.0
        if self.uzfwc < 0.00001:
            self.uzfwc = 0.0
            
        # Compute ET from lower zone
        e3 = red * (self.lztwc / (self.uztwm + self.lztwm))
        self.lztwc -= e3
        if self.lztwc < 0.0:
            e3 += self.lztwc
            self.lztwc = 0.0
        ratlzt = self.lztwc / self.lztwm
        ratlz = (self.lztwc + self.lzfpc + self.lzfsc) / (self.lztwm + self.lzfpm + self.lzfsm)
        if ratlzt < ratlz:
            delivery = (ratlz - ratlzt) * self.lztwm
            self.lztwc += delivery
            self.lzfsc -= delivery
            if self.lzfsc < 0.0:
                self.lzfpc += self.lzfsc
                self.lzfsc = 0.0
        if self.lztwc < 0.00001:
            self.lztwc = 0.0
            
        e5 = e1 + (red + e2) * ((self.adimc - e1 - self.uztwc) / (self.uztwm + self.lztwm))
        self.adimc -= e5
        if self.adimc < 0.0:
            e5 += self.adimc
            self.adimc = 0.0
        e5 *= self.adimp
        
        # Compute percolation and runoff amounts
        twx = self.pxv + self.uztwc - self.uztwm
        if twx < 0.0:
            self.uztwc += self.pxv
            twx = 0.0
        else:
            self.uztwc = self.uztwm
        self.adimc += self.pxv - twx
        
        # Compute impervious area runoff
        self.roimp = self.pxv * self.pctim
        self.runoff(twx)

        # compute sums and adjust runoff amounts by the area over which they are generated.
        eused = e1 + e2 + e3
        # eused is the et from parea which is 1.0-adimp-pctim
        parea = 1.0 - self.adimp - self.pctim
        self.sif *= parea
        # Separate channel component of baseflow from the non-channel component
        tbf = bf * parea
        # tbf is total baseflow
        bfcc = tbf * (1.0 / (1.0 + self.side))
        # bfcc is baseflow, channel component
        bfp = self.spbf * parea / (1.0 + self.side)
        bfs = bfcc - bfp
        bfs = max(bfs, 0.0)
        bfncc = tbf - bfcc
        # bfncc is baseflow,non-channel component

        # compute total channel inflow for the time interval.
        self.tci = self.roimp + self.addro + self.ssur + self.sif + bfcc

        # compute e4-et from riparian vegetation.
        e4 = (edmnd - eused) * self.riva

        # subtract e4 from channel inflow
        self.tci -= e4
        if self.tci < 0.0:
            e4 += self.tci
            self.tci = 0.0

        # compute total evapotranspiration - tet
        eused = eused * parea
        tet = eused + e5 + e4
        self.sett += tet
        self.se1 += e1 * parea
        self.se3 += e3 * parea
        self.se4 += e4
        self.se5 += e5
        # check that adimc >= uztwc
        self.adimc = max(self.uztwc, self.adimc)
    
    def runoff(self, twx):
        
        # Initialize time interval sums
        self.sif = 0.0
        self.sperc = 0.0
        self.spbf = 0.0
        
        # Determine computational time increment for the basic time interval
        ninc = 1.0 + 0.2 * (self.uzfwc + twx)
        # ninc = number of time increments that the time interval is divided into for further
        # soil-moisture accounting. No one increment will exceed 5.0 millimeters of uzfwc+pav
        dinc = (1.0 / ninc) * self.DT
        # dinc = length of each increment in days
        pinc = twx / ninc
        # pinc = Amount of available moisture for each increment. Compute free water depletion
        # fractions for the time increment being used-basic depletions are for one day
        duz = 1.0 - ((1.0 - self.uzk)**dinc)
        dlzp = 1.0 - ((1.0 - self.lzpk)**dinc)
        dlzs = 1.0 - ((1.0 - self.lzsk)**dinc)
        
        # Start incremental do loop for the time interval.
        for i in range(int(ninc)):
            adsur = 0.0
            # Compute direct runoff (from adimp area)
            ratio = (self.adimc - self.uztwc) / self.lztwm
            if ratio < 0.0:
                ratio = 0.0
            addro = pinc * ratio**2
            # addro is the amount of direct runoff from the area adimp
            
        bf = self.baseflow(dlzp, dlzs)

    def baseflow(self, dlzp, dlzs):
        # Compute baseflow
        bf = self.lzfpc * dlzp
        self.lzfpc -= bf
        if self.lzfpc <= 0.0001:
            bf += self.lzfpc
            self.lzfpc = 0.0

        self.spbf += bf
        bf = self.lzfsc * dlzs
        self.lzfsc -= bf
        if self.lzfsc <= 0.0001:
            bf += self.lzfsc
            self.lzfsc = 0.0
        return bf
        
        # Compute percolation-if no water available then skip
        if pinc + self.uzfwc <= 0.01:
            self.uzfwc += pinc
        else:
            self.percolation(dlzp, dlzs, duz, pinc, addro, adsur)

        # Distribute pinc between uzfwc and surface runoff.
        if pinc != 0.0:
            # Check if pinc exceeds uzfwm
            if (pinc + self.uzfwc) <= self.uzfwm:
                # No surface runoff
                self.uzfwc = self.uzfwc + pinc
            else:
                #
                #     compute surface runoff (sur) and keep track of time interval sum.
                sur = pinc + self.uzfwc - self.uzfwm
                self.uzfwc = self.uzfwm
                # self.ssur += sur * self.parea -- I removed cumulative since time step is always 1 day
                adsur = sur * (
                            1.0 - addro / pinc)  # adsur is the amount of surface runoff which comes from that portion of adimp which is not  # currently generating direct runoff.  addro/pinc is the fraction of adimp currently generating  # direct runoff.  # self.ssur += adsur * self.adimp -- I removed cumulative since time step is always 1 day  # adimp area water balance -- sdro is the 6 hr sum of direct runoff.

        self.adimc = self.adimc + pinc - addro - adsur
        if self.adimc > self.uztwm + self.lztwm:
            addro = addro + self.adimc - (self.uztwm + self.lztwm)
            self.adimc = self.uztwm + self.lztwm
        self.sdro += addro * self.adimp
        if self.adimc < 0.00001:
            self.adimc = 0.0

        # compute new frost index and moisture transfer.
        if self.IFRZE:
            self.frost1(self.pxv, sur, addro, self.lwe, self.we, self.isc, self.aesc)
            
    def percolation(self, dlzp, dlzs, duz, pinc, addro, adsur):
        percm = self.lzfpm * dlzp + self.lzfsm * dlzs
        perc = percm * (self.uzfwc / self.uzfwm)
        defr = 1.0 - ((self.lztwc + self.lzfpc + self.lzfsc) / (self.lztwm + self.lzfpm + self.lzfsm))
        #     defr is the lower zone moisture deficiency ratio
        self.fr = 1.0
        #     fr is the change in percolation withdrawal due to frozen ground.
        self.fi = 1.0
        #     fi is the change in interflow withdrawal due to frozen ground.
        if self.IFRZE:
            uzdefr = 1.0 - ((self.uztwc + self.uzfwc) / (self.uztwm + self.uzfwm))
            self.fgfr1()
        
        perc = perc * (1.0 + self.zperc * (defr ** self.rexp)) * self.fr
        #     note...percolation occurs from uzfwc before pav is added.
        if perc >= self.uzfwc:
            # Percolation rate exceeds uzfwc.
            perc = self.uzfwc
        # Percolation rate is less than uzfwc.
        self.uzfwc = self.uzfwc - perc
        #     check to see if percolation exceeds lower zone deficiency.
        check = self.lztwc + self.lzfpc + self.lzfsc + perc - self.lztwm - self.lzfpm - self.lzfsm
        if check > 0.0:
            perc = perc - check
            self.uzfwc += check

        self.sperc += perc
        #     sperc is the time interval summation of perc
        #
        #     compute interflow and keep track of time interval sum.
        #     note...pinc has not yet been added
        delivery = self.uzfwc * duz * self.fi
        self.sif += delivery
        self.uzfwc = self.uzfwc - delivery
        # Distribute percolated water into the lower zones
        # Tension water must be filled first except for the pfree area.
        # perct is percolation to tension water and percf is percolation going to free water.
        perct = perc * (1.0 - self.pfree)
        if (perct + self.lztwc) <= self.lztwm:
            self.lztwc = self.lztwc + perct
            percf = 0.0
        else:
            percf = perct + self.lztwc - self.lztwm
            self.lztwc = self.lztwm
        #
        #      distribute percolation in excess of tension
        #      requirements among the free water storages.
        percf = percf + perc * self.pfree
        if percf != 0.0:
            hpl = self.lzfpm / (self.lzfpm + self.lzfsm)
            #     hpl is the relative size of the primary storage
            #     as compared with total lower zone free water storage.
            ratlp = self.lzfpc / self.lzfpm
            ratls = self.lzfsc / self.lzfsm
            #     ratlp and ratls are content to capacity ratios, or
            #     in other words, the relative fullness of each storage
            fracp = (hpl * 2.0 * (1.0 - ratlp)) / ((1.0 - ratlp) + (1.0 - ratls))
            #     fracp is the fraction going to primary.
            fracp = min(fracp, 1.0)
            percp = percf * fracp
            percs = percf - percp
            # percp and percs are the amount of the excess percolation going to primary
            # and supplemental storges, respectively.
            self.lzfsc += percs
            if self.lzfsc > self.lzfsm:
                percs = percs - self.lzfsc + self.lzfsm
                self.lzfsc = self.lzfsm
            self.lzfpc = self.lzfpc + (percf - percs)
            # Check to make sure lzfpc does not exceed lzfpm.
            if self.lzfpc > self.lzfpm:
                excess = self.lzfpc - self.lzfpm
                self.lztwc = self.lztwc + excess
                self.lzfpc = self.lzfpm
            
        
    
    def fgfr1(self):
        # Compute the change in the percolation and interflow withdrawal rates due to frozen ground.
        # The following vars are references to items from an array that I still need to find.
        findx = 1
        frtemp = 1.0
        satr = 1.0
        frexp = 1.0

        #     determine if frozen ground effect exists.
        if findx < frtemp:
            # Compute saturated reduction.
            exp = frtemp - findx
            fsat = (1.0 - satr)**exp
            # Change at dry conditions
            fdry = 1.0
            # Compute actual change
            if self.lzdefr <= 0.0:
                self.fr = fsat
                self.fi = self.fr
            else:
                self.fr = fsat + (fdry - fsat) * self.lzdefr**frexp
                self.fi = self.fr

    def frost1(self, pxv, sur, addro, isc, aesc):
        # Compute the change in the frozen ground index and moisture movement due to temperature gradients.        #
        # The following vars are references to items from an array that I still need to find.
        ta = 1.0
        lwe = 1.0
        we = 1.0
        findx = 1.0
        # findx1 = findx
        csoil = 4.0 * self.DT * 1.0
        csnow = 1.0
        ghc = 1.0 * self.DT
        rthaw = 1.0
        #
        # Compute moisture movement (equations not ready yet)
        #
        # Compute change in frozen ground index due to water frezing in the soil.
        if findx < 0.0:  # go to 120
            water = pxv - sur - addro
            if water > 0.0:  # go to 120
                findx += rthaw * water
            findx = max(findx, 0.0)
        
        # change due to temperature.
        if (findx < 0.0) or (ta < 0.0):
            # Compute transfer coefficient.
            if lwe == 0.0 or we == 0.0:
                c = csoil
            else:
                cover = 1.0
                twe = we / cover
                c = csoil * (1.0 - cover) + csoil * ((1.0 - csnow) ** twe) * cover
            if isc > 0:
                cover = aesc
            else:
                cover = 1.0
                twe = we / cover
                c = csoil * (1.0 - cover) + csoil * ((1.0 - csnow) ** twe) * cover
            if cover == 0.0:
                c = csoil

            # compute change in frost index.
            if ta < 0.0:  # go to 126
                cfi = -c * math.sqrt(ta * ta + findx * findx) - c * findx + ghc
                findx = findx + cfi
            # go to 190
            else:
                findx = findx + c * ta + ghc
        
        return max(findx, 0.0)
