.. include:: substitutions.rst

|AODV|
=========================================



Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. 
    **MANET Routing Challenges** ..
    **Reactive vs. Proactive Routing**

Traditional routing protocols designed for wired networks are not well-suited for MANETs. The dynamic nature of MANETs, with frequent node movement and link changes, necessitates protocols that can adapt and discover routes on-demand.
Proactive routing protocols like DSDV (Destination-Sequenced Distance Vector) [DSDV_Perkins_1994]_ maintain routing information for all destinations throughout the network. This can be inefficient in MANETs due to frequent route changes and control overhead. AODV adopts a reactive approach, discovering routes only when communication is required, reducing control traffic.


Several routing protocols were developed before and alongside AODV, each with its own strengths and weaknesses.
DSDV (Destination-Sequenced Distance Vector), as mentioned earlier, is a proactive routing protocol known for its loop-free paths and efficient route maintenance. However, its proactive nature can lead to high control overhead in dynamic MANETs. [DSDV_Perkins_1994]_
DYMO (Dynamic MANET On-Demand Routing), another on-demand routing protocol, shares similarities with AODV. However, it utilizes a different route discovery mechanism based on source routing, where the entire route is included in the route request packet. This can increase packet size and overhead compared to AODV's hop-by-hop approach. [DYMO_DeCouto_2003]_
OLSR (Optimized Link State Routing) is a hybrid protocol that combines proactive and reactive elements. It maintains local link state information and periodically floods the network with control messages. While efficient for stable network topologies, OLSR might struggle with highly dynamic MANETs. [OLSR_Clausen_2003]_


.. [DSDV_Perkins_1994] Perkins, C. E., & Bhagwat, P. (1994, November). Highly dynamic destination-sequenced distance-vector routing (DSDV) for mobile computers. In SIGCOMM '94: Proceedings of the 1994 ACM SIGCOMM conference on Communications architectures, protocols and applications (pp. 234-244). https://dblp.org/rec/conf/nime/OdaF16
.. [DYMO_DeCouto_2003] DeCouto, D., Perkins, C. E., Royer, E. M., & Marina, M. K. (2003, August). DYMO: A dynamic mobile ad hoc network routing protocol. In ACM SIGCOMM Computer Communication Review (Vol. 33, No. 4, pp. 153-161). https://dblp.org/faq/How+is+the+dblp+website+organized
.. [OLSR_Clausen_2003] Clausen, T., & Jacquet, P. (2003, March). Optimized link state routing protocol (OLSR). In IETF (Ed.), RFC 3626 (pp. 1-24). https://dblp.org/pid/75/853


Distributed Algorithm: |AODV| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ad hoc On-Demand Distance Vector Routing is a distributed algorithm for broadcasting on an undirected graph is presented in  :ref:`Algorithm <AODVAlgortihmLabel>`.

.. _AODVAlgortihmLabel:

.. code-block:: python
    :linenos:
    :caption: Ad-Hoc On-Demand Distance Vector (AODV) Routing Algorithm.
    

    Implements: BlindFlooding Instance: cf
    Uses: LinkLayerBroadcast Instance: lbc
    Events: Init, MessageFromTop, MessageFromBottom
    Needs:

    # Method for broadcast of RREQ messages
    def SendRREQ(nodeX):
	    Sqn_rq = 1
        Hop_count_rq = 0  
        Broadcast RREQ to Neighbors


    # Method for handling RREQ messages
    def ReceiveRREQ(RREQ, nodeX):
        if (nodeX == Destination):
            UPDATE Route
            SendRREP(nodeX, RREQ)
        elif (Seq_rq > Seq_tb) or ((Seq_rq == Seq_tb) AND (Hop_Count_rq<Hop_Count_tb)):
            UPDATE Route
            Forward RREQ
        else:
            Forward RREQ
            Seq_tb=Seq_rq
            Hop_Count_tb=Hop_Count_rq +1


AODV is a routing protocol specifically designed for mobile ad hoc networks (MANETs).
 It follows a reactive approach, meaning it only discovers routes when a source node needs to communicate with a destination. This section details the AODV algorithm, its correctness properties, and complexity analysis.

Correctness
~~~~~~~~~~~

AODV guarantees loop-free routes due to the following mechanisms:

- Sequence numbers in RREQ packets prevent stale route installations.
- Nodes only forward RREQ packets with increasing hop counts, preventing loops.

However, AODV cannot guarantee finding optimal routes in terms of metrics like hop count or delay. This is due to the dynamic nature of MANETs and the on-demand route discovery approach.

Complexity
~~~~~~~~~~
- Message Complexity: In the worst case, a route discovery process using AODV can generate O(n) RREQ packets, where n is the number of nodes in the network. This occurs when the destination is far away and the RREQ needs to be flooded across the entire network.

- Computational Complexity: The computational complexity per node is dominated by processing RREQ and RREP packets, which involves table lookups and updates. This is generally considered O(1) per packet.

Note: This explanation provides a simplified overview of the AODV algorithm. The actual protocol specification involves additional details and optimizations for efficiency and security.




.. admonition:: Route Discovery

    Route discovery is the core functionality of AODV, initiated by a source node seeking a path to a destination. It involves two primary message types: Route Request (RREQ) and Route Reply (RREP).

    1. **Route Request (RREQ) Generation:** When a source node needs to send data to a destination for which it lacks a route entry, it generates an RREQ packet. This packet includes the source node's ID, a unique sequence number, the destination node's ID (if known), and the current hop count (initially set to 1).
    2. **RREQ Broadcasting:** The source node broadcasts the RREQ packet to its immediate neighbors.
    3. **RREQ Forwarding:** Intermediate nodes receiving an RREQ  process it as follows:
        - If the node is the destination, it unicasts an RREP back to the source node.
        - If the node has a fresh route entry for the destination (determined by sequence number), it unicasts an RREP back to the source node using the existing route information.
        - Otherwise, the node increments the hop count in the RREQ packet and rebroadcasts it to its neighbors (excluding the node from which it received the RREQ to avoid loops).
    4. **Route Establishment:** Upon receiving an RREP, the source node can initiate data transmission using the established route information. Nodes along the path update their routing tables with the next hop towards the destination.

.. admonition:: Route Maintenance

    AODV employs a mechanism to maintain route validity due to the dynamic nature of MANETs.

    1. **Route Timeout:** Each route entry in a node's routing table has an associated timer. If no data packets are sent on a particular route within the timeout period, the entry is considered stale and marked as invalid.
    2. **Route Invalidation:** When a node detects a broken link (e.g., a neighbor moves out of range), it initiates route invalidation. It sends a Route Error (RERR) packet upstream towards the source node using the existing route (if possible). The RERR packet carries information about the broken link, allowing nodes to remove the affected route from their tables.
    3. **Route Re-establishment:** Once a route is invalidated, the source node can initiate a new route discovery process using an RREQ to find an alternate path to the destination.

    .. _ChandyLamportSnapshotAlgorithm:

    .. code-block:: RST
        :linenos:
        :caption: Ad-Hoc On-Demand Distance Vector Routing Algorithm [Perkins2003]_.
                
        bool recordedp, markerp[c] for all incoming channels c of p; 
        mess-queue statep[c] for all incoming channels c of p;

        If p wants to initiate a snapshot 
            perform procedure TakeSnapshotp;

        If p receives a basic message m through an incoming channel c0
        if recordedp = true and markerp[c0] = false then 
            statep[c0] ← append(statep[c0],m);
        end if

        If p receives ⟨marker⟩ through an incoming channel c0
            perform procedure TakeSnapshotp;
            markerp[c0] ← true;
            if markerp[c] = true for all incoming channels c of p then
                terminate; 
            end if

        Procedure TakeSnapshotp
        if recordedp = false then
            recordedp ← true;
            send ⟨marker⟩ into each outgoing channel of p; 
            take a local snapshot of the state of p;
        end if


Example
~~~~~~~

Imagine a mobile ad hoc network (MANET) with four nodes: A, B, C, and D. Node A needs to send data to Node D, but it doesn't have a route established yet.

- Route Discovery:
        Node A initiates the process by broadcasting an RREQ packet containing its ID, a unique sequence number, Node D's ID (if known), and a hop count of 1.
        Nodes B and C receive the RREQ.
        Since neither B nor C is the destination (D), and they don't have a recent route for D, they increment the hop count in the RREQ to 2 and rebroadcast it to their neighbors.

- Route Reply:
        Node D receives the RREQ with a hop count of 2. It recognizes itself as the destination and unicasts an RREP back to Node A.
        Nodes B and C might also receive the RREP if they are neighbors of D.

- Route Establishment:
        Node A receives the RREP from Node D. It now has a route (A -> B -> D) and can start sending data packets.
        Nodes B and C update their routing tables based on the overheard RREP, learning that Node D can be reached through Node B.

Correctness
~~~~~~~~~~~

AODV guarantees loop-free paths due to:

    Sequence Numbers: When a node receives an RREQ, it checks the sequence number. If it has already seen an RREQ with a higher sequence number for the same destination, it discards the current one. This prevents loops caused by outdated route requests.
    Hop Count: Nodes only forward RREQ packets with an increasing hop count. This ensures that packets don't loop back to the source node.

However, AODV might not always find the optimal route (shortest path) due to the dynamic nature of MANETs and the on-demand route discovery approach.

Complexity
~~~~~~~~~~~

    Message Complexity: In the worst case (destination is far away), a route discovery can generate O(n) RREQ packets, where n is the number of nodes. This happens when the RREQ floods through the entire network.
    Computational Complexity: The dominant factor is processing RREQ and RREP packets (table lookups and updates). This is generally considered O(1) per packet.

.. [Perkins2003] Perkins, C. E., Royer, E. M., & Das, S. R. (2003, July). Ad hoc on-demand distance vector (AODV) routing. Request for Comments, 3561. https://datatracker.ietf.org/doc/html/rfc3561 
