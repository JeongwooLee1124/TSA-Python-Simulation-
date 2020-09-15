import numpy as np

class Assigner:
    """
    Instances of this class are used to "select" objects in a dictionary, using various
    selection rules (embedded in functions)
    """

    def __init__(self):
        """
        Constructor
        """
        self._last_assigned = -1

    def assignInSequence(self, dict):
        """
        Selects and returns an object from the supplied dictionary in sequence. OK to use
        with destinations, but not Servers.
        @param dict: dictionary - dictionary containing the set of objects which can
                                  be selected
        @return: obj or None
        """
        if len(dict) == 0:
            return None

        # increment the sequence number and wrap to beginning of dictionary if past end
        self._last_assigned += 1
        if self._last_assigned >= len(dict):
            self._last_assigned = 0

        # return the actual object
        return list(dict.values())[self._last_assigned]

    def assignToShortest(self, dict):
        """
        Selects and returns an object based on the number of customers waiting. Requires that
        the objects in the dictionary provide a getNumCustomersWaiting function (i.e. they are
        CustomerDestinations.
        @param dict: dictionary - dictionary containing the set of objects which can
                                  be selected
        @return: obj or None
        """

        if len(dict) == 0:
            return None

        # first, get the objects from the dictionary
        obj = dict.values()

        # construct an ndarray
        ncust = np.array([o.getNumCustomersWaiting() for o in obj])

        # find the first index where the number of customers waiting matches the min customers waiting
        idx = ncust.argmin()

        # find the corresponding dictionary key
        qkey = list(dict.keys())[idx]

        # return the actual object
        return dict[qkey]

    def assignByAvailableTime(self, dict):
        """
        Selects an object from the dictionary based on the minimum availableSince time.
        Objects in the dict must implement an availableSince property or public attribute.
        @param dict: dictionary
        @return: Object from the dictionary
        """
        if len(dict) == 0:
            return None

        which = np.argmin([srvr.availableSince for srvr in dict.values()])
        return list(dict.values())[which]
