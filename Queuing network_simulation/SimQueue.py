from CustomerDestination import CustomerDestination
from Server import Server
from ServerState import ServerState
from ServerEvent import ServerEvent
from SystemExit import SystemExit
from Experience import Experience
from Customer import Customer
from QueueEvent import QueueEvent
import numpy as np
import math


class SimQueue(CustomerDestination):
    """
    Stub class to allow for project 5 testing. You will replace this with your own
    Queue class in a future submission. Because this is just a stub for testing,
    only the acceptArrival and getNumCustomersWaiting methods are implemented.
    """

    def __init__(self, id, assignDestination):
        """
        Constructor
        @param id: int or str - Unique identifier/descriptor of the queue
        @param assignDestination: function - Function that accepts a dictionary of objects
                                             as an argument and returns a single selected
                                             object.
        """

        # ensure that object is a valid SimulationStage/CustomerDestination
        super().__init__(id)
        self._id = id
        self._destination = dict()
        self._servers = dict()
        self._assignServer = None
        self._buffer = list()

        self.assignDestination = assignDestination
        self._debug = False




    @property
    def assignDestination(self):

        return self._assignDestination

    @assignDestination.setter
    def assignDestination(self, assignDestination):
        # validate that assignDestination is a function that takes a single argument.

        if callable(assignDestination):
            # assignDestination is a valid function
            self._assignDestination = assignDestination
        else:
            # assignDestination is not a function, so instance is not valid
            self._assignDestination = None
            return

        # if we reached this point, we now have a valid assignDestination function
        # need to test whether or not it requires arguments

        if self._assignDestination.__code__.co_argcount == 1:
            # assignDestination requires one argument, so it is valid
            self._assignDestination = assignDestination
        elif self._assignDestination.__code__.co_argcount == 2 and \
            self._assignDestination.__code__.co_varnames[0] == 'self':
            self._assignDestination = assignDestination
        else:
            # assignDestination should require 1 argument, so it is invalid
            self._assignDestination = None

    @property
    def assignServer(self):
        return self._assignServer

    @assignServer.setter
    def assignServer(self, assignServer):
        if callable(assignServer):
            # assignServer is a valid function
            self._assignServer = assignServer
        else:
            # assignServer is not a function, so instance is not valid
            self._assignServer = None
            return

        # if we reached this point, we now have a valid assignServer function
        # need to test whether or not it requires arguments

        if self._assignServer.__code__.co_argcount == 1:
            # assignServer requires one argument, so it is valid
            self._assignServer = assignServer
        elif self._assignServer.__code__.co_argcount == 2 and \
            self._assignServer.__code__.co_varnames[0] == 'self':
            self._assignServer = assignServer
        else:
            # assignServer should require 1 argument, so it is invalid
            self._assignServer = None

    def acceptArrival(self, simtime, customer):
        """
        Because this is a stub class, instances will ALWAYS accept an arriving customer
        and this method will alays return true
        @param customer: Customer
        @param simtime: double
        @return: True
        """
        servers = self._getAvailableServers()
        customer.logArrival(simtime, self.id)
        self._buffer.append(customer)
        self._advanceCustomers(simtime)

        return True

    def getNumCustomersWaiting(self):
        """
        Because this is a stub class, this method will return a randomly generated
        integer between 0 and 10.
        @return: int
        """

        #return np.random.randint(0, 11)
        return len(self._buffer)

    def _advanceCustomers(self, simtime):
        if self.getNumCustomersWaiting() > 0 and self.getNumAvailableServers() > 0:

            if self.getNumCustomersWaiting() > self.getNumAvailableServers():
                numAdvancedCustomers = self.getNumAvailableServers()
            else:
                numAdvancedCustomers = self.getNumCustomersWaiting()
            for i in range(numAdvancedCustomers):
                #self._buffer[0].logArrival(simtime, self.id)
                server = self.assignServer(self._getAvailableServers())
                server.acceptCustomer(simtime, self._buffer[0])
                del(self._buffer[0])

        return True

    def isValid(self):
        if self.assignDestination != None and self.assignServer != None and \
            len(self._servers) > 0 and len(self._destination) > 0:
            return True
            
        return False
        
    def addServer(self, server):
        if isinstance(server, Server):
            if server.id in self._servers.keys():
                ret = False
            else:
                self._servers[server.id] = server
                ret = True
        else:
            ret = False
        
        return ret

    def addCustomerDestination(self, destination):
        if isinstance(destination, SimQueue) or isinstance(destination, SystemExit):
            if destination._id in self._destination.keys():
                ret = False
            else:
                self._destination[destination._id] = destination
                ret = True
        else:
            ret = False
        
        return ret        


    def removeServer(self, serverId):
        if serverId in self._servers.keys():
            server = self._servers[serverId]
            del self._servers[serverId]
        else:
            server = None

        return server


    def removeCustomerDestination(self, destId):
        if destId in self._destination.keys():
            destination = self._destination[destId]
            del self._destination[destId]
        else:
            destination = None

        return destination

    def getNumAvailableServers(self):

        return len(self._getAvailableServers())


    def _getAvailableServers(self):
        availableServers = {srvr.id: srvr for srvr in self._servers.values() if srvr.isAvailable}

        return availableServers

    def getNextEventTime(self):
        nextEventTimes = [srvr.getNextEventTime() for srvr in sorted(self._servers.values(), key=lambda srvr: srvr.getNextEventTime())]

        if not nextEventTimes:
            return math.inf
        else:
            return nextEventTimes[0]

    def getNextEventType(self):
        nes: Server = [srvr for srvr in sorted(self._servers.values(), key=lambda srvr: srvr.getNextEventTime())]
        
        if nes[0].nextEventType == ServerEvent.SERVER_DOWN:
            nextEventType = QueueEvent.SERVER_DOWN
        elif nes[0].nextEventType == ServerEvent.SERVER_UP:
            nextEventType = QueueEvent.SERVER_UP
        else:
            nextEventType = QueueEvent.SERVICE_COMPLETION

        return nextEventType
          

    def getNumBusyServers(self):

        return len({srvr.id: srvr for srvr in self._servers.values() if srvr.isBusy})


    def processEvent(self, simtime):
        serv = {srvr.id: srvr for srvr in self._servers.values()}
        nes: Server = [srvr for srvr in sorted(serv.values(), key=lambda srvr: srvr.getNextEventTime())]

        if simtime != self.getNextEventTime():
            return None

        if len(nes) > 0:
            customer = nes[0].processEvent(simtime)
            #print("customer in SimQueue: ", customer)
            if customer != None:
                dest_exit = self.assignDestination({dest.id: dest for dest in self._destination.values() if isinstance(dest, SystemExit)})

                if dest_exit != None:
                    #print('simtime in SystemExit: ', simtime)
                    #print('customer in SystemExit: ', customer)
                    dest_exit.acceptArrival(simtime, customer)
        else:
            customer = None

        self._advanceCustomers(simtime)

        return customer


    def __str__(self):
        if isinstance(self._id, str):
            return self._id
        else:
            return str(self._id)


    def __repr__(self):
        return self.__str__()
