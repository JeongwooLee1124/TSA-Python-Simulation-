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
#from collections import deque
import copy

class TestSimQueue(TestCase):

    def setUp(self) -> None:
        np.random.seed(100)
        # first setup a queue
        self.testq = SimQueue('Q1', Assigner().assignInSequence)

        # then setup servers
        self.dist = {}
        self.dist['dt'] = Distribution("triangular(14400, 14400, 18000)")
        self.dist['oos'] = Distribution("triangular(300, 600, 1200)")
        self.dist['st'] = Distribution("exponential(1/300)")

        # uncomment to test validity of server construction
        # for k, v in self.dist.items():
        #     with self.subTest(dist=k):
        #         self.assertTrue(v.isValid())

        self.dist['invalid'] = Customer('teddy', 0)

        self.servers = [Server(f'Server{i}', 100*i,
                             self.dist['dt'],
                             self.dist['oos'],
                             self.dist['st']
                             ) for i in range(1,4)]

        self.dest = [SimQueue(f'Queue{i}', Assigner().assignInSequence) for i in range(1,4)]
        self.dest.append(SystemExit('Exit1'))

        self.cust = [Customer(f'Cust{i}', i * 100) for i in range(1,11)]

    def test_init(self):
        # first verify identity
        self.dest = SimQueue(1234, lambda x: x)

        self.assertTrue(isinstance(self.dest.__str__(), str))
        self.assertTrue(isinstance(self.dest.__repr__(), str))

        self.assertFalse(self.dest.assignDestination is None)
        self.assertEqual(1234, self.dest.id)

        self.assertTrue(isinstance(self.dest, SimulationStage))
        self.assertTrue(isinstance(self.dest, CustomerDestination))
        self.assertTrue(isinstance(self.dest, SimQueue))

        # next, verify that inherited functions are still working correctly
        self.assertTrue(self.dest.processEvent(5) is None)
        self.assertTrue(math.isinf(self.dest.getNextEventTime()))

    def test_isValid(self):

        # test case of missing assignDestination function. Instantiate and
        # force other attributes
        testq = copy.deepcopy(self.testq)
        testq._servers = self.servers
        testq._assignServer = Assigner().assignInSequence
        testq._assignDestination = None
        testq._destination[1] = self.dest[0]
        self.assertFalse(testq.isValid())

        # now add in an assignDestination function and recheck
        testq.assignDestination = Assigner().assignToShortest
        self.assertTrue(testq.isValid())

        # now test with assignDestination, but no assignServer
        testq = copy.deepcopy(self.testq)
        testq._servers = self.servers
        testq._destination[1] = self.dest[0]
        self.assertFalse(testq.isValid())

        # now add in an assignDestination function and recheck
        testq.assignServer = Assigner().assignToShortest
        self.assertTrue(testq.isValid())

        # now test with everything except destinations
        testq = copy.deepcopy(self.testq)
        testq._servers = self.servers
        testq._assignServer = Assigner().assignInSequence
        self.assertFalse(testq.isValid())

        # now add in an assignDestination function and recheck
        testq._destination[1] = self.dest[0]
        self.assertTrue(testq.isValid())

        # now test with everything except Servers
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignInSequence
        testq._destination[1] = self.dest[0]
        self.assertFalse(testq.isValid())

        # now add in an assignDestination function and recheck
        testq._servers = self.servers
        self.assertTrue(testq.isValid())

    def test_getNumCustomersWaiting(self):
        self.assertEqual(0, self.testq.getNumCustomersWaiting())

        self.testq._buffer.append(1)
        self.assertEqual(1, self.testq.getNumCustomersWaiting())

        self.testq._buffer.append(2)
        self.testq._buffer.append(3)
        self.assertEqual(3, self.testq.getNumCustomersWaiting())

        # remove the leftmost Customer - i.e. the one waiting the longest
        # self.testq._buffer.popleft()
        temp = self.testq._buffer.copy()
        temp.clear()
        for i in range(1, len(self.testq._buffer)):
            temp.append(self.testq._buffer[i])
        self.testq._buffer = temp

        self.assertEqual(2, self.testq.getNumCustomersWaiting())

    def test_addDestination(self):
        # verify initial state
        testq = copy.deepcopy(self.testq)
        testq._servers = self.servers
        testq._assignServer = Assigner().assignInSequence

        self.assertFalse(testq.isValid())

        # now add some destinations
        self.assertTrue(testq.addCustomerDestination(self.dest[0]))
        self.assertTrue(testq.isValid())
        self.assertEqual(1, len(testq._destination))

        # now try re-adding additional destinations
        for i in range(len(self.dest)):
            with self.subTest(i=i):
                rslt = testq.addCustomerDestination(self.dest[i])
                if i == 0:
                    self.assertFalse(rslt)
                else:
                    self.assertTrue(rslt)

                self.assertEqual(i+1, len(testq._destination))

        self.assertTrue(testq.isValid())

        # now try to add an invalid destination (i.e. not a CustomerDestination)
        self.assertFalse(testq.addCustomerDestination(self.servers[0]))
        self.assertFalse(testq.addCustomerDestination(5))

        self.assertEqual(4, len(testq._destination))

    def test_addServer(self):
        # verify initial state
        testq = copy.deepcopy(self.testq)
        testq._destination = self.dest
        testq._assignServer = Assigner().assignInSequence

        self.assertFalse(testq.isValid())

        # now add a Server
        self.assertTrue(testq.addServer(self.servers[0]))
        self.assertTrue(testq.isValid())
        self.assertEqual(1, len(testq._servers))

        # now try adding additional Servers
        for i in range(len(self.servers)):
            with self.subTest(i=i):
                rslt = testq.addServer(self.servers[i])
                if i == 0:
                    # server 1 already exists so this one should fail
                    self.assertFalse(rslt)
                else:
                    self.assertTrue(rslt)

                self.assertEqual(i+1, len(testq._servers))

        self.assertTrue(testq.isValid())

        # now try to add an invalid destination (i.e. not a Server)
        self.assertFalse(testq.addServer(self.dest[0]))
        self.assertFalse(testq.addServer(5))

        self.assertEqual(3, len(testq._servers))

    def test_removeDestination(self):
        testq = copy.deepcopy(self.testq)
        testq._servers = self.servers
        testq._assignServer = Assigner().assignInSequence

        # now try re-adding additional destinations
        for i in range(len(self.dest)):
            with self.subTest(i=i):
                testq.addCustomerDestination(self.dest[i])

        self.assertEqual(len(self.dest), len(testq._destination))
        self.assertTrue(testq.isValid())

        # now try to remove an invalid destination (i.e. doesn't exist)
        self.assertTrue(testq.removeCustomerDestination('dummy') is None)

        # now try to remove a valid destination (i.e. it exists)
        self.assertTrue(isinstance(testq.removeCustomerDestination('Queue1'), CustomerDestination))
        self.assertEqual(3, len(testq._destination))

    def test_removeServer(self):
        testq = copy.deepcopy(self.testq)
        testq._destination = self.dest
        testq._assignServer = Assigner().assignInSequence

        # now add Servers
        for i in range(len(self.servers)):
            with self.subTest(i=i):
                testq.addServer(self.servers[i])

        self.assertEqual(len(self.servers), len(testq._servers))
        self.assertTrue(testq.isValid())

        # now try to remove an invalid Server (i.e. doesn't exist)
        self.assertTrue(testq.removeServer('dummy') is None)

        # now try to remove a valid destination (i.e. it exists)
        self.assertTrue(isinstance(testq.removeServer('Server1'), Server))
        self.assertEqual(2, len(testq._servers))

    def test_getNumAvailableServers(self):
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignInSequence

        # add servers and destinations
        for dest in self.dest:
            testq.addCustomerDestination(dest)

        for srvr in self.servers:
            testq.addServer(srvr)

        self.assertTrue(testq.isValid())

        # all servers should be available
        self.assertEqual(len(self.servers), testq.getNumAvailableServers())

        # now let's make a server busy
        n = min(len(self.servers), len(self.cust))
        for i in range(n):
            with self.subTest(i=i):
                self.cust[i].logArrival(self.cust[i].systemArrivalTime, testq.id)
                testq._servers[self.servers[i].id].acceptCustomer(self.cust[i].systemArrivalTime, self.cust[i])
                self.assertEqual(len(self.servers) - (i + 1), testq.getNumAvailableServers())

        self.assertEqual(len(self.servers) - n, testq.getNumAvailableServers())

    def test_getAvailableServers(self):
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignInSequence

        # add servers and destinations
        for dest in self.dest:
            testq.addCustomerDestination(dest)

        for srvr in self.servers:
            testq.addServer(srvr)

        # now test that all are available
        self.assertListEqual(self.servers, list(testq._getAvailableServers().values()))

        # put Server 1 into service and retest
        self.cust[0].logArrival(self.cust[0].systemArrivalTime, testq.id)
        testq._servers[self.servers[0].id].acceptCustomer(self.cust[0].systemArrivalTime, self.cust[0])
        self.assertEqual(len(self.servers) - 1, testq.getNumAvailableServers())

        self.assertListEqual(self.servers[1:], list(testq._getAvailableServers().values()))

        # put Server 3 into service and retest
        self.cust[1].logArrival(self.cust[1].systemArrivalTime, testq.id)
        testq._servers[self.servers[2].id].acceptCustomer(self.cust[1].systemArrivalTime, self.cust[1])
        self.assertEqual(len(self.servers) - 2, testq.getNumAvailableServers())

        self.assertListEqual(self.servers[1:2], list(testq._getAvailableServers().values()))

        # finally, place Server 2 into service

        self.cust[2].logArrival(self.cust[2].systemArrivalTime, testq.id)
        testq._servers[self.servers[1].id].acceptCustomer(self.cust[2].systemArrivalTime, self.cust[2])
        self.assertEqual(0, testq.getNumAvailableServers())

        self.assertListEqual([], list(testq._getAvailableServers().values()))

    def test_advanceCustomers(self):
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignByAvailableTime

        # add servers and destinations
        for dest in self.dest:
            testq.addCustomerDestination(dest)

        for srvr in self.servers:
            testq.addServer(srvr)

        # now test that all are available
        self.assertListEqual(self.servers, list(testq._getAvailableServers().values()))
        self.assertEqual(0, testq.getNumBusyServers())

        # now queue up some customers
        for i in range(2):
            self.cust[i].logArrival(self.cust[i].systemArrivalTime, testq.id)
            testq._buffer.append(self.cust[i])

        self.assertEqual(2, testq.getNumCustomersWaiting())

        # advance customers and retest
        testq._advanceCustomers(1000)
        self.assertEqual(1, testq.getNumAvailableServers())
        self.assertListEqual(self.servers[2:], list(testq._getAvailableServers().values()))
        self.assertEqual(0, testq.getNumCustomersWaiting())
        self.assertEqual(2, testq.getNumBusyServers())

        for i in range(2):
            with self.subTest(i=i):
                temp : Experience = list(self.cust[i].getExperiences().values())[0]
                self.assertAlmostEqual(1000, temp.serviceEntryTime)

        # add and advance another customer
        self.cust[2].logArrival(self.cust[2].systemArrivalTime, testq.id)
        testq._buffer.append(self.cust[2])
        self.assertEqual(1, testq.getNumCustomersWaiting())
        self.assertTrue(testq._advanceCustomers(2000))
        self.assertEqual(0, testq.getNumCustomersWaiting())
        self.assertEqual(3, testq.getNumBusyServers())

        self.assertAlmostEqual(2000, list(self.cust[2].getExperiences().values())[0].serviceEntryTime)

        # attempt
        # self.assertListEqual(self.servers[1:], testq._getAvailableServers())
        #
        # # put Server 3 into service and retest
        # self.cust[1].logArrival(self.cust[1].systemArrivalTime, testq.id)
        # testq._servers[self.servers[2].id].acceptCustomer(self.cust[1].systemArrivalTime, self.cust[1])
        # self.assertEqual(len(self.servers) - 2, testq.getNumAvailableServers())
        #
        # self.assertListEqual(self.servers[1:2], testq._getAvailableServers())
        #
        # # finally, place Server 2 into service
        #
        # self.cust[2].logArrival(self.cust[2].systemArrivalTime, testq.id)
        # testq._servers[self.servers[1].id].acceptCustomer(self.cust[2].systemArrivalTime, self.cust[2])
        # self.assertEqual(0, testq.getNumAvailableServers())
        #
        # self.assertListEqual([], testq._getAvailableServers())

    def test_acceptArrival(self):
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignByAvailableTime

        # add servers and destinations
        for dest in self.dest:
            testq.addCustomerDestination(dest)

        for srvr in self.servers:
            testq.addServer(srvr)

        # now test that all are available
        self.assertListEqual(self.servers, list(testq._getAvailableServers().values()))
        self.assertEqual(0, testq.getNumBusyServers())

        # now queue up some customers - should accept all 3 customers
        # and immediately advance to service
        for i in range(3):
            with self.subTest(i=i):
                self.assertTrue(testq.acceptArrival(self.cust[i].systemArrivalTime,
                                                    self.cust[i]))
                exp: Experience = list(self.cust[i].getExperiences().values())[0]
                self.assertEqual(self.cust[i].systemArrivalTime,
                                 exp.serviceEntryTime)
                self.assertEqual(self.servers[i].id, exp.serverId)

                self.assertEqual(0, testq.getNumCustomersWaiting())
                self.assertEqual(i + 1, testq.getNumBusyServers())
                self.assertEqual(len(self.servers) - (i + 1), testq.getNumAvailableServers())

        # now that all servers are busy, advance three more customers
        # who will have to remain in the buffer

        for i in range(3,6):
            with self.subTest(i=i):
                self.assertTrue(testq.acceptArrival(self.cust[i].systemArrivalTime,
                                                    self.cust[i]))
                exp: Experience = list(self.cust[i].getExperiences().values())[0]
                self.assertTrue(math.isnan(exp.serviceEntryTime))

                self.assertEqual(i - 2, testq.getNumCustomersWaiting())
                self.assertEqual(3, testq.getNumBusyServers())
                self.assertEqual(0, testq.getNumAvailableServers())

        # now complete a service on Server2 and advance customers. Customer[3]
        # should then enter service with Server2

        srvr: Server = testq._servers['Server2']
        exp = list(self.cust[1].getExperiences().values())[0]
        fincust = srvr._completeService(exp.serviceEntryTime + 200)
        self.assertTrue(isinstance(fincust, Customer))
        self.assertEqual(2, testq.getNumBusyServers())
        self.assertEqual(1, testq.getNumAvailableServers())
        self.assertListEqual(self.servers[1:2], list(testq._getAvailableServers().values()))
        self.assertEqual(3, testq.getNumCustomersWaiting())

        # now see if we can advance any customers - should advance Customer[3]
        self.assertTrue(testq._advanceCustomers(3000))
        self.assertEqual(0, testq.getNumAvailableServers())
        exp = list(self.cust[3].getExperiences().values())[0]
        self.assertEqual(self.servers[1].id, exp.serverId)
        self.assertEqual(2, testq.getNumCustomersWaiting())

        # # advance customers and retest
        # testq._advanceCustomers(1000)
        # self.assertEqual(1, testq.getNumAvailableServers())
        # self.assertListEqual(self.servers[2:], list(testq._getAvailableServers().values()))
        # self.assertEqual(0, testq.getNumCustomersWaiting())
        # self.assertEqual(2, testq.getNumBusyServers())
        #
        # for i in range(2):
        #     with self.subTest(i=i):
        #         temp : Experience = list(self.cust[i].getExperiences().values())[0]
        #         self.assertAlmostEqual(1000, temp.serviceEntryTime)
        #
        # # add and advance another customer
        # self.cust[2].logArrival(self.cust[2].systemArrivalTime, testq.id)
        # testq._buffer.append(self.cust[2])
        # self.assertEqual(1, testq.getNumCustomersWaiting())
        # self.assertTrue(testq._advanceCustomers(2000))
        # self.assertEqual(0, testq.getNumCustomersWaiting())
        # self.assertEqual(3, testq.getNumBusyServers())
        #
        # self.assertAlmostEqual(2000, list(self.cust[2].getExperiences().values())[0].serviceEntryTime)

        # attempt
        # self.assertListEqual(self.servers[1:], testq._getAvailableServers())
        #
        # # put Server 3 into service and retest
        # self.cust[1].logArrival(self.cust[1].systemArrivalTime, testq.id)
        # testq._servers[self.servers[2].id].acceptCustomer(self.cust[1].systemArrivalTime, self.cust[1])
        # self.assertEqual(len(self.servers) - 2, testq.getNumAvailableServers())
        #
        # self.assertListEqual(self.servers[1:2], testq._getAvailableServers())
        #
        # # finally, place Server 2 into service
        #
        # self.cust[2].logArrival(self.cust[2].systemArrivalTime, testq.id)
        # testq._servers[self.servers[1].id].acceptCustomer(self.cust[2].systemArrivalTime, self.cust[2])
        # self.assertEqual(0, testq.getNumAvailableServers())
        #
        # self.assertListEqual([], testq._getAvailableServers())

    def test_getNextEventTime(self):
        # first, set up the SimQueue
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignInSequence

        # add servers and destinations
        for dest in self.dest:
            testq.addCustomerDestination(dest)

        for srvr in self.servers:
            testq.addServer(srvr)

        self.assertTrue(testq.isValid())

        # figure out first event time (all downTimes at this point)
        nextEventTimes = [srvr.getNextEventTime() for srvr in self.servers]
        expNext = min(nextEventTimes)

        self.assertAlmostEqual(expNext, testq.getNextEventTime())
        # self.assertEqual(QueueEvent.SERVER_DOWN, testq.getNextEventType())

        # Place Server1 in service
        rstate = np.random.get_state()
        expSvcCompTime1 = self.cust[0].systemArrivalTime + self.servers[0]._serviceTimeDistribution.getEvent()
        np.random.set_state(rstate)

        testq.acceptArrival(self.cust[0].systemArrivalTime, self.cust[0])
        nextEventTimes = [srvr.getNextEventTime() for srvr in self.servers]
        self.assertAlmostEqual(expSvcCompTime1, self.servers[0].getNextEventTime())
        self.assertAlmostEqual(expSvcCompTime1, testq.getNextEventTime())
        # self.assertEqual(QueueEvent.SERVICE_COMPLETION, testq.getNextEventType())
        # print(testq._analyzeNextEvent())

        # now, complete service and recheck
        self.servers[0]._completeService(expSvcCompTime1)
        self.assertAlmostEqual(expNext, testq.getNextEventTime())
        # self.assertEqual(QueueEvent.SERVER_DOWN, testq.getNextEventType())

    def test_processEvent1(self):
        # first, set up the SimQueue
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignInSequence

        # add servers and a single SystemExit
        testq.addCustomerDestination(self.dest[3])
        self.assertEqual('Exit1', self.dest[3].id)

        for srvr in self.servers:
            testq.addServer(srvr)

        self.assertTrue(testq.isValid())

        # figure out first event time (all downTimes at this point)
        nextEventTimes = [srvr.getNextEventTime() for srvr in self.servers]
        nextEventTimesSorted = sorted(nextEventTimes)
        # print(nextEventTimes)
        downTime = nextEventTimesSorted[0]
        downTime2 = nextEventTimesSorted[1]

        self.assertAlmostEqual(downTime, testq.getNextEventTime())
        self.assertEqual(QueueEvent.SERVER_DOWN, testq.getNextEventType())

        # Place Server1 in service
        rstate = np.random.get_state()
        expSvcCompTime1 = self.cust[0].systemArrivalTime + self.servers[0]._serviceTimeDistribution.getEvent()
        np.random.set_state(rstate)

        testq.acceptArrival(self.cust[0].systemArrivalTime, self.cust[0])
        nextEventTimes = [srvr.getNextEventTime() for srvr in self.servers]
        self.assertAlmostEqual(expSvcCompTime1, self.servers[0].getNextEventTime())
        self.assertAlmostEqual(expSvcCompTime1, testq.getNextEventTime())
        self.assertEqual(QueueEvent.SERVICE_COMPLETION, testq.getNextEventType())

        # now, complete service and recheck
        rslt1 = testq.processEvent(expSvcCompTime1)
        self.assertTrue(isinstance(rslt1, Customer))
        self.assertAlmostEqual(downTime, testq.getNextEventTime())
        self.assertEqual(QueueEvent.SERVER_DOWN, testq.getNextEventType())
        se: SystemExit = self.dest[3]
        self.assertEqual(1, len(se._customers))

        #nextEventTimes =  [srvr.getNextEventTime() for srvr in self.servers]

        # try to process an event prematurely

        earlyTime = testq.getNextEventTime() - 100
        rslt2 = testq.processEvent(earlyTime)
        self.assertTrue(rslt2 is None)
        self.assertAlmostEqual(downTime, testq.getNextEventTime())

        # next event should be a server down on server 2, so let's get the return
        # to service time to process the events
        rstate = np.random.get_state()
        expUpTime = self.servers[1]._nextDownTime + self.servers[1]._oosDistribution.getEvent()
        np.random.set_state(rstate)

        rslt3 = testq.processEvent(downTime)
        self.assertTrue(rslt3 is None)
        self.assertAlmostEqual(expUpTime, testq.getNextEventTime())
        self.assertEqual(ServerState.OOS, self.servers[1].status)

        # processing the next event should return Server 2 to service at nextUpTime
        rstate = np.random.get_state()
        nextDownTime = expUpTime + self.servers[1]._downTimeDistribution.getEvent()
        np.random.set_state(rstate)

        rslt4 = testq.processEvent(expUpTime)
        self.assertTrue(rslt4 is None)

        nextEventTimes =  [srvr.getNextEventTime() for srvr in self.servers]

        self.assertAlmostEqual(downTime2, testq.getNextEventTime())
        self.assertTrue(self.servers[1].isAvailable)

    def test_processEvent2(self):
        # first, set up the SimQueue
        testq = copy.deepcopy(self.testq)
        testq._assignServer = Assigner().assignInSequence

        # add servers and two queues as destinations
        for i in range(2):
            testq.addCustomerDestination(self.dest[i])

        for srvr in self.servers:
            testq.addServer(srvr)

        self.assertTrue(testq.isValid())

        downTimes = [srvr._nextDownTime for srvr in self.servers]

        # Have 1st 5 customers arrive
        expSvcCompTime1 = [0, 0, 0, 0, 0]
        rstate = np.random.get_state()

        for i in range(3):
            expSvcCompTime1[i] = self.cust[i].systemArrivalTime + self.servers[i]._serviceTimeDistribution.getEvent()

        # in this test, customers 4 and 5 will enter service immediately after
        # customers 1 and 2 exit, even though they technically haven't arrived yet.
        expSvcCompTime1[3] = expSvcCompTime1[0] + self.servers[0]._serviceTimeDistribution.getEvent()
        expSvcCompTime1[4] = expSvcCompTime1[3] + self.servers[0]._serviceTimeDistribution.getEvent()

        svcCompOrder = np.argsort(expSvcCompTime1)

        np.random.set_state(rstate)

        for i in range(5):
            testq.acceptArrival(self.cust[i].systemArrivalTime, self.cust[i])

        nextEventTimes = [expSvcCompTime1[i] for i in svcCompOrder]
        # print(f'Event times:  {nextEventTimes}')
        # print(f'Svc comp times:  {expSvcCompTime1}')

        self.assertAlmostEqual(min(expSvcCompTime1), testq.getNextEventTime())
        # self.assertEqual(QueueEvent.SERVICE_COMPLETION, testq.getNextEventType())
        self.assertEqual(2, testq.getNumCustomersWaiting())
        self.assertEqual(3, testq.getNumBusyServers())

        # now, complete service on the first 3 customers and recheck
        rslt = []
        for i in range(3):
            with self.subTest(i=i):
                rslt.append(testq.processEvent(expSvcCompTime1[svcCompOrder[i]]))
                self.assertTrue(isinstance(rslt[i], Customer))

                self.assertAlmostEqual(nextEventTimes[i+1], testq.getNextEventTime())

        self.assertEqual(0, testq.getNumCustomersWaiting())
        self.assertEqual(2, testq.getNumBusyServers())

        # now complete service on the last 2 customers
        for i in range(3,5):
            with self.subTest(i=i):
                rslt.append(testq.processEvent(expSvcCompTime1[svcCompOrder[i]]))
                self.assertTrue(isinstance(rslt[i], Customer))

                if i == 3:
                    self.assertAlmostEqual(nextEventTimes[i + 1], testq.getNextEventTime())
                else:
                    self.assertAlmostEqual(min(downTimes), testq.getNextEventTime())

        self.assertEqual(0, testq.getNumCustomersWaiting())
        self.assertEqual(0, testq.getNumBusyServers())
        self.assertEqual(3, testq.getNumAvailableServers())

if __name__ == '__main__':
    main(verbosity=2)
