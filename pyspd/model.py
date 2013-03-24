import pulp as lp
import numpy as np

class LPSolver:
    """ Linear Program Solver fo the small models
    """
    
    def __init__(self, ISO):
        self.ISO = ISO
        
    
    def setup_lp(self):
        """ Set up the Linear Program by creating an objective function and 
            passing the requisite variables to it.
        
        """
        
        # Get the Constraints and lists for model creation simplification
        eb = self.ISO.energy_bands
        rb = self.ISO.reserve_bands
        tb = self.ISO.transmission_bands
        nd  = self.ISO.all_nodes
        
        et = self.ISO.energy_totals
        rt = self.ISO.reserve_totals
        tt = self.ISO.transmission_totals
        
        ebmap = self.ISO.energy_band_map
        rbmap = self.ISO.reserve_band_map
        tbmap = self.ISO.transmission_band_map
               
        ebp = self.ISO.energy_band_prices
        rbp = self.ISO.reserve_band_prices

        ebm = self.ISO.energy_band_maximum
        rbm = self.ISO.reserve_band_maximum
        tbm = self.ISO.transmission_band_maximimum
        
        etm = self.ISO.energy_total_maximum
        ttm = self.ISO.transmission_total_maximum
        rbpr = self.ISO.reserve_band_proportion
        
        spin = self.ISO.spinning_stations
        spin_map = self.ISO.spinning_map        
        
        self.lp = lp.LpProblem("Model Dispatch", lp.LpMinimize)
        
        # Add variables
        ebo = lp.LpVariable.dicts("energy_band", eb, 0)
        rbo = lp.LpVariable.dicts("reserve_band", rb, 0)
        tbo = lp.LpVariable.dicts("transmission_band", tb)
        
        eto = lp.LpVariable.dicts("energy_total", et)
        rto = lp.LpVariable.dicts("reserve_total", rt)
        tto = lp.LpVariable.dicts("transmission_total", tt)
        
        node_inj = lp.LpVariable.dict("nodal_inject", nd)
        
        
        # Map the add Constraint method to a simpler string
        addC = self.lp.addConstraint
        
        

        # Objective function
        self.lp.setObjective(lp.lpSum([ebo[i] * ebp[i] for i in eb]) +\
                             lp.lpSum([rbo[j] * rbp[j] for j in rb]))
                             
        # Begin Adding Constraint
        
        # Nodal Dispatch
        
        
        # Individual Band Offer
        for i in eb:
            addC(ebo[i] <= ebm[i])
            
        # Reserve Band Offer
        for j in rb:
            addC(rbo[j] <= rbm[j])
            
        # Transmission band Offer
        for t in tb:
            addC(tbo[t] <= tbm[t])
            addC(tbo[t] >= tbm[t] * -1)
            
        # Energy Total Offer
        for i in et:
            addC(lp.lpSum([ebo[j] for j in ebmap[i]]) == eto[i])
            
        # Reserve Total Offer
        for i in rt:
            addC(lp.lpSum([rbo[j] for j in rbmap[i]]) == rto[i])
            
        # Transmission Total offer
        for i in tt:
            addC(lp.lpSum([tbo[j] for j in tbmap[i]]) == tto[i])
            addC(tto[i] <= ttm[i])
            addC(tto[i] >= ttm[i] * -1)
            
        # Spinning Reserve Constraints
        for i in spin:
            addC(rto[i] + eto[i] <= etm[i]
            
            for j in spin_map[i]
                addC(rbo[j] <= rbpr[j] * eto[i])
                
                
        
            
       
        
        
    
    
