from logGenerator import logGenerator
from datetime import timedelta, datetime
import os
import math
import random
import json
import csv

if __name__ == "__main__":
    #read config.json and load all the details
    configJSON = open("./config.json", "r")
    config = json.load(configJSON)
    configJSON.close()

    startTime = datetime.strptime(config["startTime"], "%H:%M:%S")
    endTime = startTime #This will be the global end time, inclusive of all individual APIs
    timeStride = config["timeStride"]

    outputDir = os.path.dirname(config["outputFile"])
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    outputFile = open(config["outputFile"], "w+")
    outputCSV = csv.writer(outputFile)

    apis = []
    for api in config["APIs"]:
        actionsRaw = api["actions"]
        actions = []
        for actionRaw in actionsRaw:
            action = {}
            action["name"] = actionRaw["action"]
            action["arguments"] = []
            if actionRaw["action"] != "idle":
                action["arguments"].append(actionRaw["amount"])
            action["arguments"].extend([
                actionRaw["duration"],
                actionRaw["minResTime"],
                actionRaw["maxResTime"],
                actionRaw["rateOfFailure"]
            ])
            actions.append(action)
        apis.append(logGenerator(api["apiName"], actions, startTime, timeStride))
        apis[-1].doAll()
        if (apis[-1].time > endTime):
            endTime = apis[-1].time #Global end time will the be max of end time of all APIs

    #repeatedly generate data and write into csv file
    outputCSV.writerow(["API route", "Time", "HTTP Code", "Response Time", "Status"])
    while startTime < endTime:
        logs = []
        for api in apis:
            logs += api.getLogs(startTime)
        random.shuffle(logs) #shuffling only for an aesthetic resemblance to real logs
        outputCSV.writerows(logs)
        startTime += timedelta(seconds = timeStride)
    
    outputFile.close()

