from enum import Enum

class ServerState(Enum):
    AVAILABLE = 0
    BUSY = 1
    OOS = 2
    PENDING_OOS = 3
    INVALID = 4

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name