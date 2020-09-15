#%%

import numpy as np
class Distribution:

    def __init__(self, dist_spec):
        self.RNG = dist_spec

    def __str__(self):
#        msg = ""
#        msg = msg + f'{type(self)} object at {id(self)}\n'
#        msg = str(self._RNG)
        return self._msg

    def __repr__(self):
        return self.__str__()

    @property
    def RNG(self):
        return self._RNG

    @RNG.setter
    def RNG(self, dist_spec):
        try:
            self._RNG = eval("lambda: np.random." + dist_spec.strip())
            self._msg = "lambda: np.random." + dist_spec.strip()
        except (NameError, SyntaxError):
            self._RNG = None
            return

        if self._RNG.__code__.co_argcount > 0:
            self._RNG = None
            return

        if not callable(self._RNG):
            self._RNG = None
            return

        try:
            rstate = np.random.get_state()
            self._RNG()
            np.random.set_state(rstate)
            return
        except:
            self._RNG = None

    def getEvent(self):
        if self.isValid():
            rv = self._RNG()

            if isinstance(rv, np.ndarray):
                return rv[0]
            else:
                return rv
        else:
            return None

    def isValid(self):
        if self._RNG is None:
            return False
        else:
            return True

