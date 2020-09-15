import math
import pandas as pd

class Experience:

    def __init__(self, *args):
        numargs = len(args)
        self._stageId = args[0]
        self._queueEntryTime = args[1]
        self._df = list()
        self._serviceEntryTime = math.nan
        self._serviceCompletionTime = math.nan
        self._systemTime = math.nan
        self._serverId = math.nan
        self._waitingTime = math.nan

        if numargs == 5:
            self._serverId = args[2];
            self._serviceEntryTime = args[3]
            self._serviceCompletionTime = args[4]
       

    def logServiceEntry(self, serverId, serviceEntryTime):
        self._serverId = serverId
        self._serviceEntryTime = serviceEntryTime
        self._waitingTime = serviceEntryTime - self._queueEntryTime;

    def logServiceCompletion(self, serviceCompletionTime):
        self._serviceCompletionTime = serviceCompletionTime
        self._systemTime = serviceCompletionTime - self._queueEntryTime

    def makeRow(self):
        df = pd.DataFrame([[self._stageId, self._queueEntryTime, self._serverId, self._serviceEntryTime, self._serviceCompletionTime, self._systemTime, self._waitingTime]],\
                columns=['stageId', 'queueEntryTime', 'serverId', 'serviceEntryTime', 'serviceCompletionTime', 'systemTime', 'waitingTime'])
        return df

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if isinstance(self._stageId, str):
            return self._stageId
        else:
            return str(self._stageId)

    @property
    def stageId(self):
        if hasattr(self, '_stageId'):
            return self._stageId
        else:
            return math.nan

    @property
    def queueEntryTime(self):
        if hasattr(self, '_queueEntryTime'):
            return self._queueEntryTime
        else:
            return math.nan

    @property
    def serverId(self):
        if hasattr(self, '_serverId'):
            return self._serverId
        else:
            return math.nan

    @property
    def serviceEntryTime(self):
        if hasattr(self, '_serviceEntryTime'):
            return self._serviceEntryTime
        else:
            return math.nan

    @property
    def serviceCompletionTime(self):
        if hasattr(self, '_serviceCompletionTime'):
            return self._serviceCompletionTime
        else:
            return math.nan 

    @property
    def systemTime(self):
        if hasattr(self, '_systemTime'):
            return self._systemTime
        else:
            return math.nan

    @property
    def waitingTime(self):
        if hasattr(self, '_waitingTime'):
            return self._waitingTime
        else:
            return math.nan

