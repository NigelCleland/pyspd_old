import pulp as lp
import numpy as np

class LPSolver:
    """ Linear Program Solver fo the small models
    """
    
    def __init__(self, ISO):
        self.ISO = ISO
        
    
    def setup_lp(self, reserve=True, proportion=True, combined=True,
                 transmission=True):
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
        tbm = self.ISO.transmission_band_maximum
        
        etm = self.ISO.energy_total_maximum
        ttm = self.ISO.transmission_total_maximum
        rbpr = self.ISO.reserve_band_proportion
        
        spin = self.ISO.spinning_station_names
        spin_map = self.ISO.spin_map
        
        node_map = self.ISO.node_energy_map
        demand = self.ISO.node_demand
        
        node_t_map = self.ISO.node_t_map
        td = self.ISO.node_transmission_direction
        
        rzones = self.ISO.reserve_zone_names
        rzone_g = self.ISO.reserve_zone_generators
        rzone_t = self.ISO.reserve_zone_transmission
        
        rz_providers = self.ISO.reserve_zone_reserve
        
        # Set up the linear program        
        
        self.lp = lp.LpProblem("Model Dispatch", lp.LpMinimize)
        
        # Add variables
        ebo = lp.LpVariable.dicts("energy_band", eb, 0)
        rbo = lp.LpVariable.dicts("reserve_band", rb, 0)
        tbo = lp.LpVariable.dicts("transmission_band", tb)
        
        eto = lp.LpVariable.dicts("energy_total", et, 0)
        rto = lp.LpVariable.dicts("reserve_total", rt, 0)
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
            n1 = '_'.join([n, 'energy_price'])
            n2 = '_'.join([n, 'nodal_transmission'])
            addC(node_inj[n] == SUM([eto[i] for i in node_map[n]]) - demand[n], n1)
            addC(node_inj[n] == SUM([tto[i] * td[n][i] for i in node_t_map[n]]), n2)
        
        # Individual Band Offer
        for i in eb:
            name = '_'.join([i, 'band_energy'])
            addC(ebo[i] <= ebm[i], name)
            
        # Reserve Band Offer
        for j in rb:
            name = '_'.join([j, 'band_reserve'])
            addC(rbo[j] <= rbm[j], name)
            
        # Transmission band Offer
        for t in tb:
            addC(tbo[t] <= tbm[t])
            addC(tbo[t] >= tbm[t] * -1)
            
        # Energy Total Offer
        for i in et:
            name = '_'.join([i, 'total_energy'])
            addC(SUM([ebo[j] for j in ebmap[i]]) == eto[i], name)
            
        # Reserve Total Offer
        for i in rt:
            name = '_'.join([i, 'total_reserve'])
            addC(SUM([rbo[j] for j in rbmap[i]]) == rto[i], name)
            
        # Transmission Total offer
        for i in tt:
            addC(SUM([tbo[j] for j in tbmap[i]]) == tto[i])
            addC(tto[i] <= ttm[i])
            addC(tto[i] >= ttm[i] * -1)
            
        # Spinning Reserve Constraints
        for i in spin:
            name = '_'.join([i, 'combined_dispatch'])
            addC(rto[i] + eto[i] <= etm[i], name)
            
            for j in spin_map[i]:
                name = '_'.join([i, j, 'prop'])
                addC(rbo[j] <= rbpr[j] * eto[i], name)
                
        
        # Risk Constraints
        
        for r in rzones:
            # Generation Risk
            for i in rzone_g[r]:
                name = '_'.join([r, i])
                addC(risk[r] >= eto[i], name)
        
            # Transmission Risk        
            for t in rzone_t[r]:
                name = '_'.join([r, t])
                addC(risk[r] >= -1 * tto[t], name)
                
        # Reserve Dispatch
        for r in rzones:
            n1 = '_'.join([r, 'reserve_price_pos'])
            n2 = '_'.join([r, 'reserve_price_neg'])
            addC(SUM(rto[i] for i in rz_providers[r]) - risk[r] >= 0., n1)
        
        
    def write_lp(self):
        self.lp.writeLP("Test.lp")
        
    def solve_lp(self):
        self.lp.solve(lp.COIN_CMD())
        print "LP Status is:", lp.LpStatus[self.lp.status]
        print 'Objective function value is:', lp.value(self.lp.objective)
        
        
    def get_values(self):
        for val in self.lp.variables():
            print val, val.varValue
            
            
    def get_shadow_values(self):
        for n in self.lp.constraints:
            try:
                print n, self.lp.constraints[n].pi
            except:
                print n, 0
        
    def get_prices(self):
        for n in self.lp.constraints:
            if "price" in n:
                try:
                    print n, self.lp.constraints[n].pi
                except:
                    print n, "no value"
        
                
if __name__ == '__main__':
    pass
