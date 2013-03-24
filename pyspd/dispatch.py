import sys
import os

sys.path.append(os.path.expanduser('~/python/pyspd/pyspd'))

from iso import ISO
from participants import Station, Node
from model import LPSolver

if __name__ == '__main__':
    
    # Set up the simulation
    
    SO = ISO("System Operator")
    
    hay = Node("Haywards")
    ben = Node("Benmore")
    
    manapouri = Station("Manapouri", ben, SO, 720, spinning=True)
    huntly = Station("Huntly", hay, SO, 1000, spinning=True)
    
    manapouri.add_energy_offer('1', 5, 300)
    manapouri.add_energy_offer('2', 25, 200)
    manapouri.add_energy_offer('3', 50, 220)
    
    huntly.add_energy_offer('1', 5, 300)
    huntly.add_energy_offer('2', 25, 200)
    huntly.add_energy_offer('3', 50, 220)

