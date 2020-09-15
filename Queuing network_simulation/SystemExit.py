from CustomerDestination import CustomerDestination
from Customer import Customer

class SystemExit(CustomerDestination):

    def __init__(self, systemId):
        self._customers = {}
        self._id = systemId
        self._isValid = True

    def isValid(self):
        return True

    def acceptArrival(self, simtime, customer):
        if customer.name in self._customers:
            return False
        else:
            self._customers[customer.name] = customer
            return True

    def getNumCustomersWaiting(self):
        return 0

    def __iter__(self):
        return iter(self._customers.values())

    def arrivalTimeIterator(self):
        return sorted(self._customers.values(), key=lambda Customer:Customer.systemArrivalTime)

    def __str__(self):
        return self._id



