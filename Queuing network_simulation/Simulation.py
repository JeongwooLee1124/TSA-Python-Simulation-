from CustomerDestination import CustomerDestination
from Server import Server
from Distribution import Distribution
from ServerState import ServerState
from ServerEvent import ServerEvent
from SystemExit import SystemExit
from Experience import Experience
from Customer import Customer
from QueueEvent import QueueEvent
from SourcePopulation import SourcePopulation
from Assigner import Assigner
from SimQueue import SimQueue
import numpy as np
import pandas as pd
import math

class Simulation:
    def __init__(self, seedVal = None):
        self._seed = seedVal
        self._numStages = 0
        self._simtime = 0
        self._stages = dict()
        self._totalTrialsCompleted = 0
        self._customers = dict()

    def setup(self, choice = 'Figure2'):
        if choice == 'Figure2':
            print("Figure2 setup is used")
            self.setup_Figure2()
        elif choice == 'Figure3':
            print("Figure3 setup is used")
            self.setup_Figure3()
        else:
            print("please using one of setup('Figure2') or setup('Figure3')")

    def setup_Figure2(self):
        np.random.seed(self.seed)

        assigner = Assigner()
        dist = dict()
        dist['ar'] = Distribution("exponential(180)")
        dist['dt'] = Distribution("triangular(14400, 14400, 18000)")
        dist['oos'] = Distribution("triangular(300, 600, 1200)")
        dist['st'] = Distribution("exponential(144)")

        # define 2 valid system exits
        for i in range(2):
            self._stages[f'SE{i}'] = SystemExit(f'SE{i}')

        # define one valid source populations 
        self._stages['SP-PRE'] = SourcePopulation('SP-PRE', dist['ar'], assigner.assignToShortest)

        # define the other valid source populations 
        self._stages['SP-REG'] = SourcePopulation('SP-REG', dist['ar'], assigner.assignToShortest)

        # define a valid one server per one queue for SP-PRE
        for i in range(3):
            self._stages[f'Q{i}'] = SimQueue(f'Q{i}', assigner.assignInSequence)
            self._stages[f'Q{i}'].addCustomerDestination(self._stages['SE0'])
            self._stages[f'Q{i}'].assignServer = assigner.assignByAvailableTime

            server = Server(f'Server{i}', 0, dist['dt'], dist['oos'], dist['st'])
            self._stages[f'Q{i}'].addServer(server)        

            self._stages['SP-PRE'].addCustomerDestination(self._stages[f'Q{i}'])

        # define a valid one server per one queue for SP-REG
        for i in range(3, 7):
            self._stages[f'Q{i}'] = SimQueue(f'Q{i}', assigner.assignInSequence)
            self._stages[f'Q{i}'].addCustomerDestination(self._stages['SE1'])
            self._stages[f'Q{i}'].assignServer = assigner.assignByAvailableTime

            server = Server(f'Server{i}', 0, dist['dt'], dist['oos'], dist['st'])
            self._stages[f'Q{i}'].addServer(server)        

            self._stages['SP-REG'].addCustomerDestination(self._stages[f'Q{i}'])




    def setup_Figure3(self):
        np.random.seed(self.seed)

        assigner = Assigner()
        dist = dict()
        dist['ar'] = Distribution("exponential(180)")
        dist['dt'] = Distribution("triangular(14400, 14400, 18000)")
        dist['oos'] = Distribution("triangular(300, 600, 1200)")
        dist['st'] = Distribution("exponential(144)")

        # define 2 valid system exits
        for i in range(2):
            self._stages[f'SE{i}'] = SystemExit(f'SE{i}')

        # define one valid source populations 
        self._stages['SP-PRE'] = SourcePopulation('SP-PRE', dist['ar'], assigner.assignToShortest)

        # define the other valid source populations 
        self._stages['SP-REG'] = SourcePopulation('SP-REG', dist['ar'], assigner.assignToShortest)


        # define a valid queue, Q0
        self._stages['Q0'] = SimQueue('Q0', assigner.assignInSequence)
        self._stages['Q0'].addCustomerDestination(self._stages['SE0'])
        self._stages['Q0'].assignServer = assigner.assignByAvailableTime
        self._stages['SP-PRE'].addCustomerDestination(self._stages['Q0'])
        for i in range(3):
            server = Server(f'Server{i}', 0, dist['dt'], dist['oos'], dist['st'])
            self._stages['Q0'].addServer(server)

        # define the other valid queue, Q1
        self._stages['Q1'] = SimQueue('Q1', assigner.assignInSequence)
        self._stages['Q1'].addCustomerDestination(self._stages['SE1'])
        self._stages['Q1'].assignServer = assigner.assignByAvailableTime
        self._stages['SP-REG'].addCustomerDestination(self._stages['Q1'])
        for i in range(3, 7):
            server = Server(f'Server{i}', 0, dist['dt'], dist['oos'], dist['st'])
            self._stages['Q1'].addServer(server)


        return

    @property
    def simtime(self):
        return self._simtime

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seedVal):
        self._seed = seedVal

    @property
    def numStages(self):
        self._numStages = len(self._stages)

        return self._numStages


    def addStage(self, stage):
        if isinstance(stage, SourcePopulation) is True or isinstance(stage, SimQueue) is True or isinstance(stage, SystemExit) is True:
            if stage.id in self._stages.keys():
                ret = False
            else:
                self._stages[stage.id] = stage
                ret = True
        else:
            ret = False
            
        return ret

    def removeStage(self, stageId):
        if stageId in self._stages.keys():
            del(self._stages[stageId])
            ret = True
        else:
            ret = False

        return ret

    def getSimResults(self):

        return self._customers

    def getSimulatedTime(self):

        return self._simtime

    def getTrialsCompleted(self):

        return self._totalTrialsCompleted

    def run(self, maxTime = math.inf, maxEvents = 1000):
        
        for i in range(maxEvents):
            self._totalTrialsCompleted += 1
            ids = [stage.id for stage in sorted(self._stages.values(), key=lambda stage: stage.getNextEventTime())]

            self._simtime = self._stages[ids[0]].getNextEventTime()
            customer = self._stages[ids[0]].processEvent(self._stages[ids[0]].getNextEventTime())
            if customer != None:
                self._customers[customer.name] = customer

        return

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.seed)

    def __iter__(self):
        systemExit = {systemExit.id: systemExit for systemExit in self._stages.values() if isinstance(self._stages, SystemExit)}

        return iter(self._customers.values())
