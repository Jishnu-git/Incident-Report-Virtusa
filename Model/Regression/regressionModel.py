import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class RegressionModel:
    def __init__(self, train : "DataFrame", target : str):
        self.trainX = np.asanyarray(train.drop(target, axis=1))
        self.trainY = np.asanyarray(train[target])
        self.model = LinearRegression()
        self.model.fit(self.trainX, self.trainY)

    def getAttributes(self) -> dict:
        return {
            "Coefficients": self.model.coef_.tolist(),
            "Intercept": self.model.intercept_.tolist()
        }

    def makePrediction(self, data) -> "array":
        return self.model.predict(data)

