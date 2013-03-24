import sys
import os

sys.path.append(os.path.expanduser('~/python/pyspd/pyspd'))

from iso import ISO
from participants import Station, Node, ReserveZone
from model import LPSolver

if __name__ == '__main__':
    
    # Set up the simulation
    
    SO = ISO("System Operator")
    
    RZNorth = ReserveZone("North", SO)
    RZSouth = ReserveZone("South", SO)
    
    hay = Node("Haywards", SO, RZNorth, demand=100)
    ben = Node("Benmore", SO, RZSouth, demand=200)
    
    manapouri = Station("Manapouri", ben, SO, capacity=720, spinning=True)
    huntly = Station("Huntly", hay, SO, capacity=1000, spinning=True)
    maraetai = Station("Maraetai", hay, SO, capacity=600, spinning=True)
    
    manapouri.add_energy_offer(band='1', price=5, offer=300)
    manapouri.add_energy_offer(band='2', price=25, offer=200)
    manapouri.add_energy_offer(band='3', price=50, offer=220)
    
    huntly.add_energy_offer(band='1', price=5, offer=300)
    huntly.add_energy_offer(band='2', price=25, offer=200)
    huntly.add_energy_offer(band='3', price=50, offer=220)
    
    maraetai.add_energy_offer(band='1', price=5, offer=300)
    maraetai.add_energy_offer(band='2', price=25, offer=200)
    maraetai.add_energy_offer(band='3', price=50, offer=220)
    
    manapouri.add_reserve_offer(band='1', price=1, offer=50, proportion=0.5)
    manapouri.add_reserve_offer(band='2', price=5, offer=25, proportion=0.7)
    
    SO.get_nodal_demand()
    SO.get_energy_offers()
    SO.get_reserve_offers()

