from Simulation import Simulation
from Customer import Customer
import pandas as pd
import numpy as np

class SimulationAnalysis:
    """
    Performs analysis on a completed simulation. Accepts a Simulation instance
    at construction and performs analysis on that simulation instance.
    """
    def __init__(self, simulation):
        #todo implement __init__
        if not isinstance(simulation, Simulation):
            # argument is not a Simulation instance, so this SimulationAnalysis
            # instance is invalid
            self._sim = None
            self._analysis = None

        # The argument is a simulation - proceed with the analysis
        self._sim = simulation

        if self._sim.getTrialsCompleted() <= 0:
            # there are no completed trials for this simulation, cannot
            # perform the analysis
            self._analysis = None
            self._custdf = None

        # We have trials, we're in business - time to construct the dataframe
        # of results
        custstats = [[cust.name, cust.totalWaitTime, cust.totalSystemTime] for cust in self._sim]

        self._custdf = pd.DataFrame(custstats, columns = ['Name', 'WaitTime', 'SystemTime'])

        # now construct the dictionary with the analysis results
        self._analysis = {}

        # use DataFrame functions to calculate percentiles, means, max
        percentiles = self._custdf.quantile(.9, interpolation='higher')
        averages = self._custdf.mean()
        maxs = self._custdf.max()

        # assign results to analysis dictionary for returning

        self._analysis['NumCustomers'] = len(self._custdf)
        self._analysis['AvgWaitTime'] = averages['WaitTime']
        self._analysis['MaxWaitTime'] = maxs['WaitTime']
        self._analysis['AvgSystemTime'] = averages['SystemTime']
        self._analysis['MaxSystemTime'] = maxs['SystemTime']
        self._analysis['90%WaitTime'] = percentiles['WaitTime']
        self._analysis['90%SystemTime'] = percentiles['SystemTime']

        self._compareResult = dict()

    @property
    def customerSummary(self):
        """
        A Pandas Dataframe containing a single row for each Customer who comleted
        service in the system. Columns include Name, total WaitTime, total SystemTime
        @return: Dataframe
        """
        if self.isValid():
            return self._custdf
        else:
            return None

    @property
    def sim(self):
        return self._sim

    def analyzeSystemPerformance(self):
        """
        Analyzes a completed Simulation's performance, returning a
        @return:
        """
        # Actually, the analysis is done (it was done on construction)
        # All that's required here is to return the analysis dictionary.
        # Since the results can't change (the simulation is DONE),
        # This approach is more efficient, ensuring the calculations are
        # completed only one time, regardless of the number of times
        # analyzeSystemPerformance is called.

        return self._analysis

    def comparePerformance(self, compareTo):
        #todo implement comparePerformance
        if isinstance(compareTo, Simulation):
            if compareTo.simtime == 0:
                compareTo.run(500)
            compareRes = SimulationAnalysis(compareTo)
            for key in self._analysis:
                self._compareResult[key] = self._analysis[key] - compareRes._analysis[key]

        return self._compareResult

    def isValid(self):
        if self._sim is None or self._analysis is None:
            return False
        else:
            return True

