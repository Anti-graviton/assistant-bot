from enum import Enum


class State(Enum):
        UNKNOWN = 0
        WON = 1
        UNREGISTERED = 2
        REGISTERED = 3


class Action(Enum):
        UNKNOWN = 0
        ADDCAR = 1
        RMCAR = 2


class EventType(Enum):
        LOTTERY = 0
        PES = 1
