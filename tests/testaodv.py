#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.getcwd())

from adhoccomputing.Generics import *
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel

from aodv.models import AODVNode, AODVLayer
from aodv.msgs_old import MessageTypes, RREQ_Broadcast_Head, RREQ_Broadcast_Data

import networkx as nx

# Wrap Snapshot in a node model!

def main():
    setAHCLogLevel(DEBUG)
    topo = Topology()

    # randomly generate a topology
    graph = nx.random_graphs.random_regular_graph(3, 10, seed=42)
    topo.construct_from_graph(graph, AODVLayer, GenericChannel)

    sender, receiver = 0, 3 # we know they are neighbors

    head = RREQ_Broadcast_Head(sender, receiver)
    data = GenericMessagePayload(messagepayload="Hello from test environment!")
    event = Event(topo.nodes[sender], EventTypes.MFRT, GenericMessage(head, data))
    topo.nodes[0].on_init(None)
    topo.nodes[3].on_init(None)
    topo.nodes[sender].on_rreq(event)
    
    ## topo.nodes[sender].send_self(Event(topo.nodes[sender], EventTypes.AODVMSG, (MessageTypes.RREQ, receiver)))
    # topo.start()
    time.sleep(5)
    topo.exit()


if __name__ == "__main__":
    exit(main())