from enum import Enum
from adhoccomputing.GenericModel import GenericMessagePayload, GenericMessageHeader, GenericMessage


class MessageTypes(Enum):
    RREQ = 1
    """Route Request Message Format"""

    RREP = 2
    """Route Reply Message Format"""

    RERR = 3
    """Route Error Message Format"""

    DATA = 4
    """Route Reply Acknowledgment Message Format"""

############################################################################################################
# AODV Broadcasting Message


class AODVBroadcastingMessageHeader(GenericMessageHeader):
    def __init__(self, messagetype: MessageTypes, messagefrom: int, messageto: int,
                 nexthop: int = float('inf'), interfaceid: int = float('inf'),
                 sequencenumber: int = -1, hopFrom: int = None, hopCount: int = -1):
        assert isinstance(messagetype, MessageTypes)
        super().__init__(messagetype, messagefrom, messageto,
                         nexthop, interfaceid, sequencenumber)
        self.hopFrom: int = hopFrom
        self.hopCount: int = hopCount


class AODVBroadcastingMessagePayload(GenericMessagePayload):
    pass


class AODVBroadcastingMessage(GenericMessage):
    pass


############################################################################################################
# AODV Application Layer Message
class AODVApplicationLayerMessageHeader(GenericMessageHeader):
    pass


class AODVApplicationLayerMessagePayload(GenericMessagePayload):
    pass


class AODVApplicationLayerMessage(GenericMessage):
    pass
