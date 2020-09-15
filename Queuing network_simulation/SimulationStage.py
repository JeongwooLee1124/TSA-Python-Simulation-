import math

class SimulationStage:
    """
    Base class representing the public interface that must be implemented by all simulation
    stage subclasses.
    """

    def __init__(self, id):
        """
        Constructor, requires a stage id (any integral type, e.g. int, str).
        @param id: int or str suggested - Id of stage (must be unique for every stage)
        """
        self._id = id

    @property
    def id(self):
        return self._id

    def getNextEventTime(self):
        """
        Because a SimulationStage is an abstract class/interface, it can have no real
        next event time. Therefore, this method always returns infinity
        @return: math.inf
        """

        return math.inf

    def isValid(self):
        """
        Because a SimulationStage is an abstract class/interface, it cannot be
        valid ifi instantiated. Therefore this method always returns False.
        @return: False
        """

        return False

    def processEvent(self, simtime):
        """
        Because a SimulationStage is an abstract class/interface, there can be no real
        event for it to process. Therefore, this method does nothing except return None.
        @param simtime: double - elapsed time (from the beginning of the simulation) at which
                                 the event occurs.
        @return: None
        """

        return None