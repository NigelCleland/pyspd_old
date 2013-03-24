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
        
        spin = self.ISO.spinning_station_names
        spin_map = self.ISO.spinning_map
        
        node_map = self.ISO.node_energy_map
        demand = self.ISO.node_demand
        
        node_t_map = self.ISO.node_transmission_map
        td = self.ISO.node_transmission_direction
        
        rzones = self.ISO.reserve_zones
        rzone_g = self.ISO.reserve_zone_generators
        rzone_t = self.ISO.reserve_zone_transmission
        
        
        # Set up the linear program        
        
        self.lp = lp.LpProblem("Model Dispatch", lp.LpMinimize)
        
        # Add variables
        ebo = lp.LpVariable.dicts("energy_band", eb, 0)
        rbo = lp.LpVariable.dicts("reserve_band", rb, 0)
        tbo = lp.LpVariable.dicts("transmission_band", tb)
        
        eto = lp.LpVariable.dicts("energy_total", et)
        rto = lp.LpVariable.dicts("reserve_total", rt)
        tto = lp.LpVariable.dicts("transmission_total", tt)
        
        node_inj = lp.LpVariable.dicts("nodal_inject", nd)
        
        risk = lp.LpVariable.dicts("risk", rzones)
        
        
        # Map the add Constraint method to a simpler string
        addC = self.lp.addConstraint
        SUM = lp.lpSum
        
        

        # Objective function
        self.lp.setObjective(SUM([ebo[i] * ebp[i] for i in eb]) +\
                             SUM([rbo[j] * rbp[j] for j in rb]))
                             
        # Begin Adding Constraint
        
        # Nodal Dispatch
        for n in nd:
            addC(node_inj[n] == SUM([ebo[i] for i in node_map[n]]) - demand[n])
            addC(node_inj[n] == SUM([tto[i] * td[i] for i in node_t_map[n]]))
        
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
            addC(SUM([ebo[j] for j in ebmap[i]]) == eto[i])
            
        # Reserve Total Offer
        for i in rt:
            addC(SUM([rbo[j] for j in rbmap[i]]) == rto[i])
            
        # Transmission Total offer
        for i in tt:
            addC(SUM([tbo[j] for j in tbmap[i]]) == tto[i])
            addC(tto[i] <= ttm[i])
            addC(tto[i] >= ttm[i] * -1)
            
        # Spinning Reserve Constraints
        for i in spin:
            addC(rto[i] + eto[i] <= etm[i])
            
            for j in spin_map[i]:
                addC(rbo[j] <= rbpr[j] * eto[i])
                
        
        # Risk Constraints
        
        for r in rzones:
            # Generation Risk
            for i in rzone_g:
                addC(risk[r] >= eto[i])
        
            # Transmission Risk        
            for t in rzone_t:
                addC(risk[r] >= tto[t])
        
                
                
if __name__ == '__main__':
    pass
