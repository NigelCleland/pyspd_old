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
        
        self.node_name_map = {}
        self.reserve_zone_name_map = {}
        self.station_name_map = {}
        self.reserve_name_map = {}
        self.branch_name_map = {}
        
        self.intload = []
        self.intload_names = []
        
    def initialise_empty(self):
        """ Initialise an empty dispatch """
        
        self.energy_bands = [] # Done
        self.reserve_bands = [] # Done
        self.transmission_bands = [] # Done
        self.all_nodes = [] # Done
        
        self.energy_totals = [] # Done
        self.reserve_totals = [] # Done
        self.transmission_totals = [] # Done
        
        self.energy_band_map = defaultdict(list) # Done
        self.reserve_band_map = defaultdict(list) # Done
        self.transmission_band_map = defaultdict(list) # Done
        
        self.energy_band_prices = {} # Done
        self.reserve_band_prices = {} # Done
        
        self.energy_band_maximum = {} # Done
        self.reserve_band_maximum = {} # Done
        self.transmission_band_maximum = {} # Done
        
        self.energy_total_maximum = {} # Done
        self.transmission_total_maximum = {} # Done
        self.reserve_band_proportion = {} # Done
        self.transmission_band_loss_factor = {} # Done
        
        self.spinning_stations = [] # Done
        self.spinning_station_names = [] # Done
        self.spin_map = defaultdict(list) # Done
        
        self.node_energy_map = defaultdict(list) # Done
        self.node_demand = {} # Done
        
        self.node_t_map = defaultdict(list) # Done
        self.node_transmission_direction = defaultdict(dict) # Done
        
        self.reserve_zones = [] # Done
        self.reserve_zone_names = [] # Done
        self.reserve_zone_generators = defaultdict(list) # Done
        self.reserve_zone_transmission = defaultdict(list) # Done
        
        self.reserve_zone_reserve = defaultdict(list) # Done
        
        
    def create_offers(self):
        """ Create a full offer for dispatch """
        #self.initialise_empty()
        self.get_nodal_demand()
        self.get_energy_offers()
        self.get_reserve_offers()
        self.get_network()
        
        
    def get_nodal_demand(self):
        for node in self.nodes:
            self.all_nodes.append(node.name)
            self.node_demand[node.name] = node.demand
            for station in node.nodal_stations:
                self.node_energy_map[node.name].append(station.name)
            
        
        
    def get_energy_offers(self):
        for station in self.stations:
            self.energy_totals.append(station.name)
            self.energy_total_maximum[station.name] = station.capacity
            
            for band in station.band_names:
                self.energy_bands.append(band)
                self.energy_band_prices[band] = station.band_prices[band]
                self.energy_band_maximum[band] = station.band_offers[band]
                self.energy_band_map[station.name].append(band)
                
            if station.spinning == True:
                self.spinning_station_names.append(station.name)
                    
                    
    def get_reserve_offers(self):
        for station in self.spinning_stations:
            self.reserve_totals.append(station.name)
            
            
            for band in station.rband_names:
                self.reserve_bands.append(band)
                self.reserve_band_prices[band] = station.rband_prices[band]
                self.reserve_band_maximum[band] = station.rband_offers[band]
                self.reserve_band_proportion[band] = station.rband_proportions[band]
            
                self.reserve_band_map[station.name].append(band)
                self.spin_map[station.name].append(band)
                
        for il in self.intload:
            self.reserve_totals.append(il.name)
            
            for band in il.band_names:
                self.reserve_bands.append(band)
                self.reserve_band_prices[band] = il.band_prices[band]
                self.reserve_band_maximum[band] = il.band_offers[band]
                self.reserve_band_map[il.name].append(band)
                
                
        for RZ in self.reserve_zones:
            for station in RZ.stations:
                self.reserve_zone_generators[RZ.name].append(station.name)
                self.reserve_zone_reserve[RZ.name].append(station.name)
                
            for il in RZ.intload:
                self.reserve_zone_reserve[RZ.name].append(il.name)
                
            
    def get_network(self):
        for branch in self.branches:
            self.transmission_totals.append(branch.name)
            self.transmission_total_maximum[branch.name] = branch.capacity

            # Node names for adding
            snN = branch.sending_node.name
            rnN = branch.receiving_node.name            
            # Add nodes
            self.node_t_map[snN].append(branch.name)
            self.node_t_map[rnN].append(branch.name)
            
            # Add Transmission directions

            self.node_transmission_direction[snN][branch.name] = 1
            self.node_transmission_direction[rnN][branch.name] = -1
            
            # Add Reserve Zones for flows
            if branch.risk == True:
                # To reduce line length...
                snRZ = branch.sending_node.RZ.name
                rnRZ = branch.receiving_node.RZ.name
                self.reserve_zone_transmission[snRZ].append(branch.name)
                self.reserve_zone_transmission[rnRZ].append(branch.name)
            
            
            for band in branch.bands:
                self.transmission_bands.append(band)
                self.transmission_band_maximum[band] = branch.bc[band]
                self.transmission_band_loss_factor[band] = branch.blf[band]
                self.transmission_band_map[branch.name].append(band)
                
                
    def pretty_print(self):
        """ Pretty Printing of the solved dispatch including for analysis """
        print "---------------------------------------------------------------"
        print "--------------- Beginning Dispatch Results --------------------"
        print "---------------------------------------------------------------"
        print "--------------- Energy Prices ---------------------------------"
        print "----- Node ----- Price ----------------------------------------"
        for node in self.nodes:
            print "    | %s |   $%0.2f/MWh | " % (node.name[:4], node.price)
        print "--------------- Reserve Prices --------------------------------"
        print "----- RZone ----- Price ---------------------------------------"
        for rzone in self.reserve_zones:
            print "    | %s |   $%0.2f/MWh | " % (rzone.name[:5], rzone.price)
        print "--------------- Energy Dispatch -------------------------------"
        print "----- Station ----- Dispatch ----- Revenue --------------------"
        for station in self.stations:
            print "    | %s |   %0.2f MW |  $%0.2f |" % (station.name[:5], 
                                                  abs(station.energy_dispatch),
                                                  abs(station.energy_revenue))
        print "--------------- Reserve Dispatch ------------------------------"
        print "----- Station ----- Dispatch ----- Revenue --------------------"
                
        
        
    
    def _add_station(self, station):
        """ Add a generation station to the ISO """
        self.stations.append(station)
        self.station_name_map[station.name] = station
        if station.spinning:
            self.spinning_stations.append(station)
            self.reserve_name_map[station.name] = station
        
        
    def _add_node(self, node):
        self.nodes.append(node)
        self.node_name_map[node.name] = node
        
    
    def _add_branch(self, branch):
        self.branches.append(branch)
        self.branch_name_map[branch.name] = branch
        
        
    def _add_reserve_zone(self, RZ):
        self.reserve_zones.append(RZ)
        self.reserve_zone_names.append(RZ.name)
        self.reserve_zone_name_map[RZ.name] = RZ
        
    
    def _add_intload(self, Load):
        self.intload.append(Load)
        self.intload_names.append(Load)
        self.reserve_name_map[Load.name] = Load
        
        
if __name__ == '__main__':
    pass
