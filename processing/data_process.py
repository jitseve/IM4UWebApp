from sys import intern
import numpy as np
from math import factorial
from processing.settings import Settings as s
from scipy.signal import find_peaks


class DataProcess(object):
    """
    
    """
    def __init__(self, storeddata): #TODO make everything that can be array an array
        self.gyro = [storeddata['gyrX'],storeddata['gyrY'],storeddata['gyrZ']]
        self.acc = [storeddata['accX'],storeddata['accY'],storeddata['accZ']]
        self.time = storeddata['time_a'] 

        self.combAcc = []
        return

    
    def combineAccelerations(self):
        """
    Function that combines the accelerations
        """
        self.combAcc =  (np.sqrt(np.square(self.acc[0]) + 
                                 np.square(self.acc[1]) +
                                 np.square(self.acc[2]))
                                 - s.gravity )
        return self.combAcc


   
    def emwaFilter(self,data,alpha):
        """
        EMWA filter
        """
        #Initialization
        emwaData = [data[0]]

        #Filtering
        for k in range(1, len(data)):
            emwaData.append(alpha*emwaData[k-1]+(1-alpha)*data[k])
            
        return emwaData
