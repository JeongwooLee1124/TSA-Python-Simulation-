from unittest import TestCase, main
from SourcePopulation import SourcePopulation
from Distribution import Distribution
from Assigner import Assigner
from CustomerDestination import CustomerDestination
from SimulationStage import SimulationStage
from SimQueue import SimQueue
import numpy as np
import math

# setUp
dist = Distribution('triangular(10, 20, 40)')

# SourcePopulation generates the first arrival time on construction
# so we have to set the random number before creating the source population

np.random.seed(100)
sp = SourcePopulation("Source1", dist, Assigner().assignInSequence)
        
# __init__        

# addCustomerDestination
sp.isValid() == False
dest = CustomerDestination('test_dest')
sp.addCustomerDestination(dest)
sp.isValid() == True
sp.addCustomerDestination(list())


##### processEvent
# add a valid destination to the SourcePopulation
dest = SimQueue('test_dest', Assigner().assignInSequence)
sp.addCustomerDestination(dest) == True

# save the random seed state
rstate = np.random.get_state()

# generate arrival times for validation
np.random.seed(100)
arrival_times = np.random.triangular(10, 20, 40, 10).cumsum()

# reset the seed state
np.random.set_state(rstate)

for i in range(10):
    with self.subTest(i = i):
        self.assertAlmostEqual(arrival_times[i], self.sp.getNextEventTime())
        self.sp.processEvent(self.sp.getNextEventTime())