import os
import json
from binance.client import Client




# paths


class getCred:
    def __init__(self):
        self.pathCred = os.path.join(os.path.expanduser('~'),'0_cred')
        binanceApiDict = self.readDictFromTxt(os.path.join(self.pathCred,'binanceAPI_2.txt'))
        binanceAPI = binanceApiDict['binanceAPI']
        binanceAPISecret = binanceApiDict['binanceAPISecret']
        self.client = Client(binanceAPI, binanceAPISecret)
        self.cmcAPI = open(os.path.join(self.pathCred,'cmcAPI.txt')).read()

    def readDictFromTxt(self,path):
        # reading the data from the file
        with open(path) as f:
            data = f.read()
        return json.loads(data)

cred = getCred()

