import pandas as pd
from Regression.regressionModel import RegressionModel
from AutoRegression import autoRegressionModel
import labeler
import os
import json

def regression(trainData : "DataFrame", testData : "DataFrame", trainingWindow : int) -> tuple:
    regressionModel = RegressionModel(trainData, "Failure Rate")
    statePredictions = ["-"] * (trainingWindow - 1)
    failurePredictions = ["-"] * (trainingWindow - 1)
    for i in range(0, testData.shape[0] - trainingWindow):
        currentWindow = testData.iloc[i:(i + trainingWindow)]
        forecastUsers = autoRegressionModel.makePrediction(currentWindow, "Requests", 5)
        forecastResTime = autoRegressionModel.makePrediction(currentWindow, "Response Time", 5)
        forecastWindow = pd.DataFrame({"Response Time": forecastResTime, "Requests": forecastUsers})

        forecastAggRaw = forecastWindow.agg(["mean", "min", "max"])
        forecastAggFormatted = pd.DataFrame({
            "Average Response Time": [forecastAggRaw["Response Time"]["mean"]],
            "Minimum Response Time": [forecastAggRaw["Response Time"]["min"]],
            "Maximum Response Time": [forecastAggRaw["Response Time"]["max"]],
            "Average Request Count": [forecastAggRaw["Requests"]["mean"]],
            "Minimum Request Count": [forecastAggRaw["Requests"]["min"]],
            "Maximum Request Count": [forecastAggRaw["Requests"]["max"]],
        })
        failurePredictions.append(regressionModel.makePrediction(forecastAggFormatted)[0])
        forecastAggFormatted["Failure Rate"] = [failurePredictions[-1]]
        print(forecastAggFormatted)
        statePredictions.extend(labeler.label(forecastAggFormatted))

    failurePredictions.append("-")
    statePredictions.append("-")

    predictedData = testData
    predictedData["Predicted Failure"] = failurePredictions
    predictedData["Status"] = statePredictions
    return regressionModel.getAttributes(), predictedData

if __name__ == "__main__":
    configJSON = open("./config.json", "r")
    config = json.load(configJSON)
    configJSON.close()

    models = {
        "regression": regression
    }

    trainData = pd.read_csv(config["trainingFile"])
    testData = pd.read_csv(config["testingFile"])
    predictionFile = config["predictedOutputFile"]
    modelFile = config["modelOutputFile"]
    method = config["model"]
    trainingWindow = config["trainingWindow"]

    for outputFile in [predictionFile, modelFile]:
        outputDir = os.path.dirname(outputFile)
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

    modelAttributes, predictedData = models[method](trainData, testData, trainingWindow)
    predictedData.to_csv(predictionFile, index=False)
    with open(modelFile, "w") as modelOutput:
        json.dump(modelAttributes, modelOutput)

