

def friction_loss(pipe, flow_rate, method='HW'):
    """Function that takes a reach of pipe and flow rate then returns the head loss
        due to friction.
        
        #TODO: add metric option
        #TODO: add D-W calculation option
        
        Parameters
        ----------
        pipe : Pipe object
        flow_rate : float
        method : str 'HW' is default
            Options are HW: Hazen-Williams or DW: Darcy-Weisbach
        
        Returns
        -------
        head_loss : float
        
    """
    hf = 0.0
    if method == 'HW':
        hf = ((4.73 * pipe.hazen_williams ** -1.852 * pipe.length * pipe.diameter ** -4.87) * flow_rate ** 1.852)
    
    return hf
