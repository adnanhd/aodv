from enum import Enum

from dataclasses import dataclass
from adhoccomputing.GenericModel import GenericMessagePayload, GenericMessageHeader


class MessageTypes(Enum):
    RREQ = 1
    """Route Request Message Format"""

    RREP = 2
    """Route Reply Message Format"""

    RERR = 3
    """Route Error Message Format"""

    DATA = 4
    """Route Reply Acknowledgment Message Format"""


@dataclass
class RREQ_Broadcast_Head(GenericMessageHeader):
    """**Route Request (RREQ) Message Header Format**"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    f_join_multicast: bool = False
    """Join flag; reserved for multicast."""

    f_repair_multicast: bool = False
    """Repair flag; reserved for multicast."""

    f_gratuitous: bool = False
    """Gratuitous RREP flag; indicates whether a
    gratuitous RREP should be unicast to the node
    specified in the Destination IP Address field (see
    sections 6.3, 6.6.3)."""

    f_dest_only: bool = False
    """Destination only flag; indicates only the
    destination may respond to this RREQ (see
    section 6.5)."""

    unk_seq_num: bool = False
    """Unknown sequence number; indicates the destination
    sequence number is unknown (see section 6.3)."""


@dataclass
class RREQ_Broadcast_Data(GenericMessagePayload):
    """**Route Request (RREQ) Message Header Format**"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    hop_count: int
    """The number of hops from the Originator IP Address
    to the node handling the request."""

    rreq_id: int
    """A sequence number uniquely identifying the
    particular RREQ when taken in conjunction with the
    originating node's IP address."""

    dest_addr: str
    """The IP address of the destination for which a route
    is desired."""

    dest_seq: int
    """The latest sequence number received in the past
    by the originator for any route towards the
    destination."""

    src_addr: str
    """The IP address of the node which originated the
    Route Request."""

    src_seq: int
    """The current sequence number to be used in the route
    entry pointing towards the originator of the route
    request."""


@dataclass
class RREP_Broadcast_Head(GenericMessageHeader):
    """**Route Reply (RREP) Message Header Format**"""

    f_repair: bool = False
    """Repair flag; indicates the RREP is part of a
    repair process."""

    f_ack: bool = False
    """Acknowledgement flag; indicates the RREP is an
    acknowledgement for a previously received RREQ."""

    prefix_size: int = 0  # Predecessor node Hop Lifetime (optional)
    """If nonzero, the 5-bit Prefix Size specifies that the
    indicated next hop may be used for any nodes with
    the same routing prefix (as defined by the Prefix
    Size) as the requested destination."""


@dataclass
class RREP_Broadcast_Data(GenericMessagePayload):
    """**Route Reply (RREP) Message Payload Format**"""

    hop_count: int
    """The number of hops from the Originator IP Address
    to the Destination IP Address.  For multicast route
    requests this indicates the number of hops to the
    multicast tree member sending the RREP."""

    dest_addr: str
    """The IP address of the destination for which a route
    is supplied."""

    dest_seq: int
    """The destination sequence number associated to the
    route."""

    src_ip_addr: str
    """The IP address of the node which originated the RREQ
    for which the route is supplied."""

    lifetime: int = 0  # Target node Hop Lifetime (optional)
    """The time in milliseconds for which nodes receiving
    the RREP consider the route to be valid."""


@dataclass
class RERR_Broadcast_Head(GenericMessageHeader):
    """**Route Error (RERR) Message Header Format**"""

    f_no_del: bool = False
    """No delete flag; set when a node has performed a local
    repair of a link, and upstream nodes should not delete
    the route."""


@dataclass
class RERR_Broadcast_Data(GenericMessagePayload):
    """**Route Error (RERR) Message Payload Format**"""

    dest_count: int
    """The number of unreachable destinations included in the
    message; MUST be at least 1."""

    unreach_addr: str
    """The IP address of the destination that has become
    unreachable due to a link break."""

    unreach_seq: int
    """The sequence number in the route table entry for
    the destination listed in the previous Unreachable
    Destination IP Address field."""


@dataclass
class RERR_Broadcast_Ack(GenericMessageHeader):
    """**Route Reply Acknowledgment (RREP-ACK) Message Format**"""
