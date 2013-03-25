
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
        
        self.node = node
        
        
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
        
    def add_reserve_offer(self, band='0', price=0, prop=0, offer=0):
        """ Add a reserve offer """
        if self.spinning:
            rband_name = '_'.join([self.name, 'reserve', band])
            self.rband_names.append(rband_name)
            self.rband_offers[rband_name] = offer
            self.rband_prices[rband_name] = price
            self.rband_proportions[rband_name] = prop
            
        else:
            print "Not a spinning station, cannot add reserve offers"
            
    def add_multiple_energy_offers(self, offer_dict):
        for row in offer_dict:
            self.add_energy_offer(**row)
            
    
    def add_multiple_reserve_offers(self, offer_dict):
        for row in offer_dict:
            self.add_reserve_offer(**row)
            
            
    def add_dispatch(self, dispatch):
        self.energy_dispatch = dispatch
        self.calculate_energy_revenue()
        
        
    def calculate_energy_revenue(self):
        self.energy_revenue = self.energy_dispatch * self.node.price
        

    def add_res_dispatch(self, dispatch):
        self.reserve_dispatch = dispatch
        
        
class Node:


    def __init__(self, name, ISO, RZ, demand=0):
        self.name = name
        self.nodal_stations = []
        self.intload = []
        self.demand = demand
        self.RZ = RZ
        self.ISO = ISO
        self.ISO._add_node(self)
        self.RZ._add_node(self)
        self.price = 0
        
        
    def add_station(self, Station):
        self.nodal_stations.append(Station)
        self.RZ._add_station(Station)
        
        
    def set_demand(self, demand):
        self.demand = demand
        
        
    def add_intload(self, Load):
        self.intload.append(Load)
        self.RZ._add_intload(Load)
        
        
    def add_price(self, price):
        self.price = price
        self.load_cost()
        
        
    def load_cost(self):
        self.load_cost = self.demand * self.price
        
class Branch:

    def __init__(self, SN, RN, ISO, capacity=0, loss_factor=0.0001, bands=3,
                 risk=False):
        self.name = '_'.join([SN.name, RN.name])
        self.sending_node = SN
        self.receiving_node = RN
        self.capacity = capacity
        self.lf = loss_factor
        self.ISO = ISO
        self.risk = risk

        
        self.bands = []
        self.bc = {} # Branch band capacity
        self.blf = {} # Branch band loss factor
        
        ISO._add_branch(self)
        
        self._create_bands(bands=bands)
        
    def _create_bands(self, bands=3):
        
        for band in xrange(bands):
            b = str(band + 1)
            band_name = '_'.join([self.name, b])
            
            self.bands.append(band_name)
            
            self.bc[band_name] = self.capacity / bands * 1.0
            self.blf[band_name] = 2 * (band + 0.5) * self.bc[band_name] * self.lf
            
            
    def add_flow(self, flow):
        self.flow = flow
        
        
        
class ReserveZone:
    
    def __init__(self, name, ISO):
        self.name = name
        self.nodes = []
        ISO._add_reserve_zone(self)
        self.stations = []
        self.intload = []
        self.price = 0
    
    def _add_node(self, node):
        
        self.nodes.append(node)
        
    def _add_station(self, station):
        self.stations.append(station)
        
    def _add_intload(self, IL):
        self.intload.append(IL)
        
    
    def add_price(self, price):
        self.price = price
        
        
class InterruptibleLoad:

    def __init__(self, name, node, ISO, capacity=0):
        self.name = name
        self.node = node
        self.capacity=0
        
        
        node.add_intload(self)
        ISO._add_intload(self)
        
        self.band_names = []
        self.band_prices = {}
        self.band_offers = {}
        
    
    def add_offer(self, band='0', price=0, offer=0):
        name = '_'.join([self.name, band])
        self.band_names.append(name)
        self.band_prices[name] = price
        self.band_offers[name] = offer
        
    def add_multiple_offers(self, offer_dict):
        for row in offer_dict:
            self.add_offer(**row)   
            
            
    def add_res_dispatch(self, dispatch):
        self.reserve_dispatch = dispatch     
        
        
if __name__ == '__main__':
    pass 
    
