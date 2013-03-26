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
    
    
def test_station_price_dispatch():
    
    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    CO = Company("CO")
    
    ST = Station("ST", ND, SO, CO, spinning=False, capacity=400)
    
    ND.add_price(400)
    ST.add_dispatch(300)
    
    assert ST.energy_dispatch == 300
    assert ST.energy_revenue == 300 * 400
    assert ST.total_revenue == 300 * 400
    
def test_station_energy_and_reserve():

    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    CO = Company("CO")
    
    ST = Station("ST", ND, SO, CO, spinning=True, capacity=400)

    ND.add_price(400)
    ST.add_dispatch(300)
    
    RZ.add_price(200)
    ST.add_res_dispatch(200)
    
    assert ST.reserve_dispatch == 200
    assert ST.reserve_revenue == 200 * 200
    assert ST.total_revenue == 200 * 200 + 400 * 300


    
def test_node_creation():

    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    
    assert ND.name == "ND"
    assert ND.nodal_stations == []
    assert ND.demand == 0
    assert ND.ISO == SO
    assert ND.RZ == RZ
    assert ND.intload == []
    
def test_node_additions():

    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    Co =Company("Co")
    
    ST = Station("ST", ND, SO, Co, spinning=True, capacity=400)
    IL = InterruptibleLoad("IL", ND, SO, Co, capacity=300)
    
    assert ND.nodal_stations == [ST]      
    assert ND.RZ.stations == [ST]
    assert ND.RZ.intload == [IL]
    assert ND.intload == [IL]
    
    
def test_node_methods():
    
    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    
    ND.set_demand(200)
    ND.add_price(100)
    
    assert ND.demand == 200
    assert ND.price == 100
    assert ND.load_cost == 200 * 100
    
def test_branch_creation():

    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND1 = Node("ND1", SO, RZ)
    ND2 = Node("ND2", SO, RZ)
    
    BR = Branch(ND1, ND2, SO, capacity=500, loss_factor=0.2, bands=2)
    
    assert BR.name == "ND1_ND2"
    assert BR.sending_node == ND1
    assert BR.receiving_node == ND2
    assert BR.capacity == 500
    assert BR.lf == 0.2
    assert BR.risk == False
    
    assert BR.bands == ["ND1_ND2_1", "ND1_ND2_2"]
    assert BR.bc["ND1_ND2_1"] == 500 / 2.
    assert BR.blf["ND1_ND2_1"] == 2 * 0.5 * 250. * 0.2
    
    BR.add_flow(300)
    
    assert BR.flow == 300
    
    
    
    
if __name__ == '__main__':
    pass
