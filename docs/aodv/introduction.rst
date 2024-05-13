.. include:: substitutions.rst

Introduction
============

This section addresses the challenge of inefficient routing in dynamic mobile ad-hoc networks (MANETs).
MANETs are characterized by frequent node movement and link changes, rendering traditional routing protocols 
designed for static networks unsuitable. Here, we explore the limitations of these protocols and the need 
for an alternative approach specifically tailored for the dynamic nature of MANETs. Here are some key terms that
you will be encountering throughout the report:

* **Mobile Ad-Hoc Network (MANET)**: A temporary network formed by mobile devices without a central infrastructure.
* **Routing Protocol**: A set of rules that devices use to determine the path for data packets across a network.
* **Proactive Routing**: A routing protocol where nodes maintain routing information for all destinations continuously.
* **Reactive Routing**: A routing protocol where nodes only discover routes when communication with a specific destination is needed.

The Problem
-----------

Mobile ad-hoc networks (MANETs) are dynamic environments where devices connect and disconnect 
frequently, and network connections constantly change. Traditional routing protocols designed 
for static networks struggle in this scenario. Establishing and maintaining efficient routes 
for communication between nodes in a MANET is a critical challenge. 

The constant changes in network topology within a MANET pose a significant challenge to 
traditional routing protocols. These protocols typically rely on a proactive approach,
where each node maintains routing information for all possible destinations. In a static network,
this strategy works well. However, in a MANET, the dynamic nature of the environment leads
to several issues:

* **Frequent Route Updates**: Due to node movement and link changes, routing tables require constant updates to maintain accurate information. This generates a significant amount of control overhead, wasting valuable bandwidth and battery power on mobile devices.
* **Stale Routing Information**: Frequent updates might not keep pace with the rapid changes in network topology. This can lead to routing tables containing outdated information, resulting in dropped or delayed data packets when directed to unreachable nodes.
* **Inefficient Resource Usage**: Proactive routing protocols constantly exchanging routing updates can drain the limited resources (battery power, bandwidth) of mobile devices in a MANET.

Importance and Significance
---------------------------

Efficient routing in MANETs unlocks a wide range of applications. These include:

* Sensor networks for environmental monitoring and disaster relief.
* Mobile communication in remote areas without fixed infrastructure.
* Collaborative computing among mobile devices.

Without effective routing, communication in these scenarios becomes unreliable or impossible. 
Delays and disruptions can severely limit the functionality and usefulness of MANETs.

The Challenge
-------------

The dynamic nature of MANETs makes routing difficult. Traditional static routing protocols 
cannot adapt to frequent changes in network topology. Naive approaches that continuously flood 
the network with route updates are inefficient and lead to excessive overhead.

Limitations of Existing Solutions
---------------------------------

Existing routing protocols for MANETs often have limitations. Some may be slow to adapt to 
network changes, leading to outdated routes and communication failures. Others might require 
nodes to maintain routes to all destinations, even those not actively communicating, wasting 
resources.

The AODV Approach and Key Features
----------------------------------

The Ad hoc On-Demand Distance Vector (AODV) routing algorithm addresses these challenges. It 
utilizes a **reactive approach**, discovering routes only when a source node needs to communicate 
with a specific destination. This conserves resources compared to proactive methods.

AODV employs destination sequence numbers to ensure **loop-free operation** and route freshness. 
Nodes choose routes with the highest sequence numbers, guaranteeing the latest and most reliable 
paths. This approach offers quick route acquisition, efficient adaptation to network changes, and 
avoids the "*counting to infinity*" problem seen in traditional distance vector protocols.

However, it's important to acknowledge that AODV might incur a slight delay in **route discovery** 
for the first communication with a new destination. This is a trade-off for the efficiency gains 
in a dynamic environment.

In conclusion, AODV provides a robust and efficient solution for routing in MANETs by adapting 
to network changes, conserving resources, and ensuring reliable communication.

Contributions
-------------

Authors' [Perkins2003]_ primary contributions consist of the following:

- **On-demand route discovery**: Minimizes wasted overhead by only finding routes when communication is needed.
- **Quick route acquisition**: Enables rapid establishment of new routes for efficient data transfer.
- **Loop-free operation with destination sequence numbers**: Ensures reliable paths and avoids routing loops in a simple and efficient way.
- **Fast adaptation to network changes**: Responds effectively to link breakages and network topology shifts.
- **Resource efficiency**: Avoids maintaining unnecessary routes, saving battery life and bandwidth in mobile devices.

..
    If you would like to get a good grade for your project, you have to write a good report.  Your project will be assessed mostly based on the report. Examiners are not mind-readers, and cannot give credit for work which you have done but not included in the report [York2017]_.

    Here is the Stanford InfoLab's patented five-point structure for Introductions. Unless there's a good argument against it, the Introduction should consist of five paragraphs answering the following five questions:

    - What is the problem?
    - Why is it interesting and important? What do you gain when you solve the problem, and what do you miss if you do not solve it?
    - Why is it hard? (e.g., why do naive approaches fail?)
    - Why hasn't it been solved before? What's wrong with previous proposed solutions? How does yours differ?
    - What are the key components of your approach and results including any specific limitations.

    Then have a penultimate paragraph or subsection: "Contributions". It should list the major contributions in bullet form, mentioning in which sections they can be found. This material doubles as an outline of the rest of the paper, saving space and eliminating redundancy.

    .. [York2017]  York University. (2017) How to write a project report.



    .. admonition:: EXAMPLE 

        In the realm of snapshot algorithms for distributed systems, the fundamental problem lies in capturing a consistent global state without interrupting the ongoing execution of processes and avoiding excessive overhead. The challenges involve managing concurrency, ensuring accurate message ordering, providing fault tolerance to handle process failures, optimizing efficiency to minimize computational and communication overhead, and maintaining scalability as the system expands. Successfully addressing these challenges is crucial for designing snapshot algorithms that accurately reflect the distributed system's dynamic state while preserving efficiency and resilience.,
        
        Snapshot algorithms are both interesting and important due to their pivotal role in understanding, managing, and troubleshooting distributed systems. Solving the problem of capturing consistent global states in a distributed environment offers several significant benefits. Firstly, it provides invaluable insights into the system's behavior, facilitating tasks such as debugging, performance analysis, and identifying issues like deadlocks or message race conditions. Moreover, snapshot algorithms enable efficient recovery from failures by providing checkpoints that allow systems to resume operation from a known, consistent state. Additionally, they aid in ensuring system correctness by verifying properties like termination or the absence of deadlock. Without solving this problem, distributed systems would lack the capability to effectively diagnose and resolve issues, leading to increased downtime, inefficiencies, and potentially catastrophic failures. The absence of snapshot algorithms would hinder the development, deployment, and management of robust and reliable distributed systems, limiting their usability and scalability in modern computing environments. Thus, addressing this problem is critical for advancing the field of distributed systems and maximizing the reliability and efficiency of distributed computing infrastructures.

        Capturing consistent global states in distributed systems poses significant challenges due to their decentralized, asynchronous nature. Naive approaches often fail due to complexities such as concurrency, message ordering, synchronization, fault tolerance, and scalability. Concurrency and ordering issues may lead to inconsistent snapshots, while synchronization difficulties hinder performance. Inadequate fault tolerance can result in incomplete or incorrect snapshots, jeopardizing system recovery and fault diagnosis. Additionally, inefficient approaches may impose excessive overhead, impacting system performance. Overcoming these challenges requires sophisticated algorithms that balance correctness, efficiency, fault tolerance, and scalability, navigating the inherent trade-offs of distributed systems to capture accurate global states without disrupting system operation.

        The persistent challenge of capturing consistent global states in distributed systems, particularly within the context of the Chandy-Lamport Algorithm, arises from the algorithm's inherent complexities and the dynamic nature of distributed environments. While the Chandy-Lamport Algorithm offers a promising approach by utilizing marker propagation to capture snapshots without halting the system's execution, its implementation faces obstacles such as concurrency management, ensuring accurate message ordering, and handling fault tolerance. Previous attempts at solving these challenges with the Chandy-Lamport Algorithm may have been hindered by their complexity, limited scalability, or inability to adapt to changing system conditions. Thus, achieving a comprehensive resolution within the Chandy-Lamport framework requires addressing these concerns through innovative approaches that optimize for correctness, efficiency, fault tolerance, and scalability while considering the evolving requirements of distributed systems.

        The Chandy-Lamport Algorithm is a key method for capturing consistent global snapshots in distributed systems, comprising the initiation of marker propagation, recording of local states by processes upon marker reception, and subsequent snapshot reconstruction. It allows for the capture of snapshots without halting system execution, facilitating concurrent operations and serving various purposes like debugging and failure recovery. However, the algorithm exhibits limitations including increased message overhead due to marker propagation, challenges in managing concurrency which may affect snapshot accuracy, potential difficulties in handling faults during snapshot collection, and scalability concerns as system size grows. Despite these limitations, the Chandy-Lamport Algorithm remains foundational in distributed systems, driving further research in snapshot capture techniques. DETAILS OF Lai-Yang Algorithm.

        Our primary contributions consist of the following:
        
        - Implementation of both the Chandy-Lamport Algorithm and the Lai-Yang Algorithm on the AHCv2 platform. The implementation specifics are detailed in Section XX.
        - Examination of the performance of these algorithms across diverse topologies and usage scenarios. Results from these investigations are outlined in Section XXX.
        - Comprehensive comparison and contrast of the algorithms based on criteria such as accuracy, overhead, complexity, and fault tolerance. Key insights derived from these comparisons are elaborated upon in Section XXXX.