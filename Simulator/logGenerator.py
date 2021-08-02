import httpCodes
import random
import math
from datetime import timedelta

class logGenerator:
    def __init__(self, apiName : str, actions : list, time : "datetime", timeStride : int):
        self.apiName = apiName
        self.actions = actions
        self.actionIndex = 0
        self.userCount = 0
        self.time = time
        self.timeStride = timeStride
        self.logs = {}

        self.__actionMap = {
            "increase": self.__increase,
            "decrease": self.__decrease,
            "spike": self.__spike,
            "drop": self.__drop,
            "idle": self.__idle
        }

    #Private helper function to get the loop count given duration in minutes
    def __toTicks(self, minutes : int) -> int:
        return math.floor(timedelta(minutes = minutes).seconds / self.timeStride)

    #Private helper function to generate logs based on the current value of the object's attributes
    def __generateLogs(self, minResTime : float, maxResTime : float, rateOfFailure : float) -> list:
        resultLog = []
        for _ in range(self.userCount):
            responseTime = round(random.uniform(minResTime, maxResTime), 2)
            httpCode = httpCodes.getAnyCode(rateOfFailure)
            status = "success" if httpCode < 500 else "failure"
            resultLog.append([
                self.apiName,
                str(self.time.time()),
                httpCode,
                responseTime,
                status
            ])
        return resultLog
    
    #Private function to linearly increase the number of users by the given amount over the specifed amount of time and generate logs periodically
    def __increase(self, increaseCount : int, duration : int, minResTime : float, maxResTime : float, rateOfFailure : float):
        ticks = self.__toTicks(duration)
        incPerTick = math.floor(increaseCount / ticks)
        incrementDone = 0
        for i in range(ticks):
            if i == (ticks - 1):
                self.userCount += increaseCount - incrementDone
                incrementDone += increaseCount - incrementDone
            else:
                self.userCount += incPerTick
                incrementDone += incPerTick

            self.logs[self.time] = self.__generateLogs(
                minResTime + (0.75 * (maxResTime - minResTime) * incrementDone / increaseCount),
                maxResTime - (0.75 * (maxResTime - minResTime) * (increaseCount - incrementDone) / increaseCount),
                (rateOfFailure * 0.5) + (rateOfFailure * 0.5 * incrementDone / increaseCount)
            )
            
            self.time += timedelta(seconds = self.timeStride)
            
    #Private function to linearly decrease the number of users by the given amount over the specifed amount of time and generate logs periodically    
    def __decrease(self, decreaseCount : int, duration : int, minResTime : float, maxResTime : float, rateOfFailure : float):
        ticks = self.__toTicks(duration)
        decPerTick = math.floor(decreaseCount / ticks)
        decrementDone = 0
        for i in range(ticks):
            if i == (ticks - 1):
                self.userCount -= decreaseCount - decrementDone
                decrementDone += decreaseCount - decrementDone
            else:
                self.userCount -= decPerTick
                decrementDone += decPerTick
            
            if self.userCount < 0: #Handle underflow in number of users by hard clamping to zero
                self.userCount = 0
            
            self.logs[self.time] = self.__generateLogs(
                minResTime + (0.75 * (maxResTime - minResTime) * (decreaseCount - decrementDone) / decreaseCount),
                maxResTime - (0.75 * (maxResTime - minResTime) * decrementDone / decreaseCount),
                (rateOfFailure * 0.5) + (rateOfFailure * 0.5 * (decreaseCount - decrementDone) / decreaseCount)
            )
            
            self.time += timedelta(seconds = self.timeStride)
    
    #Private function to maintain the number of users constant and generate logs periodically
    def __idle(self, duration : int, minResTime : float, maxResTime : float, rateOfFailure : float):
        ticks = self.__toTicks(duration)
        for _ in range(ticks):
            self.logs[self.time] = self.__generateLogs(minResTime, maxResTime, rateOfFailure)
            self.time += timedelta(seconds = self.timeStride)

    #Private function to increase the number of users at once and then generate logs periodically
    def __spike(self, spikeAmount : int, duration : int, minResTime : float, maxResTime : float, rateOfFailure : float):
        self.userCount += spikeAmount
        self.__idle(duration, minResTime, maxResTime, rateOfFailure)
    
    #Private function to decrease the number of users at once and then generate logs periodically
    def __drop(self, dropAmount : int, duration : int, minResTime : float, maxResTime : float, rateOfFailure : float):
        self.userCount -= dropAmount
        if self.userCount < 0:
            self.userCount = 0
        self.__idle(duration, minResTime, maxResTime, rateOfFailure)

    #Function to perform the next action in the list
    def doNext(self):
        action = self.actions[self.actionIndex]
        self.__actionMap[action["name"]](*action["arguments"])
        self.actionIndex += 1

    #Function to perform all actions in the list
    def doAll(self):
        while (self.actionIndex < len(self.actions)):
            self.doNext()

    #Function to return the logs for a specific time, if time is not specified, returns logs from all timestamps unrolled to a sinlge list
    def getLogs(self, timestamp : "datetime" = None) -> list:
        if timestamp == None:
            return [log for logs in self.logs.values() for log in logs]
        else:
            if timestamp not in self.logs.keys():
                return []
            return self.logs[timestamp]
