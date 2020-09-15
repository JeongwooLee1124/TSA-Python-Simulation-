import math
from unittest import TestCase, main
from Experience import Experience

def createExpected(stageId, queueEntryTime, serverId,
                   serviceEntryTime, serviceCompletionTime):
    return {'stageId': stageId,
            'queueEntryTime': queueEntryTime,
            'serverId': serverId,
            'serviceEntryTime': serviceEntryTime,
            'serviceCompletionTime': serviceCompletionTime
            }

class TestExperience(TestCase):
    def setUp(self) -> None:
        # define expected results
        self.expected = list()

        self.expected.append(createExpected('1', 100, 'S1', 150, 165))
        self.expected.append(createExpected('Stage 2', 200, 2, 255, 275))
        self.expected.append(createExpected(3, 300, 'Register 1', 360, 385))

        # add waiting and system times
        for x in self.expected:
            x['waitingTime'] = x['serviceEntryTime'] - x['queueEntryTime']
            x['systemTime'] = x['serviceCompletionTime'] - x['queueEntryTime']

        # Now construct the experience instances to be tested
        self.experience = list()
        for e in self.expected:
            self.experience.append(Experience(e['stageId'], e['queueEntryTime']))


    def test_init(self):
        for i in range(len(self.expected)):
            with self.subTest(i=i):
                self.assertEqual(self.expected[i]['stageId'], self.experience[i]._stageId)
                self.assertEqual(self.expected[i]['queueEntryTime'], self.experience[i]._queueEntryTime)

        self.assertTrue(isinstance(self.experience[i].__str__(), str))
        self.assertTrue(isinstance(self.experience[i].__repr__(), str))

    def test_getters(self):
        for i in range(len(self.expected)):
            with self.subTest(i=i):
                stageId = self.experience[i].stageId

                # if the stageID is a string, we can't test using math.isnan, so we'll
                # check that it has a non-zero length. If it's not a string, then
                # we'll test for nan

                if isinstance(stageId, str):
                    self.assertTrue(len(stageId) > 0)
                else:
                    self.assertFalse(math.isnan(self.experience[i].stageId))

                self.assertFalse(math.isnan(self.experience[i].queueEntryTime))
                self.assertTrue(math.isnan(self.experience[i].serverId))
                self.assertTrue(math.isnan(self.experience[i].serviceEntryTime))
                self.assertTrue(math.isnan(self.experience[i].waitingTime))
                self.assertTrue(math.isnan(self.experience[i].serviceCompletionTime))
                self.assertTrue(math.isnan(self.experience[i].systemTime))

        for i in range(len(self.experience)):
            with self.subTest(i=i):
                self.experience[i].logServiceEntry(self.expected[i]['serverId'],
                                                   self.expected[i]['serviceEntryTime'])

                if isinstance(self.expected[i]['serverId'], str):
                    self.assertTrue(len(self.experience[i].serverId) > 0)
                else:
                    self.assertFalse(math.isnan(self.experience[i].serverId))

                self.assertFalse(math.isnan(self.experience[i].serviceEntryTime))
                self.assertFalse(math.isnan(self.experience[i].waitingTime))
                self.assertTrue(math.isnan(self.experience[i].serviceCompletionTime))
                self.assertTrue(math.isnan(self.experience[i].systemTime))

        for i in range(len(self.experience)):
            with self.subTest(i=i):
                self.experience[i].logServiceCompletion(self.expected[i]['serviceCompletionTime'])

                if isinstance(self.expected[i]['serverId'], str):
                    self.assertTrue(len(self.experience[i].serverId) > 0)
                else:
                    self.assertFalse(math.isnan(self.experience[i].serverId))

                self.assertFalse(math.isnan(self.experience[i].serviceEntryTime))
                self.assertFalse(math.isnan(self.experience[i].waitingTime))
                self.assertFalse(math.isnan(self.experience[i].serviceCompletionTime))
                self.assertFalse(math.isnan(self.experience[i].systemTime))


    def test_logServiceEentry(self):
        # set up expected service entry data (serverId, serviceEntryTime)

        for i in range(len(self.expected)):
            with self.subTest(i=i):
                # verify that serverId and serviceEntryTime are updated correctly
                self.experience[i].logServiceEntry(self.expected[i]['serverId'],
                                                   self.expected[i]['serviceEntryTime'])
                self.assertEqual(self.expected[i]['serverId'], self.experience[i].serverId)
                self.assertAlmostEqual(self.expected[i]['serviceEntryTime'], self.experience[i].serviceEntryTime)

                # verify that waiting time is calculated correctly
                self.assertAlmostEqual(self.expected[i]['waitingTime'], self.experience[i].waitingTime)

                # verify that systemTime and serviceCompletionTime are currently undefined
                self.assertTrue(math.isnan(self.experience[i].serviceCompletionTime))
                self.assertTrue(math.isnan(self.experience[i].systemTime))

    def test_logServiceCompletion(self):
        # set up expected service entry data (serverId, serviceEntryTime)

        for i in range(len(self.expected)):
            with self.subTest(i=i):
                # verify that serverId and serviceEntryTime are updated correctly
                self.experience[i].logServiceEntry(self.expected[i]['serverId'],
                                                   self.expected[i]['serviceEntryTime'])
                self.experience[i].logServiceCompletion(self.expected[i]['serviceCompletionTime'])

                # verify that systemTime and serviceCompletionTime are correct
                self.assertAlmostEqual(self.expected[i]['serviceCompletionTime'],
                                       self.experience[i].serviceCompletionTime)
                self.assertAlmostEqual(self.expected[i]['systemTime'],
                                       self.experience[i].systemTime)

    def test_makeRow(self):
        for i in range(len(self.experience)):
            with self.subTest(i=i):
                self.assertEqual(self.expected[i]['stageId'], self.experience[i].stageId)


if __name__ == '__main__':
    main(verbosity=2)
