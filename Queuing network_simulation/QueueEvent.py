from enum import Enum

class QueueEvent(Enum):
    SERVICE_COMPLETION = 0
    SERVER_DOWN = 1
    SERVER_UP = 2

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name