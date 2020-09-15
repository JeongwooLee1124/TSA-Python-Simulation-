from enum import Enum
from ServerState import ServerState
from ServerEvent import ServerEvent
from Experience import Experience
from Customer import Customer
from Distribution import Distribution
from Server import Server
import numpy as np
import copy as cp

dist = {}
dist['dt'] = Distribution("triangular(14400, 14400, 18000)")
dist['oos'] = Distribution("triangular(300, 600, 1200)")
dist['st'] = Distribution("exponential(1/300)")
dist['invalid'] = Customer('teddy', 0)
server = Server('S1', 100, dist['dt'], dist['oos'], dist['st'])

ServerState.AVAILABLE == server.status

rstate = np.random.get_state()
svcEntryTime = 200
expSvcCompTime = svcEntryTime + dist['st'].getEvent()
np.random.set_state(rstate)

# next, transition to Busy
cust1 = Customer('test1', 100)
cust1.logArrival(100, 'Q1')
server.acceptCustomer(200, cust1)
ServerState.BUSY == server.status
expSvcCompTime == server.getNextEventTime()

# next, complete service and transition to available
server.processEvent(expSvcCompTime)
self.assertEqual(ServerState.AVAILABLE, server.status)
self.assertAlmostEqual(self.server._nextDownTime, self.server._nextEventTime)







np.random.seed(100)
expected = dist['dt'].getEvent()

np.random.seed(100)
actual = server._downTimeDistribution.getEvent()


np.random.seed(200)
expected = np.random.normal(100, 30)

np.random.seed(200)
server.downTimeDistribution = Distribution("normal(100,30)")
actual = server._downTimeDistribution.getEvent()
self.assertAlmostEqual(expected, actual)