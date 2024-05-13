#!/usr/bin/env python3
import networkx as nx
import os
import sys

sys.path.insert(0, os.getcwd())

from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Generics import *

from aodv.aodv import AODVNode, AODVLayerMessageType, AODVBroadcastingMessageHeader, AODVBroadcastingMessagePayload


def main():
    setAHCLogLevel(DEBUG)
    topo = Topology()

    # randomly generate a topology
    graph = nx.random_graphs.random_regular_graph(3, 10, seed=42)
    topo.construct_from_graph(graph, AODVNode, GenericChannel)

    sender, receiver = 0, 9
    import pdb
    for i in range(10):
        topo.nodes[i].aodvservice.on_init(None)
        # topo.nodes[i].aodvservice.update_topology()
    head = AODVBroadcastingMessageHeader(AODVLayerMessageType.RREQ, sender, receiver)
    data = AODVBroadcastingMessagePayload([])
    event = Event(topo.nodes[sender], EventTypes.MFRT, GenericMessage(head, data))
    
    topo.nodes[sender].aodvservice.on_rreq(event)
    # topo.nodes[sender].send_self(Event(
    #    topo.nodes[sender], EventTypes.MFRB, (AODVLayerMessageType.RREQ, receiver)))

    time.sleep(5)
    topo.exit()


if __name__ == "__main__":
    exit(main())
