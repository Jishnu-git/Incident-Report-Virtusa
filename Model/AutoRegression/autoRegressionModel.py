import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AutoReg

def makePrediction(train : "DataFrame", target : str, predictionCount : int) -> "array":
    trainVar = np.asarray(train[target])
    arModel = AutoReg(trainVar, 1, old_names=False)
    arModel = arModel.fit()
    predictedVals = arModel.forecast(predictionCount)

    return predictedVals

    