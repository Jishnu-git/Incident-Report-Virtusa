import pandas as pd
import os
import json

if __name__ == "__main__":
    configJSON = open("./config.json", "r")
    config = json.load(configJSON)
    configJSON.close()

    simulatedData = pd.read_csv(config["inputFile"])
    windowSize = config["windowSize"]
    outputFile = config["outputFile"]
    outputDir = os.path.dirname(outputFile)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    simulatedData.drop(["API route", "HTTP Code"], inplace=True, axis=1)
    simulatedData.Status = simulatedData.Status.map({"success": 0, "failure": 1})
    simulatedData["Requests"] = 1
    simulatedData.rename(columns={"Status": "Failure"}, inplace=True)
    groupedData = simulatedData.groupby("Time").agg({"Response Time": "mean", "Failure": "sum", "Requests": "count"})
    
    avgResTime = []
    minResTime = []
    maxResTime = []
    avgReqs = []
    minReqs = []
    maxReqs = []
    failPercent = []
    for i in range(0, groupedData.shape[0] - 5):
        windowAgg = groupedData.iloc[i:(i + 5)].agg({"Response Time": ["mean", "min", "max"], "Failure": "sum", "Requests": ["sum", "min", "max", "mean"]})
        avgResTime.append(windowAgg["Response Time"]["mean"])
        minResTime.append(windowAgg["Response Time"]["min"])
        maxResTime.append(windowAgg["Response Time"]["max"])
        avgReqs.append(windowAgg["Requests"]["mean"])
        minReqs.append(windowAgg["Requests"]["min"])
        maxReqs.append(windowAgg["Requests"]["max"])
        failPercent.append(windowAgg["Failure"]["sum"] / windowAgg["Requests"]["sum"])
    
    aggregatedData = pd.DataFrame({
        "Average Response Time": avgResTime,
        "Minimum Response Time": minResTime,
        "Maximum Response Time": maxResTime,
        "Average Request Count": avgReqs,
        "Minimum Request Count": minReqs,
        "Maximum Request Count": maxReqs,
        "Failure Rate": failPercent
    })

    aggregatedData.to_csv(outputFile)