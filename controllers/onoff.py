from inputs.constants import U



class OnOff:
    """A 2-position control system that only has fully on or fully off states.
    
        This type of controller is good for turning on/off an actuator to a component
        that feeds a system or draws from it. The state is switched by evaluating
        the difference between the process variable from the set point.
        
        Attributes
        ----------
        status : bool
            This is the controller's state. True indicates fully ON and false indicates
            fully OFF.
        deadband : quantity
            Depending on the operation, the deadband is either a fraction of the process
            variable quantity or of time.
            
        Methods
        -------
        
        
    """
    def __init__(self, direction, set_point, deadband=0.5 * U.m, deadband_justify='center', init_status=True):
        """Initialize the shutoff controller
        
            Parameters
            ----------
            measurement : Quantity
                This is the state variable that we are monitoring in measurement to the set_point
            direction: str
                The choices are 'UP' or 'DOWN'
                A positive value indicates that rate inputs add to the measurement to bring the
                measurement up to the set_point
            set_point: Quantity
                The set_point is the value sought by the measurement quantity.
            deadband : Quantity
                The range of dead zone around the set_point. No change of state will occur within
                this zone
            deadband_justify : str
                This defines how the deadband is situated relative to the set_point. A value of
                'center' means the set_point lies exactly in the center of the dead band. A value
                of 'top' means the targt lies at the very bottom of the deadband while 'bottom'
                indicates that the set_point lies at the bottom of the deadband.
            init_status: bool
                Starting status value. This is the state of the controller. True means "on" and
                False means "off."
            
        """
        self.direction = direction
        self.set_point = set_point
        self.deadband = deadband
        self.deadband_justify = deadband_justify
        if self.deadband_justify == 'center':
            self.upper = self.set_point + deadband / 2.0
            self.lower = self.set_point - deadband / 2.0
        elif self.deadband_justify == 'top':
            self.upper = self.set_point + deadband
            self.lower = self.set_point
        elif self.deadband_justify == 'bottom':
            self.lower = self.set_point - deadband
            self.upper = self.set_point
        else:
            AssertionError("Center, Top, Bottom only")
            
        self.status = init_status
    
    def update(self, new_measurement):
        """reports the status of the control object
        
            The status is only changed if the measurement has moved
            out of the range of the deadband since the last update.
        
            Returns
            -------
            on : bool
                True if the control is on; False if off
        """
        
        if self.status:
            if new_measurement >= self.upper and self.direction == 'UP':
                self.status = False
            elif new_measurement <= self.lower and self.direction == 'DOWN':
                self.status = False
        else:
            if new_measurement <= self.lower and self.direction == 'UP':
                self.status = True
            elif new_measurement >= self.upper and self.direction == 'DOWN':
                self.status = True
        return self.status
