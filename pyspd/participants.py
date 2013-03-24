
class Station:
    def __init__(self, name, node, capacity, ebands=3, spinning=False):
        self.name = name
        self.capacity = capacity
        self.spinning = spinning
        self.band_names = []
        self.band_offers = {}
        self.band_prices = {}
        
        node.add_station(self)
        
        if self.spinning:
            self.rband_names = []
            self.rband_offers = {}
            self.rband_prices = {}
            self.rband_proportions = {}
        
    def add_energy_offer(self, band, price, maximum):
        """ Add an Offer"""
        # Get the band name
        band_name = '_'.join([self.name, band])
        self.band_names.append(band_name)
        self.band_offers[band_name] == maximum
        self.band_prices[band_name] == price
        
    def add_reserve_offer(self, band, price, proportion, maximum):
        """ Add a reserve offer """
        if self.spinning:
            rband_name = '_'.join([self.name, 'reserve', band])
            self.rband_names.append(rband_name)
            self.rband_offers[rband_name] == maximum
            self.rband_prices[rband_name] = price
            self.rband_proportions[rband_name] == proportion
            
        else:
            print "Not a spinning station, cannot add reserve offers"
        
        
class Node:


    def __init__(self, name):
        self.name = name
        self.nodal_stations = []
        
        
    def add_station(self, Station):
        self.nodal_stations.append(Station)
        
        
class 
    
