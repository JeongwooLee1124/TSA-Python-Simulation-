import math
from unittest import TestCase, main
from Server import Server
from Distribution import Distribution
from ServerState import ServerState
from ServerEvent import ServerEvent
from Customer import Customer
from Experience import Experience
import numpy as np
import copy as cp


class TestServer(TestCase):
    def setUp(self) -> None:
        self.dist = {}
        self.dist['dt'] = Distribution("triangular(14400, 14400, 18000)")
        self.dist['oos'] = Distribution("triangular(300, 600, 1200)")
        self.dist['st'] = Distribution("exponential(1/300)")

        # uncomment to test validity of server construction
        # for k, v in self.dist.items():
        #     with self.subTest(dist=k):
        #         self.assertTrue(v.isValid())

        self.dist['invalid'] = Customer('teddy', 0)

        self.server = Server('S1', 100,
                             self.dist['dt'],
                             self.dist['oos'],
                             self.dist['st']
                             )

    def test_init(self):
        # check a valid instance
        self.assertEqual(ServerState.AVAILABLE, self.server.status)

        # force the id to None and check
        self.server._id = None
        self.assertEqual(ServerState.INVALID, self.server.status)

        # reset the server id and continue testing
        self.server._id = 'S1'

        # check invalid instances
        dist = [('invalid', 'oos', 'st'),
                ('dt', 'invalid', 'st'),
                ('dt', 'oos', 'invalid')]

        for i in range(len(dist)):
            with self.subTest(i=i):
                srvr = Server(i, i * 10, dist[i][0], dist[i][1], dist[i][2])
                self.assertTrue(srvr.status == ServerState.INVALID)

    def test_cust_in_svc(self):
        cust = Customer('Johnny', 100)
        cust.logArrival(100, 'Q1')
        self.server.acceptCustomer(100, cust)
        self.assertEqual(cust.name, self.server.custInSvc)

    def test_downTimeDistribution(self):
        np.random.seed(100)
        expected = self.dist['dt'].getEvent()

        np.random.seed(100)
        actual = self.server._downTimeDistribution.getEvent()
        self.assertAlmostEqual(expected, actual)

        # replace the downtime distribution and check
        np.random.seed(200)
        expected = np.random.normal(100, 30)

        np.random.seed(200)
        self.server.downTimeDistribution = Distribution("normal(100,30)")
        actual = self.server._downTimeDistribution.getEvent()
        self.assertAlmostEqual(expected, actual)

    def test_id(self):
        self.assertEqual('S1', self.server.id)

        self.server._id = 100

        self.assertEqual(100, self.server.id)

    def test_oosDistribution(self):
        np.random.seed(100)
        expected = self.dist['oos'].getEvent()

        np.random.seed(100)
        actual = self.server._oosDistribution.getEvent()
        self.assertAlmostEqual(expected, actual)

        # replace the downtime distribution and check
        np.random.seed(200)
        expected = np.random.normal(100, 30)

        np.random.seed(200)
        self.server.oosDistribution = Distribution("normal(100,30)")
        actual = self.server._oosDistribution.getEvent()
        self.assertAlmostEqual(expected, actual)

    def test_status(self):
        # initial status of the valid Server should be Available
        # state 1 - Available
        self.assertEqual(ServerState.AVAILABLE, self.server.status)

        # make a "test" copy of the Server instance so we can force change its internal state
        # and test the status property
        test = cp.deepcopy(self.server)

        # state 2 - pending OOS
        test._nextDownTime = 2000
        test._nextEventTime = 10000
        self.assertTrue(ServerState.PENDING_OOS, test.status)

        # state 3 OOS
        # nextEventTime
        test._nextEventTime = 12000
        test._nextDownTime = 3000
        test._nextEventType = ServerEvent.SERVER_UP

        self.assertEqual(ServerState.OOS, test.status)

        # state 4
        test._custInSvc = None
        test._nextEventType = ServerEvent.SERVER_UP
        test._nextDownTime = 2000
        test._nextEventTime = 10000

        self.assertTrue(ServerState.INVALID, test.status)

        # state 5
        self._nextEventType = ServerEvent.SERVICE_COMPLETION
        self.assertTrue(ServerState.INVALID, test.status)

        # state 6
        self._nextDownTime = 12000
        self.assertTrue(ServerState.INVALID, test.status)

        # state 7
        test._custInSvc = Customer('dummy', 100)
        test._nextEventType = ServerEvent.SERVER_DOWN
        test._nextDownTime = 2000
        test._nextEventTime = 10000
        self.assertTrue(ServerState.INVALID, test.status)

        # state 8
        test._nextEventTime = 12000
        self.assertTrue(ServerState.INVALID, test.status)

        # state 9
        test._nextEventType = ServerEvent.SERVER_UP
        test._nextDownTime = 2000
        self.assertTrue(ServerState.INVALID, test.status)

        # state 10
        test._nextDownTime = 12000
        self.assertTrue(ServerState.INVALID, test.status)

        # state 11 - busy
        test._custInSvc = Customer('dummy', 100)
        test._nextEventType = ServerEvent.SERVICE_COMPLETION
        test._nextEventTime = 10000
        test._nextDownTime = 2000

        self.assertEqual(ServerState.BUSY, test.status)

        # state 12 - busy
        test._nextDownTime = 12000

        self.assertEqual(ServerState.BUSY, test.status)

    def test_isAvailable(self):
        # initial status of the valid Server should be Available
        # state 1 - Available
        self.assertTrue(self.server.isAvailable)

        # make a "test" copy of the Server instance so we can force change its internal state
        # and test the status property
        test = cp.deepcopy(self.server)

        # state 2
        test._nextDownTime = 2000
        test._nextEventTime = 10000
        self.assertFalse(test.isAvailable)

        # state 3 OOS
        # nextEventTime
        test._nextEventTime = 12000
        test._nextDownTime = 3000
        test._nextEventType = ServerEvent.SERVER_UP

        self.assertFalse(test.isAvailable)

        # state 11 - pending OOS
        test._custInSvc = Customer('dummy', 100)
        test._nextEventType = ServerEvent.SERVICE_COMPLETION
        test._nextEventTime = 10000
        test._nextDownTime = 2000

        self.assertFalse(test.isAvailable)

        # state 12 - busy
        test._nextDownTime = 12000

        self.assertFalse(test.isAvailable)

    def test_nextEventTime(self):
        self.assertEqual(ServerState.AVAILABLE, self.server.status)
        self.server._nextDownTime = 10000
        self.server._nextEventTime = self.server._nextDownTime

        self.assertAlmostEqual(10000, self.server.nextEventTime)
        self.assertAlmostEqual(10000, self.server.getNextEventTime())

    def test_serviceTimeDistribution(self):
        np.random.seed(100)
        expected = self.dist['st'].getEvent()

        np.random.seed(100)
        actual = self.server._serviceTimeDistribution.getEvent()
        self.assertAlmostEqual(expected, actual)

        # replace the downtime distribution and check
        np.random.seed(200)
        expected = np.random.normal(100, 30)

        np.random.seed(200)
        self.server.serviceTimeDistribution = Distribution("normal(100,30)")
        actual = self.server._serviceTimeDistribution.getEvent()
        self.assertAlmostEqual(expected, actual)

    # The following tests are specific to the sample solutions classes.
    # def test_transition_actions(self):
    #     # first, verify Server is available
    #     self.assertEqual(ServerState.AVAILABLE, self.server.status)
    #
    #     # next, transition to Busy
    #     cust = Customer('test1', 100)
    #     cust.logArrival(100, 'Q1')
    #     self.server._setBusy(200, cust)
    #     self.assertEqual(ServerState.BUSY, self.server.status)
    #     self.assertTrue(math.isinf(self.server.availableSince))
    #
    #     # next, complete service and transition to available
    #     self.server._setAvailable(300)
    #     self.assertEqual(ServerState.AVAILABLE, self.server.status)
    #     self.assertEqual(300, self.server.availableSince)
    #
    #     # verify customer experience
    #     exp: Experience = list(cust.getExperiences().values())[0]
    #     self.assertEqual(100, exp.queueEntryTime)
    #     self.assertEqual(200, exp.serviceEntryTime)
    #     self.assertTrue(math.isnan(exp.serviceCompletionTime))
    #
    #     cust = Customer('test2', 500)
    #     cust.logArrival(500, 'Q1')
    #
    #     self.server._setBusy(600, cust)
    #     self.assertTrue(math.isinf(self.server.availableSince))
    #     self.assertEqual(ServerState.BUSY, self.server.status)
    #
    #     # ensure that the Server is PendingOOS so we can make the transition
    #     self.server._nextDownTime = self.server._nextEventTime - 1
    #     self.assertEqual(ServerState.BUSY, self.server.status)
    #
    #     # make transition to pendingOOS
    #     self.server._setPendingOOS(700)
    #     self.assertEqual(ServerState.PENDING_OOS, self.server.status)
    #     self.assertTrue(math.isinf(self.server.availableSince))
    #
    #     # now, make the transition to OOS
    #     self.server._setOOS(700)
    #     self.assertEqual(ServerState.OOS, self.server.status)
    #
    #     # now, make the transition back to Available
    #     availableTime = self.server.nextEventTime
    #     self.server._setAvailable(availableTime)
    #     self.assertEqual(ServerState.AVAILABLE, self.server.status)
    #     self.assertAlmostEqual(availableTime, self.server.availableSince)
    #
    # def test_complete_service(self):
    #     # first, verify Server is available
    #     self.assertEqual(ServerState.AVAILABLE, self.server.status)
    #
    #     # next, transition to Busy
    #     cust = Customer('cust1', 100)
    #     cust.logArrival(100, 'Q1')
    #     self.server._setBusy(200, cust)
    #     self.assertEqual(ServerState.BUSY, self.server.status)
    #     self.assertTrue(math.isinf(self.server.availableSince))
    #
    #     # next, complete service and transition to available
    #     self.server._completeService(300)
    #     self.assertEqual(ServerState.AVAILABLE, self.server.status)
    #     self.assertAlmostEqual(300, self.server.availableSince)
    #
    #     # verify customer experience
    #     exp: Experience = list(cust.getExperiences().values())[0]
    #     self.assertEqual(100, exp.queueEntryTime)
    #     self.assertEqual(200, exp.serviceEntryTime)
    #     self.assertEqual(300, exp.serviceCompletionTime)
    #
    #     # now, test transition to pendingOOS when completing service
    #     cust2 = Customer('cust2', 500)
    #     cust2.logArrival(600, 'Q1')
    #     self.server._setBusy(700, cust2)
    #     self.assertTrue(math.isinf(self.server.availableSince))
    #     self.assertEqual(ServerState.BUSY, self.server.status)
    #
    #     # force downtime < eventtime (i.e. service completion time), so that Server should
    #     # go pendingOOS as a result of completing service
    #     self.server._nextDownTime = self.server._nextEventTime - 1
    #     self.server._completeService(self.server._nextEventTime)
    #     self.assertTrue(math.isinf(self.server.availableSince))
    #     self.assertEqual(ServerState.PENDING_OOS, self.server.status)
    #
    #     # Now, complete OOS period
    #     availableTime = self.server._nextEventTime
    #     self.server._setAvailable(availableTime)
    #     self.assertAlmostEqual(availableTime, self.server.availableSince)
    #     self.assertEqual(ServerState.AVAILABLE, self.server.status)

    def test_acceptCustomer(self):
        rstate = np.random.get_state()

        cust1 = Customer('cust1', 100)
        cust1.logArrival(100, 'Q1')
        svcEntryTime = 200
        expectedSvcComp = svcEntryTime + self.dist['st'].getEvent()

        # reset the random seed
        np.random.set_state(rstate)

        # accept a valid customer
        self.assertTrue(self.server.acceptCustomer(svcEntryTime, cust1))
        self.assertAlmostEqual(expectedSvcComp, self.server.nextEventTime)
        self.assertAlmostEqual(expectedSvcComp, self.server.getNextEventTime())

        # still in service, reject the next valid customer
        cust2 = Customer('cust2', 250)
        self.assertFalse(self.server.acceptCustomer(250, cust2))

        # complete service and server becomes available
        self.assertTrue(isinstance(self.server._completeService(expectedSvcComp), Customer))
        self.assertTrue(self.server.isAvailable)
        custexp = list(cust1.getExperiences().values())[0]
        self.assertAlmostEqual(custexp.serviceEntryTime, svcEntryTime)
        self.assertAlmostEqual(custexp.serviceCompletionTime, expectedSvcComp)

        # make invalid acceptCustomer request (i.e. pass something other than a Customer)
        self.assertFalse(self.server.acceptCustomer(1000, 15))

    def test_processEvent(self):
        # first, verify Server is available
        self.assertEqual(ServerState.AVAILABLE, self.server.status)

        rstate = np.random.get_state()
        svcEntryTime = 200
        expSvcCompTime = svcEntryTime + self.dist['st'].getEvent()
        np.random.set_state(rstate)

        # next, transition to Busy
        cust1 = Customer('test1', 100)
        cust1.logArrival(100, 'Q1')
        self.assertTrue(self.server.acceptCustomer(200, cust1))
        self.assertEqual(ServerState.BUSY, self.server.status)
        self.assertAlmostEqual(expSvcCompTime, self.server.getNextEventTime())

        # next, complete service and transition to available
        self.server.processEvent(expSvcCompTime)
        self.assertEqual(ServerState.AVAILABLE, self.server.status)
        self.assertAlmostEqual(self.server._nextDownTime, self.server._nextEventTime)

        # verify customer experience
        exp: Experience = list(cust1.getExperiences().values())[0]
        self.assertAlmostEqual(100, exp.queueEntryTime)
        self.assertAlmostEqual(200, exp.serviceEntryTime)
        self.assertAlmostEqual(expSvcCompTime, exp.serviceCompletionTime)

        # check putting server OOS
        expDownTime = self.server._nextDownTime

        rstate = np.random.get_state()
        resumeTime = expDownTime + self.dist['oos'].getEvent()
        np.random.set_state(rstate)

        self.assertEqual(ServerEvent.SERVER_DOWN, self.server.nextEventType)
        self.assertTrue(self.server.processEvent(expDownTime) is None)
        self.assertEqual(ServerState.OOS, self.server.status)
        self.assertAlmostEqual(resumeTime, self.server.getNextEventTime())

        # now, process event to return Server to service
        rstate = np.random.get_state()
        nextDownTime = resumeTime + self.dist['dt'].getEvent()
        np.random.set_state(rstate)
        self.assertTrue(self.server.processEvent(resumeTime) is None)
        self.assertEqual(ServerState.AVAILABLE, self.server.status)
        self.assertAlmostEqual(nextDownTime, self.server._nextDownTime)
        self.assertAlmostEqual(nextDownTime, self.server.getNextEventTime())

        # now, we'll put a customer into service, ensure that the server should
        # go OOS after service completion, and verify the event processing

        cust2 = Customer('cust2', resumeTime + 1)
        cust2.logArrival(cust2.systemArrivalTime, 'Q1')

        rstate = np.random.get_state()
        svcCompTime = cust2.systemArrivalTime + self.dist['st'].getEvent()
        resumeTime2 = svcCompTime + self.dist['oos'].getEvent()
        np.random.set_state(rstate)

        # place customer into service
        self.assertTrue(self.server.acceptCustomer(cust2.systemArrivalTime, cust2))
        self.assertTrue(self.server.isBusy)
        self.assertAlmostEqual(svcCompTime, self.server.getNextEventTime())

        # force nextDownTime < svcCompTime
        self.server.pauseService(svcCompTime - 1)
        self.assertAlmostEqual(svcCompTime - 1, self.server._nextDownTime)

        # when we process the next event, we should 1) get a customer back
        # and go PENDING_OOS
        self.assertFalse(self.server.processEvent(svcCompTime) is None)
        self.assertEqual(ServerState.PENDING_OOS, self.server.status)

        # verify customer experience
        exp: Experience = list(cust2.getExperiences().values())[0]
        self.assertAlmostEqual(cust2.systemArrivalTime, exp.queueEntryTime)
        self.assertAlmostEqual(cust2.systemArrivalTime, exp.serviceEntryTime)
        self.assertAlmostEqual(svcCompTime, exp.serviceCompletionTime)

        # now, process the next event. This should place the server OOS
        rstate = np.random.get_state()
        resumeTime3 = svcCompTime + self.dist['oos'].getEvent()
        np.random.set_state(rstate)

        self.assertTrue(self.server.processEvent(svcCompTime) is None)
        self.assertEqual(ServerState.OOS, self.server.status)
        self.assertAlmostEqual(resumeTime3, self.server.getNextEventTime())

        # finally, return to service
        rstate = np.random.get_state()
        nextDownTime2 = resumeTime3 + self.dist['dt'].getEvent()
        np.random.set_state(rstate)

        self.assertTrue(self.server.processEvent(resumeTime3) is None)
        self.assertTrue(self.server.isAvailable)
        self.assertAlmostEqual(nextDownTime2, self.server.getNextEventTime())
        self.assertEqual(ServerEvent.SERVER_DOWN, self.server._nextEventType)

if __name__ == '__main__':
    main(verbosity=2)


