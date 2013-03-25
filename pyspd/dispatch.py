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
    nzst_offers = ({'band': '1', 'price': 0.01, 'offer': 45},
                   {'band': '2', 'price': 15, 'offer': 15})
    
    nzst.add_multiple_offers(nzst_offers)
    
    # Create three generation stations, each with spinning capacity
    
    manapouri = Station("Manapouri", ben, SO, capacity=720, spinning=True)
    huntly = Station("Huntly", ben, SO, capacity=1000, spinning=True)
    maraetai = Station("Maraetai", hay, SO, capacity=600, spinning=True)
    
    # Add three band offers to each station
    
    man_energy_offers = ({'band':'1', 'price':0, 'offer':300},
                         {'band':'2', 'price':25, 'offer':200},
                         {'band':'3', 'price':50, 'offer':220})
    
    hly_energy_offers = ({'band': '1', 'price': 20, 'offer': 300},
                         {'band': '2', 'price': 25, 'offer': 200},
                         {'band': '3', 'price': 50, 'offer': 220})
    
    mti_energy_offers = ({'band': '1', 'price': 2, 'offer': 300},
                         {'band': '2', 'price': 25, 'offer': 200},
                         {'band': '3', 'price': 50, 'offer': 220})
    
    
    manapouri.add_multiple_energy_offers(man_energy_offers)
    huntly.add_multiple_energy_offers(hly_energy_offers)
    maraetai.add_multiple_energy_offers(mti_energy_offers)    

    
    # Add two band reserve offers to two of the stations
    
    man_reserve_offers = ({'band': '1', 'price': 0.5, 'offer': 50, 'prop': 2},
                          {'band': '2', 'price': 0.5, 'offer': 150, 'prop': 2})
    
    mti_reserve_offers = ({'band': '1', 'price': 0.8, 'offer': 150, 'prop': 2},
                          {'band': '2', 'price': 5, 'offer': 500, 'prop': 2})
                          
    manapouri.add_multiple_reserve_offers(man_reserve_offers)
    maraetai.add_multiple_reserve_offers(mti_reserve_offers)
    
    
    # Create the offers
    SO.create_offers()
    
    # Solve the linear program
    
    Solver = LPSolver(SO)
    
    Solver.setup_lp()
    Solver.solve_lp()
    
    Solver.return_dispatch()
