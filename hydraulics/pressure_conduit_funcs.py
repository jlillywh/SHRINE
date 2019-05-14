from global_attributes.constants import nu
import math
import scipy.constants as const


def friction_loss(pipe, flow_rate, method='HW'):
    """Function that takes a reach of pipe and flow rate then returns the head loss
        due to friction. Units are in SI.
        
        Parameters
        ----------
        pipe : Pipe object
        flow_rate : float
            Assumed flow rate in terms of m3/s
        method : str
            Options are HW: Hazen-Williams or DW: Darcy-Weisbach
            'HW' is default
        
        Returns
        -------
        head_loss : float
        
    """
    hf = 0.0
    length = pipe.length
    d = pipe.diameter
    a = pipe.area
    c = pipe.hazen_williams
    q = flow_rate
    
    if method == 'HW':
        k = 0.849    # conversion factor for unit conversion (use SI)
        slope = 7.8828 / k**1.852 * q**1.852 / (c**1.852 * d**4.8704)
        hf = slope * length
    elif method == 'DW':
        velocity = q / a
        kin_viscosity = nu
        reynolds = d * velocity / kin_viscosity
        f = 0.02
        
        # Solve for friction factor based on type of flow found
        if reynolds < 2000.0:
            #  For laminar flow only (Hagen - Poiseuille formula)
            f = 64.0 / reynolds
        elif 2000.0 <= reynolds < 4000.0:
            #  Cubic interpolation from Moody Diagram
            y2 = pipe.roughness / (3.7 * d) + 5.74 / (reynolds**0.9)
            y3 = -0.86859 * math.log(pipe.roughness / (3.7 * d) + 5.74 / (4000.0**0.9))
            fa = y3**-2
            fb = fa * (2.0 - 0.00514215 / (y2 * y3))
            r = reynolds / 2000.0
            x4 = r * (0.032 - 3.0 * fa + 0.5 * fb)
            x3 = -0.128 + 13.0 * fa - 2 * fb
            x2 = 0.128 - 17.0 * fa + 2.5 * fb
            x1 = 7.0 * fa - fb
            f = x1 + r * (x2 + r * (x3 + x4))
        
        else:
            if pipe.roughness / d < 0.01:
                # Moody approximation (iterate solving "f" until done)
                f2 = (-2.0 * math.log10(((pipe.roughness / d) / 3.7) + (2.51 / (reynolds * (f ** 0.5))))) ** -2
                while not math.isclose(f2, f, rel_tol=1e-6):
                    f2 = f
                    f = (-2.0 * math.log10(((pipe.roughness/d) / 3.7) + (2.51 / (reynolds * (f2**0.5)))))**-2
            else:
                #  Swamee and Jain approximation
                f = 0.25 / (math.log(pipe.roughness/(3.7 * d) + 5.74 / (reynolds**0.9)))**2
        
        # Darcy - Weisbach equation for both smooth and rough walled pipes
        hf = f * length / d * velocity**2 / (2 * const.g)
    
    return hf
