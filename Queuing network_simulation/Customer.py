import pandas as pd
import math
from Experience import Experience

class Customer:

    def __init__(self, name, simtime):
        self._name = name
        self._systemArrivalTime = simtime
        self._experience = dict()
        self._currLocation = None
        self._totalWaitTime = math.nan
        self._totalSystemTime = math.nan

    @property
    def systemArrivalTime(self):
        return self._systemArrivalTime

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, in_name):
        self._name = in_name

    @property
    def totalSystemTime(self):
        return self._totalSystemTime

    @property
    def totalWaitTime(self):
        return self._totalWaitTime

    @property
    def currLocation(self):
        return self._currLocation

    def getExperiences(self):
        return self._experience.copy()


    def logArrival(self, simtime, stageId):
        self._experience.update({stageId: Experience(stageId, simtime)})
        self._currLocation = stageId
        self._totalWaitTime = math.nan
        self._totalSystemTime = math.nan

    def logServiceEntry(self, simtime, serverId):
        self._experience[self._currLocation].logServiceEntry(serverId, simtime)
        self._totalWaitTime = 0
        for key in self._experience:
            self._totalWaitTime += self._experience[key].waitingTime        

    def logServiceCompletion(self, simtime):
        self._experience[self._currLocation].logServiceCompletion(simtime)
        self._experience[self._currLocation].logServiceCompletion(simtime)
        self._totalSystemTime = 0
        for key in self._experience:
            self._totalSystemTime = self._totalSystemTime + self._experience[key].systemTime

    def getExperienceStatistics(self):
        df = pd.DataFrame()
        for key in self._experience:
            exp_df = self._experience[key].makeRow()
            df = pd.concat([df, exp_df], ignore_index = True)
        return df

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name
