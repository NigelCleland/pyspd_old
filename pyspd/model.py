import pulp as lp
import numpy as np

class LPSolver:
    """ Linear Program Solver fo the small models
    """
    
    def __init__(self):
        pass
        
    
    def setup_lp(self):
        """ Set up the Linear Program by creating an objective function and 
            passing the requisite variables to it.
        
        """
        
        self.lp = lp.LpProblem("Model Dispatch", lp.LpMinimize)
        
        # Add variables
        
    
    
