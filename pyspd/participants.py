
class Station:
    def __init__(self, name, node, ISO, capacity=0, ebands=3, spinning=False):
        self.name = name
        self.capacity = capacity
        self.spinning = spinning
        self.band_names = []
        self.band_offers = {}
        self.band_prices = {}
        
        node.add_station(self)
        ISO._add_station(self)
        
        
        if self.spinning:
            self.rband_names = []
            self.rband_offers = {}
            self.rband_prices = {}
            self.rband_proportions = {}
        
    def add_energy_offer(self, band='0', price=0, offer=0):
        """ Add an Offer"""
        # Get the band name
        band_name = '_'.join([self.name, band])
        
        self.band_names.append(band_name)
        self.band_offers[band_name] = offer
        self.band_prices[band_name] = price
        
    def add_reserve_offer(self, band='0', price=0, proportion=0, offer=0):
        """ Add a reserve offer """
        if self.spinning:
            rband_name = '_'.join([self.name, 'reserve', band])
            self.rband_names.append(rband_name)
            self.rband_offers[rband_name] = offer
            self.rband_prices[rband_name] = price
            self.rband_proportions[rband_name] = proportion
            
        else:
            print "Not a spinning station, cannot add reserve offers"
        
        
class Node:


    def __init__(self, name, ISO, RZ, demand=0):
        self.name = name
        self.nodal_stations = []
        self.demand = demand
        ISO._add_node(self)
        RZ._add_node(self)
        
        
    def add_station(self, Station):
        self.nodal_stations.append(Station)
        
    def set_demand(self, demand):
        self.demand = demand
        
        
class Branch:

    def __init__(self, name):
        self.name = name
        
        
class ReserveZone:
    
    def __init__(self, name, ISO):
        self.name = name
        self.nodes = []
        ISO._add_reserve_zone(self)
        
    
    def _add_node(self, node):
        
        self.nodes.append(node)
        
        
if __name__ == '__main__':
    pass 
    
