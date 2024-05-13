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

from adhoccomputing.Experimentation.Topology import Event, MessageDestinationIdentifiers
from adhoccomputing.GenericModel import GenericModel, Topology, EventTypes
from threading import Lock
from adhoccomputing.Generics import Event, GenericMessage, ConnectorTypes, GenericMessageHeader

from .msgs_old import RREQ_Broadcast_Head, RREQ_Broadcast_Data, RREP_Broadcast_Head, RREP_Broadcast_Data, MessageTypes


NULL_NODE_IDX = -1
import pdb


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
        self.eventhandlers[MessageTypes.RREQ] = self.on_rreq  # RREQ
        self.eventhandlers[MessageTypes.RREP] = self.on_rrep  # RREP
        self.eventhandlers[MessageTypes.RERR] = self.on_rerr  # RERR
        self.eventhandlers[MessageTypes.DATA] = self.on_data  # DATA
        # init routing table
        self.routing_table: dict = {
            componentid: dict(destination=componentid,
                              next_hop=componentid,
                              hop_count=0, destinationSequenceNumber=0)
        }
        self.lock = Lock()

    def on_init(self, eventobj: Event):
        self.uniquebroadcastidentifier = 1

    def on_rreq(self, eventobj: Event):
        # handle RREQ messages
        msg: GenericMessage = eventobj.eventcontent
        src_idx = msg.header.messagefrom
        dst_idx = msg.header.messageto
        seq_num = msg.header.sequencenumber
        
        self.uniquebroadcastidentifier = self.uniquebroadcastidentifier + 1
        interfaceid = self.uniquebroadcastidentifier
        nexthop = MessageDestinationIdentifiers.LINKLAYERBROADCAST

        hopCount = self.get_next_hop_count(src_idx) + 1

        print('on_rreq', self.componentinstancenumber, '->', dst_idx, f'[src_idx={src_idx}, dst_idx={dst_idx}, hopCount={hopCount}, seq_num={seq_num}]')

        head = RREQ_Broadcast_Head(messagefrom=self.componentinstancenumber, messageto=dst_idx)
        data = RREQ_Broadcast_Data(src_addr=src_idx, dest_addr=dst_idx, hop_count=hopCount)
        broadcast_msg = GenericMessage(head, data)
        self.send_down(Event(self, EventTypes.MFRT, broadcast_msg))


        # self.send_down(eventobj)
        # pdb.set_trace()

    def on_rrep(self, eventobj: Event):
        # handle RREP messages
        # handle RREQ messages
        header: RREP_Broadcast_Head = eventobj.eventcontent.header
        payload: RREP_Broadcast_Data = eventobj.eventcontent.payload

        next_hop = self.get_next_hop(header.messageto)
        hop_count = self.get_next_hop_count(header.messageto)

        head = RREP_Broadcast_Head(messagefrom=self.componentinstancenumber, messageto=next_hop, nexthop=next_hop)
        data = RREP_Broadcast_Data(hop_count=hop_count, dest_addr=header.messagefrom, dest_seq=payload.dest_seq, src_addr=header.messageto)
        print("on_rrep", self.componentinstancenumber, payload.src_addr, '->', header.messageto)
        self.send_down(Event(self, EventTypes.MFRT, GenericMessage(head, data)))
        # import pdb; pdb.set_trace()

    def on_rerr(self, eventobj: Event):
        # handle RERR messages
        print('on_rerr')
        pdb.set_trace()
        pass

    def on_data(self, eventobj: Event):
        # handle RERR messages
        print('on_data')
        pdb.set_trace()
        pass

    def get_next_hop(self, target_node_idx):
        # get next hop for the target node
        try:
            return self.routing_table[target_node_idx]['next_hop']
        except KeyError:
            return NULL_NODE_IDX

    def get_next_hop_count(self, target_node_idx):
        # get next hop for the target node
        try:
            return self.routing_table[target_node_idx]['hop_count']
        except KeyError:
            return float('inf')

    def update_routing_table(self, target_node_idx, next_hop, hop_count):
        try:
            curr_hop_cnt = self.routing_table[target_node_idx]['hop_count']
        except KeyError:
            curr_hop_cnt = float('inf')

        if hop_count < curr_hop_cnt:
            # update routing table
            print(self.componentinstancenumber, 'update_routing_table',  next_hop, '->', target_node_idx, '@', hop_count, 'hops')
            self.routing_table[target_node_idx] = {
                'next_hop': next_hop,
                'hop_count': hop_count
            }

    def on_message_from_top(self, eventobj: Event):
        # handle messages from upper layer
        import pdb
        pdb.set_trace()

    def on_message_from_bottom(self, eventobj: Event):
        # handle messages from lower layer
        broadcast_msg: GenericMessage = eventobj.eventcontent

        broadcast_msg_head: RREQ_Broadcast_Head = broadcast_msg.header
        msg: RREQ_Broadcast_Data = broadcast_msg.payload

        # source = applicationLayerMessageHeader.messagefrom
        prev_idx = broadcast_msg_head.messagefrom
        dest_idx = broadcast_msg_head.messageto
        src_idx = msg.src_addr
        hop_count = msg.hop_count
        
        print("message_from_bottom", self.componentinstancenumber, src_idx, '...', prev_idx, '->', dest_idx, msg.hop_count)
        # sequencenumber = applicationLayerMessageHeader.sequencenumber
        
        if broadcast_msg_head.messagetype == MessageTypes.RREQ:
            # handle RREQ messages
            self.lock.acquire()
            if dest_idx == self.componentinstancenumber:
                # I am the destination
                # send RREP
                print("I am the destination", self.componentinstancenumber, dest_idx, prev_idx)
                head = RREP_Broadcast_Head(messagefrom=self.componentinstancenumber, messageto=prev_idx)
                data = RREP_Broadcast_Data(hop_count=hop_count, dest_addr=src_idx, dest_seq=-1, src_addr=dest_idx)
                # hop_count: int, dest_addr: str, dest_seq: int, src_addr: str
                self.send_self(Event(self, MessageTypes.RREP, GenericMessage(head, data)))
                # print(self.connectors)
            else:
                # I am not the destination
                # forward the RREQ
                self.update_routing_table(src_idx, prev_idx, hop_count)
                pass
            self.lock.release()
        if broadcast_msg_head.messagetype == MessageTypes.RREP:
            # handle RREP messages
            print('I am a response message', self.componentinstancenumber, src_idx, '->', dest_idx)

