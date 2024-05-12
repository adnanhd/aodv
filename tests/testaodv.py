#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.getcwd())

from adhoccomputing.Generics import *
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel

from aodv.models import AODVNode, AODVLayer
from aodv.msgs import MessageTypes

import networkx as nx

# Wrap Snapshot in a node model!

def main():
    setAHCLogLevel(DEBUG)
    topo = Topology()

    # randomly generate a topology
    graph = nx.random_graphs.random_regular_graph(3, 10)
    topo.construct_from_graph(graph, AODVLayer, GenericChannel)

    sender, receiver = 0, 9

    import pdb; pdb.set_trace()
    topo.nodes[sender].send_rreq(receiver)
    
    topo.nodes[sender].send_self(Event(topo.nodes[sender], EventTypes.AODVMSG, (MessageTypes.RREQ, receiver)))

    time.sleep(5)
    topo.exit()


if __name__ == "__main__":
    exit(main())