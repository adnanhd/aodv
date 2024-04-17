"""
Implementation of the "Ad hoc On-Demand Distance Vector Routing" 
described in the ACM 2nd IEEE Workshop on Mobile Computing Systems 
and Applications in February 1999 by Charles Perkins (Sun Microsystems)
and Elizabeth Royer (now Elizabeth Belding) (University of California, 
Santa Barbara).
"""


__author__ = "Adnan Harun Dogan"
__contact__ = "adnanharundogan@gmail.com"
__copyright__ = "Copyright 2024, WINSLAB"
__credits__ = ["Adnan Harun Dogan"]
__date__ = "2024-04-17"
__deprecated__ = False
__email__ = "adnanharundogan@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"


from dataclasses import dataclass, field

from adhoccomputing.Experimentation.Topology import Event
from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, GenericMessage, ConnectorTypes

from .msgs import RREQ_Head, RREQ_Data
from .msgs import RREP_Head, RREP_Data


@dataclass
class AODVLayer(GenericModel):
    routing_table : dict = field(default_factory=dict)



@dataclass
class MobileNode(GenericModel):
    prev_node_idx : int = -1  
    next_node_idx : int = -1

    def send_rreq(self, target_node_idx):
        # broeadcast RREQ to all neighbors
        self.send_self(Event(self, "RREQ", None))
        # init an event
        rreq_head = RREQ_Head()
        rreq_data = RREQ_Data()
        msg = GenericMessage(rreq_head, rreq_data)
        self.topology.neig


    
    def send_rrep(self, target_node_idx):
        # broeadcast RREP to all neighbors
        pass