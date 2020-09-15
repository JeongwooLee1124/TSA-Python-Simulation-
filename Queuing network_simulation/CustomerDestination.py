import math
from SimulationStage import SimulationStage


class CustomerDestination(SimulationStage):
    """
    Abstract base class for all customer destinations such as Queue and SystemExit.
    """

    def acceptArrival(self, simtime, Customer):
        """
        Because SimulationStage is an abstract class, a SimulationStage instance cannot accept
        arrivals.
        @param simtime: double - elapsed time, from the start of the simulation, at which the
                                 Customer arrival is taking place.
        @param customer: Customer - instance of Customer class that has arrived at the
                                    SimulationStage
        @return: False
        """

        return False

    def getNumCustomersWaiting(self):
        """
        Because SimulationStage is an abstract class, there can be no Customers waiting.
        Therefore, this method always returns math.nan.
        @return: math.nan
        """

        return math.nan
