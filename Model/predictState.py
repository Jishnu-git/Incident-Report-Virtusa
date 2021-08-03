import pandas as pd
from Regression import regressionModel, labeler
import os
import json

def regression(trainData : "DataFrame", testData : "DataFrame") -> tuple:
    output = regressionModel.makePrediction(trainData, testData, "Failure Rate")
    predictedData = testData.drop("Failure Rate", axis=1)
    predictedData["Failure Rate"] = output["Prediction"]
    predictedData["Status"] = labeler.label(predictedData)

    return output["Attributes"], predictedData

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

    for outputFile in [predictionFile, modelFile]:
        outputDir = os.path.dirname(outputFile)
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

    modelAttributes, predictedData = models[method](trainData, testData)
    predictedData.to_csv(predictionFile, index=False)
    with open(modelFile, "w") as modelOutput:
        json.dump(modelAttributes, modelOutput)

