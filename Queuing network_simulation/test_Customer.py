import math
from unittest import TestCase, main
from Customer import Customer
from Experience import Experience
import numpy as np


class TestCustomer(TestCase):

    def setUp(self) -> None:
        # create 10 customers for use in all tests
        self.names = [f'Cust {i}' for i in range(10)]
        self.arrivalTimes = [(i + 1) * 150 for i in range(10)]

        self.cust = [Customer(self.names[i], self.arrivalTimes[i]) for i in range(10)]

    def test_init(self):

        for i in range(len(self.cust)):
            with self.subTest(i=i):
                self.assertEqual(self.names[i], self.cust[i]._name)
                self.assertEqual(self.arrivalTimes[i], self.cust[i]._systemArrivalTime)
                self.assertTrue(self.cust[i]._currLocation is None)
                self.assertTrue(isinstance(self.cust[i].__repr__(),str))
                self.assertTrue(isinstance(self.cust[i].__str__(),str))

    def test_getters(self):

        for i in range(len(self.cust)):
            with self.subTest(i=i):
                self.assertEqual(self.names[i], self.cust[i].name)
                self.assertEqual(self.arrivalTimes[i], self.cust[i].systemArrivalTime)
                self.assertTrue(self.cust[i].currLocation is None)

    def test_getExperiences(self):

        # first, getting the experience dictionary for all customers
        for i in range(len(self.cust)):
            with self.subTest(i=i):
                self.cust[i]._experience[f'Stage{i}'] = Experience(f'Stage{i}', self.cust[i].systemArrivalTime)
                temp = self.cust[i].getExperiences()
                self.assertEqual(f'Stage{i}', temp[f'Stage{i}'].stageId)
                self.assertAlmostEqual((i + 1) * 150, temp[f'Stage{i}'].queueEntryTime)

        # add additional stages for each customer and verify that we get the right values
        for cust in self.cust:
            with self.subTest(name=cust.name):
                # log arrival at 10 additional stages
                for i in range(10, 20):
                    cust._experience[f'Stage{i}'] = Experience(f'Stage{i}', (i + 1) * 100)

                # The first stage was added differently then
                # subsequent stages, so we need to handle the assertions differently

                init_stages = [f'Stage{k}' for k in range(10)]

                stageId = 10

                for k, v in cust.getExperiences().items():
                    if v.stageId in init_stages:
                        # this is the first stage for the customer
                        self.assertEqual(f'Stage{cust.name[-1]}', v.stageId)
                        self.assertAlmostEqual(cust.systemArrivalTime, v.queueEntryTime)
                    else:
                        # one of the remaining stages
                        self.assertEqual(f'Stage{stageId}', v.stageId)
                        self.assertAlmostEqual((stageId + 1) * 100, v.queueEntryTime)
                        stageId += 1

    def test_getExperienceStatistics(self):
        # we only need to test this on one customer
        np.random.seed(100)
        cust = self.cust[0]
        iaTimes = np.random.triangular(0, 30, 120, 10)
        arrivalTimes = np.add.accumulate(iaTimes)
        waitTimes = np.random.triangular(0, 20, 120, 10)
        svcEntryTimes = arrivalTimes + waitTimes
        svcTimes = np.random.exponential(30, 10)
        completionTimes = svcEntryTimes + svcTimes
        systemTimes = completionTimes - arrivalTimes

        # log customers arrival and service entry at all stages

        for i in range(len(arrivalTimes)):
            cust.logArrival(arrivalTimes[i], f'Stage{i + 1}')
            cust.logServiceEntry(svcEntryTimes[i], f'Server{(i + 1) * 10}')
            cust.logServiceCompletion(completionTimes[i])

        expstat = cust.getExperienceStatistics()
        nexp = expstat.shape[0]

        stageId = [f'Stage{i+1}' for i in range(nexp)]
        serverId = [f'Server{(i+1) * 10}' for i in range(nexp)]

        for i in range(nexp):
            with self.subTest(i=i):
                self.assertEqual(stageId[i], expstat.iloc[i,]['stageId'])
                self.assertEqual(serverId[i], expstat.iloc[i,]['serverId'])
                self.assertAlmostEqual(arrivalTimes[i], expstat.iloc[i,]['queueEntryTime'])
                self.assertAlmostEqual(svcEntryTimes[i], expstat.iloc[i,]['serviceEntryTime'])
                self.assertAlmostEqual(completionTimes[i], expstat.iloc[i,]['serviceCompletionTime'])
                self.assertAlmostEqual(waitTimes[i], expstat.iloc[i,]['waitingTime'])
                self.assertAlmostEqual(systemTimes[i], expstat.iloc[i,]['systemTime'])

    def test_logArrival(self):

        # we only need to test this on one customer
        cust = self.cust[0]
        entryTimes = [cust.systemArrivalTime * (i + 1) for i in range(10)]

        # have customer arrive in 10 stages

        for i in range(len(entryTimes)):
            cust.logArrival(entryTimes[i], f'Stage{i + 1}')

        expdict = cust.getExperiences()

        # use getExperiences (already verified) to test the logged arrives
        for i in range(len(expdict)):
            with self.subTest(i=i):
                stageId = f'Stage{i + 1}'
                self.assertAlmostEqual(entryTimes[i], expdict[stageId].queueEntryTime)

    def test_logServiceCompletion(self):

        # we only need to test this on one customer
        np.random.seed(100)
        cust = self.cust[0]
        iaTimes = np.random.triangular(0, 30, 120, 10)
        arrivalTimes = np.add.accumulate(iaTimes)
        waitTimes = np.random.triangular(0, 20, 120, 10)
        svcEntryTimes = arrivalTimes + waitTimes
        svcTimes = np.random.exponential(30, 10)
        completionTimes = svcEntryTimes + svcTimes
        systemTimes = completionTimes - arrivalTimes

        # log customers arrival and service entry at all stages

        for i in range(len(arrivalTimes)):
            cust.logArrival(arrivalTimes[i], f'Stage{i + 1}')
            cust.logServiceEntry(svcEntryTimes[i], f'Server{(i + 1) * 10}')
            cust.logServiceCompletion(completionTimes[i])

        expdict = cust.getExperiences()

        # use getExperiences (already verified) to test the service entry history
        for i in range(len(expdict)):
            with self.subTest(i=i):
                stageId = f'Stage{i + 1}'
                serverId = f'Server{(i + 1) * 10}'

                self.assertEqual(stageId, expdict[stageId].stageId)
                self.assertEqual(serverId, expdict[stageId].serverId)
                self.assertAlmostEqual(completionTimes[i], expdict[stageId].serviceCompletionTime)
                self.assertAlmostEqual(systemTimes[i], expdict[stageId].systemTime)

        print(self.cust[0].getExperienceStatistics())

    def test_logServiceEntry(self):

        # we only need to test this on one customer
        np.random.seed(100)
        cust = self.cust[0]
        iaTimes = np.random.triangular(0, 30, 120, 10)
        arrivalTimes = np.add.accumulate(iaTimes)
        waitTimes = np.random.triangular(0, 20, 120, 10)
        svcEntryTimes = arrivalTimes + waitTimes
        svcTimes = np.random.exponential(30, 10)
        completionTimes = svcEntryTimes + svcTimes

        # log customers arrival and service entry at all stages

        for i in range(len(arrivalTimes)):
            cust.logArrival(arrivalTimes[i], f'Stage{i + 1}')
            cust.logServiceEntry(svcEntryTimes[i], f'Server{(i + 1) * 10}')

        expdict = cust.getExperiences()

        # use getExperiences (already verified) to test the service entry history
        for i in range(len(expdict)):
            with self.subTest(i=i):
                stageId = f'Stage{i + 1}'
                serverId = f'Server{(i + 1) * 10}'

                self.assertEqual(stageId, expdict[stageId].stageId)
                self.assertEqual(serverId, expdict[stageId].serverId)
                self.assertAlmostEqual(svcEntryTimes[i], expdict[stageId].serviceEntryTime)
                self.assertAlmostEqual(waitTimes[i], expdict[stageId].waitingTime)

    def test_totalTimes(self):

        # first, need to log arrivals, service entries, and completions.
        # will use Customers specific to THIS test rather than the general setup.

        cust = Customer(1, 0)
        cust.logArrival(0, 'Q1')
        cust.logServiceEntry(10, "S1")
        cust.logServiceCompletion(15)

        # at this point waiting time should be 10, system time should be 15
        self.assertAlmostEqual(10, cust.totalWaitTime)
        self.assertAlmostEqual(15, cust.totalSystemTime)

        # add and test another complete stage
        cust.logArrival(15, 'Q2')
        cust.logServiceEntry(30, 'S2')
        cust.logServiceCompletion(55)

        # at this point, total waiting and system time should be 25 and 55
        self.assertAlmostEqual(25, cust.totalWaitTime)
        self.assertAlmostEqual(55, cust.totalSystemTime)

        # now test for some incompletes, add another stage
        cust.logArrival(55, 'Q3')
        self.assertTrue(math.isnan(cust.totalWaitTime))
        self.assertTrue(math.isnan(cust.totalSystemTime))

        # now, log serviceEntry and test again
        cust.logServiceEntry(57, 'S3')
        self.assertFalse(math.isnan(cust.totalWaitTime))
        self.assertTrue(math.isnan(cust.totalSystemTime))

        self.assertAlmostEqual(27, cust.totalWaitTime)

        # finally, log service completion and retest
        cust.logServiceCompletion(72)
        self.assertFalse(math.isnan(cust.totalWaitTime))
        self.assertFalse(math.isnan(cust.totalSystemTime))

        self.assertAlmostEqual(72, cust.totalSystemTime)


if __name__ == '__main__':
    main(verbosity=2)
