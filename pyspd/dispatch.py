import sys
import os

sys.path.append(os.path.expanduser('~/python/pyspd/pyspd'))

from iso import ISO
from participants import Station, Node, ReserveZone, Branch
from participants import InterruptibleLoad
from model import LPSolver

if __name__ == '__main__':
    
    # Set up the simulation
    
    SO = ISO("System Operator")
    
    # Add two Reserve Zones
    
    RZNorth = ReserveZone("North", SO)
    RZSouth = ReserveZone("South", SO)
    
    # Create a two node system
    
    hay = Node("Haywards", SO, RZNorth, demand=50)
    ben = Node("Benmore", SO, RZSouth, demand=50)
    
    # Create a single transmission branch between them
    
    HVDC = Branch(hay, ben, SO, capacity=700, risk=True)
    
    # Create an IL provider
    nzst = InterruptibleLoad("NZST", hay, SO, capacity=60)
    nzst.add_offer('1', 0.01, 45)
    nzst.add_offer('2', 15, 15)
    
    # Create three generation stations, each with spinning capacity
    
    manapouri = Station("Manapouri", ben, SO, capacity=720, spinning=True)
    huntly = Station("Huntly", ben, SO, capacity=1000, spinning=True)
    maraetai = Station("Maraetai", hay, SO, capacity=600, spinning=True)
    
    # Add three band offers to each station
    
    manapouri.add_energy_offer(band='1', price=0, offer=300)
    manapouri.add_energy_offer(band='2', price=25, offer=200)
    manapouri.add_energy_offer(band='3', price=50, offer=220)
    
    huntly.add_energy_offer(band='1', price=20, offer=300)
    huntly.add_energy_offer(band='2', price=25, offer=200)
    huntly.add_energy_offer(band='3', price=50, offer=220)
    
    maraetai.add_energy_offer(band='1', price=2, offer=300)
    maraetai.add_energy_offer(band='2', price=25, offer=200)
    maraetai.add_energy_offer(band='3', price=50, offer=220)
    
    # Add two band reserve offers to two of the stations
    
    manapouri.add_reserve_offer(band='1', price=0.5, offer=50, proportion=2)
    manapouri.add_reserve_offer(band='2', price=0.5, offer=150, proportion=2)
    
    maraetai.add_reserve_offer(band='1', price=0.8, offer=150, proportion=2)
    maraetai.add_reserve_offer(band='2', price=5, offer=100, proportion=2)
    
    # Create the offers
    SO.create_offers()
    
    # Solve the linear program
    
    Solver = LPSolver(SO)
    
    Solver.setup_lp()
    Solver.write_lp()
    Solver.solve_lp()
