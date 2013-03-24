import numpy as np
from collections import defaultdict

class ISO:
    """ 
    Independent System Operator
    ---------------------------
    Contains all of the information necessary to pass to the solver in order
    to create the grid dispatch
    """
    
    def __init__(self, name):
        self.name = name
        self.initialise_empty()
        
        self.stations = []
        self.spinning_stations = []
        
        self.nodes = []
        self.branches = []
        
    def initialise_empty(self):
        """ Initialise an empty dispatch """
        
        self.energy_bands = []
        self.reserve_bands = []
        self.transmission_bands = []
        self.all_nodes = []
        
        self.energy_totals = []
        self.reserve_totals = []
        self.transmission_totals = []
        
        self.energy_band_map = defaultdict(list)
        self.reserve_band_map = defaultdict(list)
        self.transmission_band_map = defaultdict(list)
        
        self.energy_band_prices = {}
        self.reserve_band_prices = {}
        
        self.energy_band_maximum = {}
        self.reserve_band_maximum = {}
        self.transmission_band_maximum = {}
        
        self.energy_total_maximum = {}
        self.transmission_total_maximum = {}
        self.reserve_band_proportion = {}
        
        self.spinning_stations = []
        self.spin_map = {}
        
        self.node_energy_map = defaultdict(list)
        self.node_demand = {}
        
        self.node_t_map = defaultdict(list)
        self.node_transmission_direction = defaultdict(dict)
        
        self.reserve_zones = []
        self.reserve_zone_generators = defaultdict(list)
        self.reserve_zone_transmission = defaultdict(list)
        
        
    def create_offers(self):
        """ Create a full offer for dispatch """
        
        
    def get_offers(self):
        for station in self.stations:
            pass
            
        
    
    def _add_station(self, station):
        """ Add a generation station to the ISO """
        self.stations.append(station)
        if station.spinning == True:
            self.spinning_stations.append(station)
        
        
    def _add_node(self, node):
        self.nodes.append(node)
        
    
    def _add_branch(self, branch):
        self.branches.append(branch)
        
        
        
        
    def     
