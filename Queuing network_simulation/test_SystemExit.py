from unittest import TestCase, main
from SystemExit import SystemExit
from Customer import Customer
import numpy as np


class TestSystemExit(TestCase):

    def setUp(self) -> None:
        self.se = SystemExit('SE1')

    def test_init(self):
        self.assertEqual('SE1', self.se.id)
        self.assertEqual(0, len(self.se._customers))

    def test_get_num_customers_waiting(self):
        self.assertEqual(0, self.se.getNumCustomersWaiting())

        # add some customers into the list and verify that the
        # number of customers waiting is still 0
        self.se._customers.update({'a': Customer('C1', 0), 'b': Customer('C2',10)})
        self.assertEqual(2, len(self.se._customers))
        self.assertEqual(0, self.se.getNumCustomersWaiting())

    def test_is_valid(self):
        self.assertTrue(self.se.isValid())

        # add some customers into the list and verify that the
        # number of customers waiting is still 0
        self.se._customers.update({'a': Customer('C1', 0), 'b': Customer('C2',10)})
        self.assertTrue(self.se.isValid())

    def test_accept_arrival(self):
        # create 10 customers for use in test
        self.names = [f'Cust {i}' for i in range(10)]
        self.arrivalTimes = [(i + 1) * 150 for i in range(10)]

        self.cust = [Customer(self.names[i], self.arrivalTimes[i]) for i in range(10)]

        for i in range(len(self.cust)):
            with self.subTest(i=i):
                self.assertTrue(self.se.acceptArrival(self.arrivalTimes[i], self.cust[i]))

        self.assertEqual(10, len(self.se._customers))
        self.assertEqual(0, self.se.getNumCustomersWaiting())

        # now, try to add another customer with the same name as an existing customer
        self.assertFalse(self.se.acceptArrival(500, Customer('Cust 1', 50)))

    def test_iter(self):
        # create 10 customers for use in test
        # the names and arrivalTimes lists are in Customer arrival sequence
        self.names = [f'Cust {i}' for i in range(10)]
        self.arrivalTimes = [(i + 1) * 150 for i in range(10)]

        # generate system exit order (i.e. completion order)
        self.exitOrder = np.random.permutation(10)

        # the cust list is in Customer EXIT sequence
        self.cust = [Customer(self.names[i], self.arrivalTimes[i]) for i in self.exitOrder]

        for i in range(len(self.cust)):
            self.se.acceptArrival(self.arrivalTimes[i], self.cust[i])

        # now, test iterating over SystemExit
        i = 0
        for c in self.se:
            with self.subTest(i=i):
                print(self.cust[i].name)
                self.assertEqual(self.cust[i].name, c.name)
                i += 1

    def test_arrivalTimeIterator(self):
        # create 10 customers for use in test - the names and arrival time
        # lists are in customer arrival order
        self.names = [f'Cust {i}' for i in range(10)]
        self.arrivalTimes = [(i + 1) * 150 for i in range(10)]

        # generate system exit order (i.e. completion order)
        self.exitOrder = np.random.permutation(10)

        # the cust list is in customer EXIT order
        self.cust = [Customer(self.names[i], self.arrivalTimes[i]) for i in self.exitOrder]

        for i in range(len(self.cust)):
            self.se.acceptArrival(self.arrivalTimes[i], self.cust[i])

        # now, test iterating over SystemExit
        i = 0
        for c in self.se.arrivalTimeIterator():
            with self.subTest(i=i):
                self.assertEqual(self.names[i], c.name)
                i += 1


if __name__ == '__main__':
    main(verbosity=2)
