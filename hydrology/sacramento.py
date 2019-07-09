# This is the Sacramento Soil Moisture Accounting Model implemented in Python


class Sacramento:
    def __init__(self, init_state, params, globals):
        # Initial values of state variables
        self.uztwc = init_state['uztwc']  # Upper zone tension water storage
        self.uzfwc = init_state['uzfwc']  # Upper zone free water storage
        self.lztwc = init_state['lztwc']  # Lower zone tension water storage
        self.lzfsc = init_state['lzfsc']  # Lower zone supplementary free water storage
        self.lzfpc = init_state['lzfpc']  # Upper zone primary free water storage
        self.adimc = init_state['adimc']  # Additional impervious area storage


        # Model parameters
        self.uztwm = params['uztwm']    # Upper zone tension water capacity [mm]
        self.uzfwm = params['uzfwm']    # Upper zone free water capacity [mm]
        self.lztwm = params['lztwm']     # Lower zone tension water capacity [mm]
        self.lzfpm = params['lzfpm']    # Lower zone primary free water capacity [mm]
        self.lzfsm = params['uzfsm']    # Lower zone supplementary free water capacity [mm]
        self.uzk = params['uzk']       # Upper zone free water lateral depletion rate [1/day]
        self.lzpk = params['lzpk']     # Lower zone primary free water depletion rate [1/day]
        self.lzsk = params['lzsk']     # Lower zone supplementary free water depletion rate [1/day]
        self.zperc = params['zperc']    # Percolation demand scale parameter [-]
        self.rexp = params['rexp']      # Percolation demand shape parameter [-]
        self.pfree = params['pfree']    # Percolating water split parameter (decimal fraction)
        self.pctim = params['pctim']    # Impervious fraction of the watershed area (decimal fraction)
        self.adimp = params['adimp']    # Additional impervious areas (decimal fraction)
        self.riva = params['riva']      # Riparian vegetation area (decimal fraction)
        self.side = params['side']      # The ratio of deep recharge to channel base flow [-]
        self.saved = params['saved']
        self.rserv = params['rserv']     # Fraction of lower zone free water not transferrable (decimal fraction)
        
        self.kint = globals['kint']
        self.pxv = globals['pxv']
        self.pcti = globals['pcti']
        self.simpvt = globals['simpvt']
        self.dt = globals['dt']
        self.ifrze = globals['ifrze']
        
        self.roimp = 0.0
        self.simpvt = 0.0
        self.lzdefr = 0.0
        self.fr = 0.0
        self.fi = 0.0

    def evapotrans(self):
        epdist = list(range(0, 24))
        ep = 1.0
        edmnd = ep * epdist[self.kint]
        
        # Compute ET from the upper zone
        e1 = edmnd * (self.uztwc / self.uztwm)
        
        # Residual evaporation demand
        red = edmnd - e1
        
        self.uztwc = self.uztwc - e1
        e2 = 0.0
        
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
        ratlz = (self.lztwc + self.lzfpc + self.lzfsc - self.saved) / (self.lztwm + self.lzfpm + self.lzfsm - self.saved)
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
        self.roimp = self.pxv * self.pcti
            
    def runoff(self):
        self.simpvt += self.roimp
        
        # Initialize time interval sums
        sbf = 0.0
        ssur = 0.0
        sif = 0.0
        sperc = 0.0
        sdro = 0.0
        spbf = 0.0
        
        # Determine computational time increment for the basic time interval
        ninc = 1.0 + 0.2 * (self.uzfwc + self.twx)
        # ninc = number of time increments that the time interval is divided into for further
        # soil-moisture accounting. No one increment will exceed 5.0 millimeters of uzfwc+pav
        dinc = (1.0 / ninc) * self.dt
        # dinc = length of each increment in days
        pinc = self.twx / ninc
        # pinc = Amount of available moisture for each increment. Compute free water depletion
        # fractions for the time increment being used-basic depletions are for one day
        duz = 1.0 - ((1.0 - self.uzk)**dinc)
        dlzp = 1.0 - ((1.0 - self.lzpk)**dinc)
        dlzs = 1.0 - ((1.0 - self.lzsk)**dinc)
        
        # Start incremental do loop for the time interval.
        for i in range(ninc):
            adsur = 0.0
            # Compute direct runoff (from adimp area)
            ratio = (self.adimc - self.uztwc) / self.lztwm
            if ratio < 0.0:
                ratio = 0.0
            addro = pinc * ratio**2
            # addro is the amount of direct runoff from the area adimp
            
            # Compute baseflow and keep track of time interval sum.
            bf = self.lzfpc * dlzp
            self.lzfpc -= bf
            if self.lzfpc <= 0.0001:
                bf += self.lzfpc
                self.lzfpc = 0.0
            sbf += bf
            spbf += bf
            bf = self.lzfsc * dlzs
            self.lzfsc -= bf
            if self.lzfsc <= 0.0001:
                bf += self.lzfsc
                self.lzfsc = 0.0
            sbf += bf
            
            # Compute percolation-if no water available then skip
            if pinc + self.uzfwc <= 0.01:
                self.uzfwc += pinc
                
    
    def percolation(self, dlzp, dlzs):
        percm = self.lzfpm * dlzp + self.lzfsm * dlzs
        perc = percm * (self.uzfwc / self.uzfwm)
        self.defr = 1.0 - ((self.lztwc + self.lzfpc + self.lzfsc) / (self.lztwm + self.lzfpm + self.lzfsm))
        #     defr is the lower zone moisture deficiency ratio
        self.fr = 1.0
        #     fr is the change in percolation withdrawal due to frozen ground.
        self.fi = 1.0
        #     fi is the change in interflow withdrawal due to frozen ground.
        if self.ifrze != 0:
            uzdefr = 1.0 - ((self.uztwc + self.uzfwc) / (self.uztwm + self.uzfwm))
        self.fgfr1()
        
        perc = perc * (1.0 + zperc * (defr ** rexp)) * fr
        #     note...percolation occurs from uzfwc before pav is added.
        if (perc.lt.uzfwc) go to 241
        #      percolation rate exceeds uzfwc.
        perc = uzfwc
        #     percolation rate is less than uzfwc.
        241
        uzfwc = uzfwc - perc
        #     check to see if percolation exceeds lower zone deficiency.
        check = lztwc + lzfpc + lzfsc + perc - lztwm - lzfpm - lzfsm
        if (check.le.0.0) go to 242
        perc = perc - check
        uzfwc = uzfwc + check
        242
        sperc = sperc + perc
        #     sperc is the time interval summation of perc
        #
        #     compute interflow and keep track of time interval sum.
        #     note...pinc has not yet been added
        del = uzfwc * duz * fi
        sif = sif +
        del
        uzfwc = uzfwc -
        del
        #     distribe percolated water into the lower zones
        #     tension water must be filled first except for the pfree area.
        #     perct is percolation to tension water and percf is percolation
        #         going to free water.
        perct = perc * (1.0 - pfree)
        if ((perct + lztwc).gt.lztwm) go to 243
        lztwc = lztwc + perct
        percf = 0.0
        go
        to
        244
        243
        percf = perct + lztwc - lztwm
        lztwc = lztwm
        #
        #      distribute percolation in excess of tension
        #      requirements among the free water storages.
        244
        percf = percf + perc * pfree
        if (percf.eq.0.0) go to 245
        hpl = lzfpm / (lzfpm + lzfsm)
        #     hpl is the relative size of the primary storage
        #     as compared with total lower zone free water storage.
        ratlp = lzfpc / lzfpm
        ratls = lzfsc / lzfsm
        #     ratlp and ratls are content to capacity ratios, or
        #     in other words, the relative fullness of each storage
        fracp = (hpl * 2.0 * (1.0 - ratlp)) / ((1.0 - ratlp) + (1.0 - ratls))
        #     fracp is the fraction going to primary.
        if (fracp.gt.1.0) fracp = 1.0
        percp = percf * fracp
        percs = percf - percp
        #     percp and percs are the amount of the excess
        #     percolation going to primary and supplemental
        #      storges,respectively.
        lzfsc = lzfsc + percs
        if (lzfsc.le.lzfsm) go to 246
        percs = percs - lzfsc + lzfsm
        lzfsc = lzfsm
        246
        lzfpc = lzfpc + (percf - percs)
        #     check to make sure lzfpc does not exceed lzfpm.
        if (lzfpc.le.lzfpm) go to 245
        excess = lzfpc - lzfpm
        lztwc = lztwc + excess
        lzfpc = lzfpm
        #
        #     distribute pinc between uzfwc and surface runoff.
        245 if (pinc.eq.0.0)
        go
        to
        249
        #     check if pinc exceeds uzfwm
        if ((pinc + uzfwc).gt.uzfwm) go to 248
        #     no surface runoff
        uzfwc = uzfwc + pinc
        go
        to
        249
        #
        #     compute surface runoff (sur) and keep track of time interval sum.
        248
        sur = pinc + uzfwc - uzfwm
        uzfwc = uzfwm
        ssur = ssur + sur * parea
        adsur = sur * (1.0 - addro / pinc)
        #     adsur is the amount of surface runoff which comes
        #     from that portion of adimp which is not
        #     currently generating direct runoff.  addro/pinc
        #     is the fraction of adimp currently generating
        #     direct runoff.
        ssur = ssur + adsur * adimp  #  #     adimp area water balance -- sdro is the 6 hr sum of  #          direct runoff.
    
    def fgfr1(self):
        # Compute the change in the percolation and interflow withdrawal rates due to frozen ground.
        # The following vars are references to items from an array that I still need to find.
        findx = 1.0
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
        