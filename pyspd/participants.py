"""
Participants
------------

Classes to define different agents within the system

"""
class Station:
    """
    A generation station which is associated with a node and a particular
    company.
    
    May be capable of providing spinning reserve if explicitly set to and is
    capable of providing energy and reserve offers to the ISO.
    """
    def __init__(self, name, node, ISO, Company, capacity=0, ebands=3,
                 spinning=False):
        self.name = name
        self.capacity = capacity
        self.spinning = spinning
        self.band_names = []
        self.band_offers = {}
        self.band_prices = {}
        
        node.add_station(self)
        ISO._add_station(self)
        Company.add_station(self)
        
        self.node = node
        
        
        if self.spinning:
            self.rband_names = []
            self.rband_offers = {}
            self.rband_prices = {}
            self.rband_proportions = {}
        
    def add_energy_offer(self, band='0', price=0, offer=0):
        """ Add an Energy Offer to the Station"""
        # Get the band name
        band_name = '_'.join([self.name, band])
        
        self.band_names.append(band_name)
        self.band_offers[band_name] = offer
        self.band_prices[band_name] = price
        
    def add_reserve_offer(self, band='0', price=0, prop=0, offer=0):
        """ Add a reserve offer """
        if self.spinning:
            rband_name = '_'.join([self.name, 'Reserve', band])
            self.rband_names.append(rband_name)
            self.rband_offers[rband_name] = offer
            self.rband_prices[rband_name] = price
            self.rband_proportions[rband_name] = prop
            
        else:
            pass 
            
    def add_multiple_energy_offers(self, offer_dict):
        """ Add multiple energy offers to the stations"""
        for row in offer_dict:
            self.add_energy_offer(**row)
            
    
    def add_multiple_reserve_offers(self, offer_dict):
        """ Add multiple reserve offers to the station """
        for row in offer_dict:
            self.add_reserve_offer(**row)
            
            
    def add_dispatch(self, dispatch):
        """ Obtain the energy dispatch from the Solver and calculate the revenue"""
        self.energy_dispatch = dispatch
        self.calculate_energy_revenue()
        
        
    def calculate_energy_revenue(self):
        """ Calculates the energy revenue """
        self.energy_revenue = self.energy_dispatch * self.node.price
        if self.spinning == False:
            self.total_revenue = self.energy_revenue
        

    def add_res_dispatch(self, dispatch):
        """ Obtain the reserve dispatch from the Solver
        Calculate the reserve revenue
        Calculate the total revenue
        """
        self.reserve_dispatch = dispatch
        self.calculate_reserve_revenue()
        self.calculate_total_revenue()
        
    def calculate_reserve_revenue(self):
        """ calculate the reserve revenue """
        self.reserve_revenue = self.reserve_dispatch * self.node.RZ.price
        
    def calculate_total_revenue(self):
        """ Calculate the total revenue for a station """
        self.total_revenue = self.reserve_revenue + self.energy_revenue
        
        
class Node:
    """
    Node
    ----
    
    A node is a location in the grid which is associated with generation
    stations, IL providers, reserve zones and transmission connections.
    
    It has an associated demand which must be cleared at all points in time
    in order to uniquely solve the grid dispatch.
    
    As many nodes may be declared as desired and it may be connected via
    branches to the main network.
    """

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
        """ Add a station to the node """
        self.nodal_stations.append(Station)
        self.RZ._add_station(Station)
        
        
    def set_demand(self, demand):
        """ Set the nodal demand to a non default value """
        self.demand = demand
        
        
    def add_intload(self, Load):
        """ Add an interuptible load provider to the node"""
        self.intload.append(Load)
        self.RZ._add_intload(Load)
        
        
    def add_price(self, price):
        """ Get the price from the Solver and calculated the cost of load at
        the node
        """
        self.price = price
        self.calculate_load_cost()
        
        
    def calculate_load_cost(self):
        """ Calculate the total cost of serving load at the node """
        self.load_cost = self.demand * self.price
        
class Branch:
    """
    Branch
    ------
    
    Class which is used to define the transmission between two particular
    nodes in the grid with automated support for declaring it a risk, naming it
    and determining piece wise linear losses from a loss factor and the total
    capacity.
    """

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
        """ Create a band structure and determine the piece wise linear loss
        factors for each band
        
        This is currently not needed but will eventually be used to incorporate
        losses into the pyspd model.
        
        """
        
        for band in xrange(bands):
            b = str(band + 1)
            band_name = '_'.join([self.name, b])
            
            self.bands.append(band_name)
            
            self.bc[band_name] = self.capacity / bands * 1.0
            self.blf[band_name] = 2 * (band + 0.5) * self.bc[band_name] * self.lf
            
            
    def add_flow(self, flow):
        """ Add the dispatched flow to the branch """
        self.flow = flow
        
        
        
class ReserveZone:
    """
    ReserveZone
    -----------
    A unique reserve zone for which an individual risk is determined
    as well as an individual price for different dispatched units.
    """
    
    def __init__(self, name, ISO):
        self.name = name
        self.nodes = []
        ISO._add_reserve_zone(self)
        self.stations = []
        self.intload = []
        self.price = 0
    
    def _add_node(self, node):
        """ Add a node to a particular reserve zone """
        self.nodes.append(node)
        
    def _add_station(self, station):
        """ Add a station to a particular reserve zone """
        self.stations.append(station)
        
    def _add_intload(self, IL):
        """ Add an IL provider to a particular reserve zone """
        self.intload.append(IL)
        
    
    def add_price(self, price):
        """ Add the reserve price from the dispatch to the Reserve Zone """
        self.price = price
        
        
class InterruptibleLoad:
    """
    InterruptibleLoad
    -----------------
    An interruptible load copany is one who is capable of providing reserve
    and is not associated with an individual generation plant.
    
    To do
    -----
    Add support for making sure a units load is greater than the IL provided.
    """

    def __init__(self, name, node, ISO, Company, capacity=0):
        self.name = name
        self.node = node
        self.capacity=0
        
        
        node.add_intload(self)
        ISO._add_intload(self)
        Company.add_intload(self)
        
        self.band_names = []
        self.band_prices = {}
        self.band_offers = {}
        
    
    def add_offer(self, band='0', price=0, offer=0):
        """ Add an offer to the company consisting of a band name, price 
            and offer
        """
        name = '_'.join([self.name, band])
        self.band_names.append(name)
        self.band_prices[name] = price
        self.band_offers[name] = offer
        
    def add_multiple_offers(self, offer_dict):
        """ Helper to add multiple offers at once for a station.
            Must be passed a tuple of dictionaries which are then iterated over.
        """
        for row in offer_dict:
            self.add_offer(**row)   
            
            
    def add_res_dispatch(self, dispatch):
        """ Get the reserve dispatch from the Solver and calculate the
            reserve revenue
        """
        self.reserve_dispatch = dispatch 
        self.calculate_reserve_revenue()
        
    def calculate_reserve_revenue(self):
        """ Calculate the reserve revenue from the dispatch """
        self.reserve_revenue = self.reserve_dispatch * self.node.RZ.price    
    
    
class Company:
    """
    Company
    -------
    
    Company master class, consists of a number of stations which may be spread
    across a variety of nodes.
    
    Contains methods for calculating total revenue, total dispatch,
    nodal dispatch, nodal revenue etc.
    
    """

    def __init__(self, name):
        self.name = name
        self.stations = []
        self.intload = []
        self.company_revenue = 0
        
    def add_station(self, Station):
        """ Add a generation station to the company """
        self.stations.append(Station)
        
    def add_intload(self, IL):
        """ Add an interruptible load unit to the company """
        self.intload.append(IL)
        
    def calculate_company_revenue(self):
        """ Calculate the total revenue for a company from its stations and
        IL units. Iterates over all of them and sums them together.
        """
        self.company_revenue = (sum([s.total_revenue for s in self.stations]) +
                                sum([s.reserve_revenue for s in self.intload]))
        
        
if __name__ == '__main__':
    pass 
    
