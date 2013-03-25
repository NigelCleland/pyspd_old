
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
        self.RZ = RZ
        self.ISO = ISO
        self.ISO._add_node(self)
        self.RZ._add_node(self)
        
        
    def add_station(self, Station):
        self.nodal_stations.append(Station)
        self.RZ._add_station(Station)
        
    def set_demand(self, demand):
        self.demand = demand
        
        
class Branch:

    def __init__(self, SN, RN, ISO, capacity=0, loss_factor=0.0001, bands=3):
        self.name = '_'.join([SN.name, RN.name])
        self.sending_node = SN
        self.receiving_node = RN
        self.capacity = capacity
        self.loss_factor = loss_factor
        self.ISO = ISO

        
        self.bands = []
        self.band_capacity = {}
        self.band_loss_factor = {}
        
        ISO._add_branch(self)
        
        self._create_bands(bands=bands)
        
    def _create_bands(self, bands=3):
        
        for band in xrange(bands):
            b = str(band + 1)
            band_name = '_'.join([self.name, b])
            
            self.bands.append(band_name)
            
            self.band_capacity[band_name] = self.capacity / bands * 1.0
            self.band_loss_factor[band_name] = 2 * (band + 0.5) * self.band_capacity[band_name] * self.loss_factor
        
        
        
class ReserveZone:
    
    def __init__(self, name, ISO):
        self.name = name
        self.nodes = []
        ISO._add_reserve_zone(self)
        self.stations = []
        
    
    def _add_node(self, node):
        
        self.nodes.append(node)
        
    def _add_station(self, station):
        self.stations.append(station)
        
        
if __name__ == '__main__':
    pass 
    
