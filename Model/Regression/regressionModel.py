import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def makePrediction(train : "DataFrame", test : "DataFrame", target : str) -> dict:
    trainX = np.asanyarray(train.drop(target, axis=1))
    trainY = np.asanyarray(train[target])
    testX = np.asanyarray(test.drop(target, axis=1))
    testY = np.asanyarray(test[target])

    regressionModel = LinearRegression()
    regressionModel.fit(trainX, trainY)
    predictedY = regressionModel.predict(testX)

    rmse = np.sqrt(metrics.mean_squared_error(testY, predictedY))
    return {
        "Attributes": {
            "Coefficients": regressionModel.coef_.tolist(),
            "Intercept": regressionModel.intercept_.tolist(),
            "RMSE": rmse
        },
        "Prediction": predictedY 
    }
