from nose.tools import *

import os
import sys
sys.path.append(os.path.expanduser('~/python/pyspd/pyspd/'))

from api import *

def test_station_creation():
    """ Test the Station Class """
    
    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    CO = Company("CO")
    
    ST = Station("ST", ND, SO, CO, spinning=True, capacity=400)
    
    assert ST.name == "ST"
    assert ST,capacity == 400
    assert ST.spinning == True
    assert ST.band_names == []
    assert ST.band_offers == {}
    assert ST.band_prices == {}
    
    assert ST.node == ND
    
    assert ST.rband_names == []
    assert ST.rband_offers == {}
    assert ST.rband_prices == {}
    assert ST.rband_proportions == {}
    
def test_station_energy_offer():

    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    CO = Company("CO")
    
    ST = Station("ST", ND, SO, CO, spinning=True, capacity=400)
    
    ST.add_energy_offer(band='1', price=10, offer=50)
    
    assert ST.band_names == ["ST_1"]
    assert ST.band_offers["ST_1"] == 50
    assert ST.band_prices["ST_1"] == 10
    
    
if __name__ == '__main__':
    pass
