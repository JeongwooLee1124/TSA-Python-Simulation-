from SimulationStage import SimulationStage
from Distribution import Distribution
from CustomerDestination import CustomerDestination
from Customer import Customer
from Assigner import Assigner
import numpy as np
import math

class SourcePopulation(SimulationStage):
    def __init__(self, id, distribution, assignDestination):
        self._sourceId = id
        if distribution.isValid() is True:
            self._arrivalTimeDistribution = distribution
            self._nextArrivalTime = self._arrivalTimeDistribution.getEvent()
        else:
            self._arrivalTimeDistribution = None
            self._nextArrivalTime = None
        self.setAssignDestination(assignDestination)

        self._destination = {}
        self._isValid = False
        self._customers = dict()
        self._last_cust = 0

    @property
    def id(self):
        return self._sourceId


    def addCustomerDestination(self, dest):
        if hasattr(dest, 'id') == True and isinstance(dest.id, str):
            if dest.id in self._destination:
                return False
            else:
                self._destination.update({dest.id: dest})
                return True
        else:
            return False

    
    def getNextEventTime(self):
        if self.isValid() != True:
            self._nextArrivalTime = math.nan
        return self._nextArrivalTime

    def isValid(self):
        if len(self._destination) > 0 and self._arrivalTimeDistribution != None and self._assignDestination != None:
            self._isValid = True
        else:
            self._isValid = False
        return self._isValid

    def processEvent(self, simtime):
        if simtime < self._nextArrivalTime:
            return None
        customer = Customer(f'{self._sourceId}-{len(self._customers)+1}', simtime)
        self._customers[customer.name] = customer
        self._last_cust += 1
        destination = self._assignDestination(self._destination)
        destination.acceptArrival(simtime, customer)
        self._nextArrivalTime = simtime + self._arrivalTimeDistribution.getEvent()

        return customer


    def removeCustomerDestination(self, destId):
        if destId in self._destination:
            ret = self._destination[destId]
            del self._destination[destId]
            return ret
        else:
            return None


    def setArrivalTimeDistribution(self, dist):
        self._arrivalTimeDistribution = dist


    def setAssignDestination(self, assignDestination):
        self._assignDestination = None
        if assignDestination != None: 
            if callable(assignDestination):
                argnum = assignDestination.__code__.co_argcount
                if str(type(assignDestination)) == "<class 'method'>":
                    argnum -= 1
                if argnum == 1:
                    self._assignDestination = assignDestination