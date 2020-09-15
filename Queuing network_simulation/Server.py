from ServerState import ServerState
from ServerEvent import ServerEvent
from Distribution import Distribution
from Customer import Customer
import math
import numpy as np
import copy as cp

class Server:

    def __init__(self, id, simtime, downTimeDist, oosDist, svcTimeDist):
        self._id = id
        self._status = ServerState.INVALID
        self._custInSvc = None
        self._isPaused = False

        self._systemArrivalTime = simtime            
        self._availableSince = simtime
        self.downTimeDistribution = downTimeDist

        if self.downTimeDistribution != None:
            self._nextDownTime = simtime + self._downTimeDistribution.getEvent()
        else:
            self._nextDownTime = None

        self._nextEventTime = self._nextDownTime

        self.oosDistribution = oosDist
        self.serviceTimeDistribution = svcTimeDist

        if self.downTimeDistribution != None and self.oosDistribution != None and self.serviceTimeDistribution != None:
            self._nextEventType = ServerEvent.SERVER_DOWN
            self._status = ServerState.AVAILABLE
        else:
            self._nextEventType = None  

    @property
    def id(self):
        return self._id

    @property
    def custInSvc(self):
        return self._custInSvc.name

    @property
    def availableSince(self):
        return self._availableSince

    @property
    def isAvailable(self):
        if self.status == ServerState.AVAILABLE:
            self._isAvailable = True
        else:
            self._isAvailable = False

        return self._isAvailable

    @property
    def isBusy(self):
        if self.status == ServerState.BUSY:
            self._isBusy = True
        else:
            self._isBusy = False
            
        return self._isBusy

    @property
    def nextEventTime(self):
        return self._nextEventTime

    @property
    def nextEventType(self):
        return self._nextEventType

    @property
    def serviceTimeDistribution(self):
        return self._serviceTimeDistribution

    @serviceTimeDistribution.setter
    def serviceTimeDistribution(self, svcTimeDist):
        if isinstance(svcTimeDist, Distribution):
            self._serviceTimeDistribution = svcTimeDist
        else:
            self._serviceTimeDistribution = None

    @property
    def downTimeDistribution(self):
        return self._downTimeDistribution

    @downTimeDistribution.setter
    def downTimeDistribution(self, downTimeDist):
        if isinstance(downTimeDist, Distribution):
            self._downTimeDistribution = downTimeDist
        else:
            self._downTimeDistribution = None

    @property
    def oosDistribution(self):
        return self._oosDistribution

    @oosDistribution.setter
    def oosDistribution(self, oosDist):
        if isinstance(oosDist, Distribution):
            self._oosDistribution = oosDist
        else:
            self._oosDistribution = None
    
    @property
    def status(self):
        if self._id is None:
            self._status = ServerState.INVALID        
        elif self._custInSvc == None:
            if self._nextEventType == ServerEvent.SERVER_DOWN:
                if self._nextDownTime >= self._nextEventTime:
                    self._status = ServerState.AVAILABLE
                else:
                    self._status = ServerState.PENDING_OOS
            elif self._nextEventType == ServerEvent.SERVER_UP:
                if self._nextDownTime < self._nextEventTime:
                    self._status = ServerState.OOS
                else:
                    self._status = ServerState.INVALID
            elif self._nextEventType == ServerEvent.SERVICE_COMPLETION:
                self._status = ServerState.INVALID
        else:
            if self._nextEventType == ServerEvent.SERVER_DOWN:
                self._status = ServerState.INVALID
            elif self._nextEventType == ServerEvent.SERVER_UP:
                self._status = ServerState.INVALID
                self._nextEventType = ServerEvent.SERVER_DOWN
            elif self._nextEventType == ServerEvent.SERVICE_COMPLETION:
                #if self._nextDownTime <= self._nextEventTime:
                self._status = ServerState.BUSY
                #else:
                #    self._status = ServerState.BUSY    
                    
        return self._status

    def processEvent(self, simtime):
        if self._nextEventType is ServerEvent.SERVER_UP:
            self._processServerUp(simtime)
            return None
        elif self._nextEventType is ServerEvent.SERVER_DOWN:
            self._processServerDown(simtime)
            return None
        elif self._nextEventType is ServerEvent.SERVICE_COMPLETION:
            customer = self._custInSvc
            self._processServiceCompletion(simtime)
            return customer

    def _processServerUp(self, simtime):
        self._nextDownTime = simtime + self._downTimeDistribution.getEvent()
        self._nextEventTime = self._nextDownTime
        self._nextEventType = ServerEvent.SERVER_DOWN

    def _processServerDown(self, simtime):
        self._nextEventType = ServerEvent.SERVER_UP
        self._nextEventTime = simtime + self._oosDistribution.getEvent()

    def _processServiceCompletion(self, simtime):
        self._completeService(simtime)

    def acceptCustomer(self, simtime, customer):
        if self.isAvailable == False:
            return False
        else:
            if isinstance(customer, Customer) and self._custInSvc == None:
                self._setBusy(simtime, customer)
                self._custInSvc.logServiceEntry(simtime, self.id)
                #self._systemArrivalTime = simtime

                return True

        return False


    def getNextEventTime(self):
        return self._nextEventTime

    def getNextDownTime(self):
        return self._nextDownTime

        
    def _setAvailable(self, simtime):
        self._custInSvc = None
        self._nextEventType = ServerEvent.SERVER_DOWN
        if self._nextDownTime is None or self._nextDownTime <= self._nextEventTime:
            self._nextDownTime = simtime + self._downTimeDistribution.getEvent()
        self._nextEventTime = self._nextDownTime

    def _setBusy(self, simtime, customer):
        self._custInSvc = customer
        self._nextEventType = ServerEvent.SERVICE_COMPLETION 
        self._nextEventTime = simtime + self._serviceTimeDistribution.getEvent()    

    def _setPendingOOS(self, simtime):
        self._custInSvc = None
        self._nextEventType = ServerEvent.SERVER_DOWN

    def _completeService(self, simtime):
        customer = self._custInSvc
        self._custInSvc.logServiceCompletion(simtime)

        if simtime >= self._nextEventTime and self._nextDownTime >= self._nextEventTime:
            self._setAvailable(simtime)
        else:
            self._setPendingOOS(simtime)

        return customer

    def pauseService(self, simtime):
        ret = False
        if self.status is ServerState.BUSY or self.status is ServerState.AVAILABLE:
            self._nextDownTime = simtime
            self._isPaused = True
            ret = True

        return ret

    def resumeService(self, simtime):
        ret = False
        if self.status is ServerState.OOS:
            self._nextEventTime = simtime
            self._isPaused = False
            ret = True

        return ret
        
        
    def __str__(self):
        return self.id
        
    def __repr__(self):
        return self.__str__()

