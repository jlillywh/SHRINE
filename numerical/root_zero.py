
class Root:
    def __init__(self, high_guess=9.0e3, low_guess=1.0e-4,
                 error_tolerance=1.0e-5, max_loops=200):
        self.high_guess = high_guess
        self.low_guess = low_guess
        self.error_tolerance = error_tolerance
        self.max_loops = max_loops
        
    def binary_search(self, function):
        converged = False
        loop_count = 0
        while not converged:
            mid = self.low_guess + (self.high_guess - self.low_guess) / 2.0
            
            if function(mid):
                self.high_guess = mid
            else:
                self.low_guess = mid
            
            # Check for convergence
            if loop_count > self.max_loops:
                print("Flow solver did not converge after " +
                      str(self.max_loops) + " iterations!")
                break
            error = (self.high_guess - self.low_guess) / mid
            converged = error <= self.error_tolerance
            loop_count = loop_count + 1
        
        return mid