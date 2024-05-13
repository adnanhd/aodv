from enum import Enum
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


class AODV_Broadcast_Header(GenericMessageHeader):
    @property
    def prev_hop(self) -> int:
        """The IP address of the node from which the
        Route Request was received."""
        return int(self.messagefrom)

    @property
    def dest_addr(self) -> int:
        """The IP address of the destination for which a route
        is desired."""
        return int(self.messageto)

    @property
    def seq_num(self) -> int:  # str:
        """The IP address of the node which originated the
        Route Request."""
        return int(self.sequencenumber)


class RREQ_Broadcast_Head(AODV_Broadcast_Header):
    """**Route Request (RREQ) Message Header Format**"""

    def __init__(self, messagefrom, messageto, *args, **kwargs):
        super().__init__(MessageTypes.RREQ, messagefrom, messageto, *args, **kwargs)


class RREP_Broadcast_Head(AODV_Broadcast_Header):
    """**Route Reply (RREP) Message Header Format**"""

    def __init__(self, messagefrom, messageto, *args, **kwargs):
        super().__init__(MessageTypes.RREP, messagefrom, messageto, *args, **kwargs)


class RERR_Broadcast_Head(AODV_Broadcast_Header):
    """**Route Error (RERR) Message Header Format**"""

    def __init__(self, messagefrom, messageto, *args, **kwargs):
        super().__init__(MessageTypes.RERR, messagefrom, messageto, *args, **kwargs)


class DATA_Broadcast_Head(AODV_Broadcast_Header):
    """**Route Data (DATA) Message Header Format**"""

    def __init__(self, messagefrom, messageto, *args, **kwargs):
        super().__init__(MessageTypes.DATA, messagefrom, messageto, *args, **kwargs)


class RREQ_Broadcast_Data(GenericMessagePayload):
    """**Route Request (RREQ) Message Header Format**"""

    def __init__(self, src_addr: int, dest_addr: int, hop_count: int = -1, rreq_id: int = -1, dest_seq: int = -1, src_seq: int = -1,
                 f_join_multicast: bool = False, f_repair_multicast: bool = False, f_gratuitous: bool = False,
                 f_dest_only: bool = False, unk_seq_num: bool = False):

        super().__init__(messagepayload=dict(hop_count=hop_count, rreq_id=rreq_id,
                                             dest_seq=dest_seq, src_seq=src_seq,
                                             f_join_multicast=f_join_multicast,
                                             f_repair_multicast=f_repair_multicast,
                                             f_gratuitous=f_gratuitous, f_dest_only=f_dest_only,
                                             unk_seq_num=unk_seq_num, dest_addr=dest_addr, src_addr=src_addr))

    @property
    def dest_addr(self) -> int:  # str:
        """The IP address of the destination for which a route
        is desired."""
        return int(self.messagepayload["dest_addr"])

    @property
    def src_addr(self) -> int:  # str:
        """The IP address of the node which originated the
        Route Request."""
        return int(self.messagepayload["src_addr"])

    @property
    def hop_count(self) -> int:
        """The number of hops from the Originator IP Address
        to the node handling the request."""
        return self.messagepayload["hop_count"]

    @property
    def rreq_id(self) -> int:
        """A sequence number uniquely identifying the
        particular RREQ when taken in conjunction with the
        originating node's IP address."""
        return self.messagepayload["rreq_id"]

    @property
    def dest_seq(self) -> int:
        """The latest sequence number received in the past
        by the originator for any route towards the
        destination."""
        return self.messagepayload["dest_seq"]

    @property
    def src_seq(self) -> int:
        """The current sequence number to be used in the route
        entry pointing towards the originator of the route
        request."""
        return self.messagepayload["src_seq"]

    @property
    def f_join_multicast(self) -> bool:  # = False
        """Join flag; reserved for multicast."""
        return self.messagepayload["f_join_multicast"]

    @property
    def f_repair_multicast(self) -> bool:  # = False
        """Repair flag; reserved for multicast."""
        return self.messagepayload["f_repair_multicast"]

    @property
    def f_gratuitous(self) -> bool:  # False
        """Gratuitous RREP flag; indicates whether a
        gratuitous RREP should be unicast to the node
        specified in the Destination IP Address field (see
        sections 6.3, 6.6.3)."""
        return self.messagepayload["f_gratuitous"]

    @property
    def f_dest_only(self) -> bool:  # False
        """Destination only flag; indicates only the
        destination may respond to this RREQ (see
        section 6.5)."""
        return self.messagepayload["f_dest_only"]

    @property
    def unk_seq_num(self) -> bool:  # False
        """Unknown sequence number; indicates the destination
        sequence number is unknown (see section 6.3)."""
        return self.messagepayload["unk_seq_num"]

    def __repr__(self) -> str:
        return f"RREQ_Broadcast_Data({self.hop_count}, {self.rreq_id}, {self.dest_seq}, {self.src_seq}, {self.f_join_multicast}, {self.f_repair_multicast}, {self.f_gratuitous}, {self.f_dest_only}, {self.unk_seq_num})"


class RREP_Broadcast_Data(GenericMessagePayload):
    """**Route Reply (RREP) Message Payload Format**"""

    def __init__(self, hop_count: int, dest_addr: str, dest_seq: int, src_addr: str,
                 f_repair: bool = False, f_ack: bool = False, prefix_size: int = 0, lifetime: int = 0):
        super().__init__(
            messagepayload=dict(
                hop_count=hop_count, dest_addr=dest_addr, dest_seq=dest_seq, src_addr=src_addr,
                f_repair=f_repair, f_ack=f_ack, prefix_size=prefix_size, lifetime=lifetime
            )
        )

    @property
    def f_repair(self) -> bool:  # = False
        """Repair flag; indicates the RREP is part of a
        repair process."""
        return self.messagepayload["f_repair"]

    @property
    def f_ack(self) -> bool:  # = False
        """Acknowledgement flag; indicates the RREP is an
        acknowledgement for a previously received RREQ."""
        return self.messagepayload["f_ack"]

    @property
    def prefix_size(self) -> int:  # = 0  # Predecessor node Hop Lifetime (optional)
        """If nonzero, the 5-bit Prefix Size specifies that the
        indicated next hop may be used for any nodes with
        the same routing prefix (as defined by the Prefix
        Size) as the requested destination."""
        return self.messagepayload["prefix_size"]

    @property
    def hop_count(self) -> int:
        """The number of hops from the Originator IP Address
        to the Destination IP Address.  For multicast route
        requests this indicates the number of hops to the
        multicast tree member sending the RREP."""
        return self.messagepayload["hop_count"]

    @property
    def dest_addr(self) -> str:
        """The IP address of the destination for which a route
        is supplied."""
        return self.messagepayload["dest_addr"]

    @property
    def dest_seq(self) -> int:
        """The destination sequence number associated to the
        route."""
        return self.messagepayload["dest_seq"]

    @property
    def src_addr(self) -> str:
        """The IP address of the node which originated the RREQ
        for which the route is supplied."""
        return self.messagepayload["src_addr"]

    @property
    def lifetime(self) -> int:  # = 0  # Target node Hop Lifetime (optional)
        """The time in milliseconds for which nodes receiving
        the RREP consider the route to be valid."""
        return self.messagepayload["lifetime"]

    def __repr__(self) -> str:
        return f"RREP_Broadcast_Data({self.hop_count}, {self.dest_addr}, {self.dest_seq}, {self.src_addr}, {self.f_repair}, {self.f_ack}, {self.prefix_size}, {self.lifetime})"


class RERR_Broadcast_Data(GenericMessagePayload):
    """**Route Error (RERR) Message Payload Format**"""

    f_no_del: bool = False
    """No delete flag; set when a node has performed a local
    repair of a link, and upstream nodes should not delete
    the route."""

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


class RERR_Broadcast_Ack(GenericMessageHeader):
    """**Route Reply Acknowledgment (RREP-ACK) Message Format**"""
