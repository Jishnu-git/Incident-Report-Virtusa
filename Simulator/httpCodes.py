import random

informationCodes = [100, 101]
successCodes = list(range(200, 207));
redirectionCodes = list(range(300, 305)) + [307, 308]
clientErrorCodes = list(range(400, 418)) + list(range(421, 427)) + [428, 429, 431, 451]
serverErrorCodes = list(range(500, 509)) + [510, 511]
acceptedHttpCodes = informationCodes + successCodes + redirectionCodes + clientErrorCodes
allHttpCodes = acceptedHttpCodes + serverErrorCodes


#get a random information code
def getInformationCode() -> int:
    return random.choice(informationCodes)

#get a random success code
def getSuccessCode() -> int:
    return random.choice(successCodes)

#get a random redirection code
def getRedirectionCode() -> int:
    return random.choice(redirectionCodes)

#get a random client error code
def getClientErrorCode() -> int:
    return random.choice(clientErrorCodes)

#get a random server error code
def getServerErrorCode() -> int:
    return random.choice(serverErrorCodes)

#get any random code, if no rate of failure is specified choose a truly random http code
#otherwise return a random success or a random server error according to the rate passed
def getAnyCode(rateOfFailure : float = None) -> int:
    if rateOfFailure == None:
        return random.choice(allHttpCodes)
    else:
        if (random.random() <= rateOfFailure):
            return random.choice(serverErrorCodes)
        else:
            return random.choice(acceptedHttpCodes)

#get a random http code that is not a server error
def getAnyAcceptedCode() -> int:
    return random.choice(acceptedHttpCodes)