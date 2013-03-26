""" Test the ISO Class """

from nose.tools import *

import os
import sys
sys.path.append(os.path.expanduser('~/python/pyspd/pyspd/'))

from api import *


def test_creation():
    SO = ISO("System Operator")
    assert SO.name == "System Operator"
    assert SO.stations == []
    assert SO.spinning_stations == []
    assert SO.nodes == []
    assert SO.branches == []

    assert SO.node_name_map == {}
    assert SO.reserve_zone_name_map == {}
    assert SO.station_name_map == {}
    assert SO.reserve_name_map == {}  
    assert SO.branch_name_map == {}
    
    assert SO.intload == []
    assert SO.intload_names == []
    
    
def test_add_reserve_zone():
    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    
    assert SO.reserve_zones == [RZ]
    assert SO.reserve_zone_names == [RZ.name]
    assert SO.reserve_zone_name_map[RZ.name] == RZ
    
    
def test_add_node():
    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    
    assert SO.nodes == [ND]
    assert SO.node_name_map[ND.name] == ND
    assert SO.reserve_zone_name_map[RZ.name].nodes == [ND]
    # Circular test to see proper assignment
    assert SO.reserve_zone_name_map[RZ.name].nodes[0].ISO == SO
   
def test_add_station():
    SO = ISO("System Operator")
    RZ = ReserveZone("RZ", SO)
    ND = Node("ND", SO, RZ)
    CO = Company("CO")
    
    ST = Station("ST", ND, SO, CO, spinning=True)
    
    assert SO.stations == [ST]
    assert SO.spinning_stations == [ST]
    assert SO.station_name_map[ST.name] == ST
    assert SO.reserve_name_map[ST.name] == ST
    assert SO.node_name_map[ND.name].nodal_stations == [ST]
    assert SO.reserve_zone_name_map[RZ.name].stations == [ST]
    
   
if __name__ == '__main__':
    pass
