from unittest import TestCase, main
import numpy as np
from Distribution import Distribution


# Functions for testing Distribution construction

def foo1():
    return np.random.normal(100, 20)


def foo2():
    # the following line is an intentional error. Do not correct.
    return np.random.nrml(100, 20)


class TestDistribution(TestCase):

    def test_init(self):
        # set seed to ensure known sequence
        np.random.seed(100)

        # initialize empty list for distributions
        valid = list()
        invalid = list()

        # test construction.
        # I made my Distribution class more flexible than the assignment requires.
        # This provides additional flexibility on how I can create distributions.
        # The commented tests evaluate the additional functionality in my Distribution
        # class.

        valid.append(Distribution('normal(100, 20)'))
        valid.append(Distribution('poisson(5)'))
        valid.append(Distribution('triangular(10, 20, 40)'))
        valid.append(Distribution('uniform(10,20)'))
        # valid.append(Distribution('lambda: np.random.normal(100,20)'))
        # valid.append(Distribution('lambda: 1'))
        # valid.append(Distribution(lambda: np.random.normal(100, 20)))
        # valid.append(Distribution(foo1))

        # I also wrote my Distribution class to cleanly handle erroneous
        # distribution specifications and produce an "invalid" Distribution
        # instance rather than crashing with an exception. However, I did
        # not require this level of advanced functionality in your class.
        # The commented tests below relate to testing this additional functionality.

        invalid.append(Distribution('nrml(100,20)'))
        # invalid.append(Distribution('lamda: np.random.normal(100,20'))
        # invalid.append(Distribution(foo2))

        # test construction of VALID Distributions
        for i in range(len(valid)):
            with self.subTest(i=i):
                self.assertFalse(valid[i]._RNG is None)
                self.assertTrue(isinstance(valid[i].__repr__(),str))
                self.assertTrue(isinstance(valid[i].__str__(),str))


        # test construction of INVALID Distributions
        for i in range(len(invalid)):
            with self.subTest(i=i):
                self.assertTrue(invalid[i]._RNG is None)

    def test_RNG_getter(self):
        # basically the same as the _init test, just performed another way
        # set seed to ensure known sequence
        np.random.seed(100)

        # initialize empty list for distributions
        valid = list()
        invalid = list()

        # The commented tests evaluate the additional functionality in my Distribution
        # class not required by the assignment.

        valid.append(Distribution('normal(100, 20)'))
        valid.append(Distribution('poisson(5)'))
        valid.append(Distribution('triangular(10, 20, 40)'))
        valid.append(Distribution('uniform(10,20)'))
        # valid.append(Distribution('lambda: np.random.normal(100,20)'))
        # valid.append(Distribution('lambda: 1'))
        # valid.append(Distribution(lambda: np.random.normal(100, 20)))
        # valid.append(Distribution(foo1))

        invalid.append(Distribution('nrml(100,20)'))
        # invalid.append(Distribution('lamda: np.random.normal(100,20'))
        # invalid.append(Distribution(foo2))

        for i in range(len(valid)):
            with self.subTest(i=i):
                self.assertFalse(valid[i].RNG is None)

        for i in range(len(invalid)):
            with self.subTest(i=i):
                self.assertTrue(invalid[i].RNG is None)

    def test_isValid(self):
        # set seed to ensure known sequence
        np.random.seed(100)

        # initialize empty list for distributions
        valid = list()
        invalid = list()

        # The commented tests evaluate additional functionality in my Distribution
        # class that is not required for the assignment.

        valid.append(Distribution('normal(100, 20)'))
        valid.append(Distribution('poisson(5)'))
        valid.append(Distribution('triangular(10, 20, 40)'))
        valid.append(Distribution('uniform(10,20)'))
        # valid.append(Distribution('lambda: np.random.normal(100,20)'))
        # valid.append(Distribution('lambda: 1'))
        # valid.append(Distribution(lambda: np.random.normal(100, 20)))
        # valid.append(Distribution(foo1))

        invalid.append(Distribution('nrml(100,20)'))
        # invalid.append(Distribution('lamda: np.random.normal(100,20'))
        # invalid.append(Distribution(foo2))

        for i in range(len(valid)):
            with self.subTest(i=i):
                self.assertTrue(valid[i].isValid())

        for i in range(len(invalid)):
            with self.subTest(i=i):
                self.assertFalse(invalid[i].isValid())

    def test_getEvent(self):
        # create distribution instance, normal distribution with mean 100, std 20
        dist1 = Distribution('normal(100, 20, 1)')

        # the seed must be set AFTER creating the Distribution instances, because
        # the constructor invokes the RNG function one time to validate that it
        # can be called.

        np.random.seed(100)

        expected = [65.00469054, 106.85360807, 123.06071605, 94.95127927,
                    119.62641574, 110.28437683, 104.42359338, 78.59913339,
                    96.21008338, 105.10002889]

        for i in range(0, 10):
            with self.subTest(i=i):
                actual = dist1.getEvent()
                self.assertAlmostEqual(expected[i], actual)


if __name__ == '__main__':
    main(verbosity=2)
