import math
import numpy as np
from unittest import TestCase, main
from Distribution import Distribution
from SimulationStage import SimulationStage
from CustomerDestination import CustomerDestination
from Customer import Customer
from SimQueue import SimQueue
from Assigner import Assigner
from Server import Server
from SystemExit import SystemExit
from Experience import Experience
from QueueEvent import QueueEvent
from ServerState import ServerState
from ServerEvent import ServerEvent
import copy


np.random.seed(100)
# first setup a queue
testq_org = SimQueue('Q1', Assigner().assignInSequence)

# then setup servers
dist = {}
dist['dt'] = Distribution("triangular(14400, 14400, 18000)")
dist['oos'] = Distribution("triangular(300, 600, 1200)")
dist['st'] = Distribution("exponential(1/300)")

# uncomment to test validity of server construction
# for k, v in self.dist.items():
#     with self.subTest(dist=k):
#         self.assertTrue(v.isValid())

dist['invalid'] = Customer('teddy', 0)

servers = [Server(f'Server{i}', 100*i,
                     dist['dt'],
                     dist['oos'],
                     dist['st']
                     ) for i in range(1,4)]

dest = [SimQueue(f'Queue{i}', Assigner().assignInSequence) for i in range(1,4)]
dest.append(SystemExit('Exit1'))

cust = [Customer(f'Cust{i}', i * 100) for i in range(1,11)]       






## test_processEvent1
testq = copy.deepcopy(testq_org)
testq._assignServer = Assigner().assignInSequence
# add servers and a single SystemExit
testq.addCustomerDestination(dest[3])
'Exit1' == dest[3].id

for srvr in servers:
    testq.addServer(srvr)

True == testq.isValid()

# figure out first event time (all downTimes at this point)
nextEventTimes = [srvr.getNextEventTime() for srvr in servers]
nextEventTimesSorted = sorted(nextEventTimes)
# print(nextEventTimes)
downTime = nextEventTimesSorted[0]
downTime2 = nextEventTimesSorted[1]

downTime == testq.getNextEventTime()
QueueEvent.SERVER_DOWN == testq.getNextEventType()

rstate = np.random.get_state()
expSvcCompTime1 = cust[0].systemArrivalTime + servers[0]._serviceTimeDistribution.getEvent()
np.random.set_state(rstate)
testq.acceptArrival(cust[0].systemArrivalTime, cust[0])
nextEventTimes = [srvr.getNextEventTime() for srvr in servers]
expSvcCompTime1 == servers[0].getNextEventTime()
expSvcCompTime1 == testq.getNextEventTime()
QueueEvent.SERVICE_COMPLETION == testq.getNextEventType()

rslt1 = testq.processEvent(expSvcCompTime1)
True == isinstance(rslt1, Customer)
downTime == testq.getNextEventTime()
QueueEvent.SERVER_DOWN == testq.getNextEventType()
se: SystemExit = dest[3]
1 == len(se._customers)

# try to process an event prematurely

earlyTime = testq.getNextEventTime() - 100
rslt2 = testq.processEvent(earlyTime)
rslt2 == None
downTime == testq.getNextEventTime()

# next event should be a server down on server 2, so let's get the return
# to service time to process the events
rstate = np.random.get_state()
expUpTime = servers[1]._nextDownTime + servers[1]._oosDistribution.getEvent()
np.random.set_state(rstate)

rslt3 = testq.processEvent(downTime)



















## test_advanceCustomers
testq = copy.deepcopy(testq_org)
testq._assignServer = Assigner().assignByAvailableTime

# add servers and destinations
for dest in dest:
    testq.addCustomerDestination(dest)

for srvr in servers:
    testq.addServer(srvr)

# now queue up some customers
for i in range(2):
    cust[i].logArrival(cust[i].systemArrivalTime, testq.id)
    testq._buffer.append(cust[i])
    
    
    
    
    




## acceptArrival
testq = copy.deepcopy(testq_org)
testq._assignServer = Assigner().assignByAvailableTime

# add servers and destinations
for dest in dest:
    testq.addCustomerDestination(dest)

for srvr in servers:
    testq.addServer(srvr)

servers
list(testq._getAvailableServers().values())

0 == testq.getNumBusyServers()












 














## test_isValid
        # test case of missing assignDestination function. Instantiate and
        # force other attributes
testq = copy.deepcopy(testq_org)
testq._servers = servers
testq._assignServer = Assigner().assignInSequence
testq._assignDestination = None
testq._destination[1] = dest[0]
False == testq.isValid()
        
# now add in an assignDestination function and recheck
testq.assignDestination = Assigner().assignToShortest
True == testq.isValid()

# now test with assignDestination, but no assignServer
testq = copy.deepcopy(testq_org)
testq._servers = servers
testq._destination[1] = dest[0]
False == testq.isValid()      
        
# now test with everything except destinations
testq = copy.deepcopy(testq_org)
testq._servers = servers
testq._assignServer = Assigner().assignInSequence
False == testq.isValid()

# now add in an assignDestination function and recheck
testq._destination[1] = dest[0]
True == testq.isValid()

# now test with everything except Servers
testq = copy.deepcopy(testq_org)
testq._assignServer = Assigner().assignInSequence
testq._destination[1] = dest[0]
False == testq.isValid()

# now add in an assignDestination function and recheck
testq._servers = servers
True == testq.isValid()

        
        
## test_getNextEventTime
testq = copy.deepcopy(testq_org)
testq._assignServer = Assigner().assignInSequence
        # add servers and destinations
for dest1 in dest:
    testq.addCustomerDestination(dest1)

for srvr in servers:
    testq.addServer(srvr)

True == testq.isValid()

# figure out first event time (all downTimes at this point)
nextEventTimes = [srvr.getNextEventTime() for srvr in servers]
expNext = min(nextEventTimes)
expNext
testq.getNextEventTime()
# self.assertEqual(QueueEvent.SERVER_DOWN, testq.getNextEventType())

# Place Server1 in service
rstate = np.random.get_state()
expSvcCompTime1 = cust[0].systemArrivalTime + servers[0]._serviceTimeDistribution.getEvent()
np.random.set_state(rstate)

testq.acceptArrival(cust[0].systemArrivalTime, cust[0])
nextEventTimes = [srvr.getNextEventTime() for srvr in servers]
expSvcCompTime1
servers[0].getNextEventTime()
expSvcCompTime1
testq.getNextEventTime()


for srvr in servers:
    print(srvr.id)
    print(srvr.nextEventTime)
    print(srvr.status)


# now, complete service and recheck
servers[0]._completeService(expSvcCompTime1)
for srvr in servers:
    print(srvr.id)
    print(srvr.nextEventTime)
    print(srvr.status)


    
print("testq.getNextEventTime(): ", testq.getNextEventTime())
print("expSvcCompTime1: ", expSvcCompTime1)
print("expNext: ", expNext)
expNext
testq.getNextEventTime()
        
        
        
        
        
        
        
        
        