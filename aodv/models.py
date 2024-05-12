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
from adhoccomputing.GenericModel import GenericModel, Topology, EventTypes
from adhoccomputing.Generics import Event, GenericMessage, ConnectorTypes

from .msgs import RREQ_Broadcast_Head, RREQ_Broadcast_Data
from .msgs import RREP_Broadcast_Head, RREP_Broadcast_Data
from .msgs import MessageTypes


NULL_NODE_IDX = -1


class AODVNode(GenericModel):
    def __init__(self, componentname, componentid, *args, **kwargs):
        super().__init__(componentname, componentid, *args, **kwargs)
        self.aodvservice = AODVLayer("AODVLayer", componentid)
        # CONNECTIONS AMONG SUBCOMPONENTS
        self.connect_me_to_component(ConnectorTypes.DOWN, self.aodvservice)
        self.aodvservice.connect_me_to_component(ConnectorTypes.UP, self)

    def on_message_from_top(self, eventobj: Event):
        self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

    def on_message_from_bottom(self, eventobj: Event):
        self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

    def send_rreq(self, target_node_idx):
        # broeadcast RREQ to all neighbors
        # init an event
        rreq_head = RREQ_Broadcast_Head(
            MessageTypes.RREQ, self.componentinstancenumber, target_node_idx)

        import pdb
        pdb.set_trace()
        rreq_data = RREQ_Broadcast_Data(src_seq=self.componentinstancenumber,  # degisecek
                              src_addr=self.componentinstancenumber,
                              hop_count=0, rreq_id='unique_id',
                              dest_addr=target_node_idx,
                              dest_seq=target_node_idx)  # degisecek
        msg = GenericMessage(rreq_head, rreq_data)
        self.send_down(Event(self, EventTypes.MFRT, (MessageTypes.RREQ, msg)))

    def send_rrep(self, target_node_idx):
        # broeadcast RREP to all neighbors
        pass


class AODVLayer(GenericModel):
    # routing_table: dict = field(default_factory=dict)

    def __init__(self, componentname, componentid, *args, **kwargs):
        super().__init__(componentname, componentid, *args, **kwargs)
        self.eventhandlers[MessageTypes.RREQ] = [self.on_rreq]  # RREQ
        self.eventhandlers[MessageTypes.RREP] = [self.on_rrep]  # RREP
        self.eventhandlers[MessageTypes.RERR] = [self.on_rerr]  # RERR
        self.eventhandlers[MessageTypes.DATA] = [self.on_data]  # DATA
        # init routing table
        self.routing_table: dict = {}

    def on_init(self, eventobj: Event):
        pass

    def on_rreq(self, eventobj: Event):
        # handle RREQ messages
        app_msg = eventobj.eventcontent
        dest = app_msg.payload.dest_addr

    def on_rrep(self, eventobj: Event):
        # handle RREP messages
        pass

    def on_rerr(self, eventobj: Event):
        # handle RERR messages
        pass

    def on_data(self, eventobj: Event):
        # handle RERR messages
        pass

    def get_next_hop(self, target_node_idx):
        # get next hop for the target node
        try:
            return self.routing_table[target_node_idx]['next_hop']
        except (KeyError, IndexError):
            return NULL_NODE_IDX
        
    def get_next_hop_count(self, target_node_idx):
        # get next hop for the target node
        try:
            return self.routing_table[target_node_idx]['hop_count']
        except (KeyError, IndexError):
            return float('inf')
        
    def update_routing_table(self, target_node_idx, next_hop, hop_count):
        try:
            curr_hop_cnt = self.routing_table[target_node_idx]['hop_count']
        except (KeyError, IndexError):
            curr_hop_cnt = float('inf')

        if hop_count < curr_hop_cnt:
            # update routing table
            self.routing_table[target_node_idx] = {
                'next_hop': next_hop,
                'hop_count': hop_count
            }

    def on_message_from_top(self, eventobj: Event):
        # handle messages from upper layer
        import pdb; pdb.set_trace()

    def on_message_from_bottom(self, eventobj: Event):
        # handle messages from lower layer
        pass
