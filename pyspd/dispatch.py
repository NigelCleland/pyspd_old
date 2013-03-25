import sys
import os

sys.path.append(os.path.expanduser('~/python/pyspd/pyspd'))

from iso import ISO
from participants import Station, Node, ReserveZone, Branch
from model import LPSolver

if __name__ == '__main__':
    
    # Set up the simulation
    
    SO = ISO("System Operator")
    
    RZNorth = ReserveZone("North", SO)
    RZSouth = ReserveZone("South", SO)
    
    hay = Node("Haywards", SO, RZNorth, demand=50)
    ben = Node("Benmore", SO, RZSouth, demand=50)
    ota = Node("Otahuhu", SO, RZNorth, demand=50)
    kik = Node("Kik", SO, RZSouth, demand=50)
    
    HVDC = Branch(hay, ben, SO, capacity=700, risk=True)
    Hay_Ota = Branch(hay, ota, SO, capacity=1000)
    Ben_kik = Branch(ben, kik, SO, capacity=1000)
    
    manapouri = Station("Manapouri", ben, SO, capacity=720, spinning=True)
    huntly = Station("Huntly", ota, SO, capacity=1000, spinning=True)
    maraetai = Station("Maraetai", hay, SO, capacity=600, spinning=True)
    
    manapouri.add_energy_offer(band='1', price=0, offer=300)
    manapouri.add_energy_offer(band='2', price=25, offer=200)
    manapouri.add_energy_offer(band='3', price=50, offer=220)
    
    huntly.add_energy_offer(band='1', price=20, offer=300)
    huntly.add_energy_offer(band='2', price=25, offer=200)
    huntly.add_energy_offer(band='3', price=50, offer=220)
    
    maraetai.add_energy_offer(band='1', price=2.5, offer=300)
    maraetai.add_energy_offer(band='2', price=25, offer=200)
    maraetai.add_energy_offer(band='3', price=50, offer=220)
    
    manapouri.add_reserve_offer(band='1', price=1, offer=50, proportion=2)
    manapouri.add_reserve_offer(band='2', price=1, offer=150, proportion=2)
    
    maraetai.add_reserve_offer(band='1', price=1, offer=100, proportion=2)
    maraetai.add_reserve_offer(band='2', price=1, offer=100, proportion=2)
    
    SO.get_nodal_demand()
    SO.get_energy_offers()
    SO.get_reserve_offers()
    SO.get_network()
    
    Solver = LPSolver(SO)
    
    Solver.setup_lp()
    Solver.write_lp()
    Solver.solve_lp()
