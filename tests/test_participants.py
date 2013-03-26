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
    
    new_offers = ({'band': '2', 'price': 50, 'offer': 100},
                  {'band': '3', 'price': 100, 'offer': 150})
                  
    ST.add_multiple_energy_offers(new_offers)
    assert ST.band_names == ["ST_1", "ST_2", "ST_3"]
    assert ST.band_offers["ST_2"] == 100
    assert ST.band_offers["ST_3"] == 150
    
    assert ST.band_prices["ST_2"] == 50
    assert ST.band_prices["ST_3"] == 100
    
    
def test_station_reserve_offer():

    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    CO = Company("CO")
    
    ST = Station("ST", ND, SO, CO, spinning=True, capacity=400)
    
    ST.add_reserve_offer(band="1", price=10, offer=50, prop=3)
    
    assert ST.rband_names == ["ST_Reserve_1"]
    assert ST.rband_offers["ST_Reserve_1"] == 50
    assert ST.rband_prices["ST_Reserve_1"] == 10
    assert ST.rband_proportions["ST_Reserve_1"] == 3
    
    
    # Run the same tests for a station without a spinning flag
    STFalse = Station("ST2", ND, SO, CO, spinning=False, capacity=400)
    
    STFalse.add_reserve_offer(band="1", price=30, offer=100, prop=4)
    
    # Note, since we set a spinning reserve flag to False these items
    # should not even exist in the units name space.
    assert 'rband_names' not in STFalse.__dict__
    assert 'rband_offers' not in STFalse.__dict__
    assert 'rband_prices' not in STFalse.__dict__
    assert 'rband_proportions' not in STFalse.__dict__
    
    
if __name__ == '__main__':
    pass
