import glob, os, sys, csv, json
import numpy as np
from matplotlib import pyplot as plt


class DataRead():
    """
    Class that can both loads data from json files
    """

    def __init__(self):
        """
        Initialising the class
        """
        return 


    def read(self, folderpath, filetype='csv'):
        if (filetype == 'csv'):
            list_of_uploads = glob.glob(folderpath + "/*.csv")
            latest_upload = max(list_of_uploads, key=os.path.getctime)
            data_comb = self.load_csv(latest_upload)
            data = self.transform_csvformat(data_comb)

        elif (filetype == 'json'):
            #Todo: Readout json files
            print("Json Chosen")
        
        return data

   
    def load_csv(self, path):
        """
        Function that reads a folder of CSV files

        =INPUT=
            self        Datastructure to save the read data in
            paths       array with relative paths to the seperate files
        =OUTPUT=
            self.data   Datastructure with all the data
        """
        with open(path, newline='') as csvfile:
            return list(csv.reader(csvfile))

        print("Error in reading CSV")
        return


    def transform_csvformat(self, data_container):
        """
        Function that transforms the sorting of the data output

        =INPUT=
            self                Datastructure to save the read data in
            data_container      Data_container that needs to be transformed
        =OUTPUT=
            self.transdata      Datastructure with all the transformed data
        """

        # Transforming data
        transdata = {'accX': [], 'accY': [], 'accZ': [], 'gyrX': [], 'gyrY': [], 'gyrZ': [], 'time': []}
        for kk in range(len(data_container)):
            if (kk != 0):
                transdata['time'].append(float(data_container[kk][0]))
                transdata['accX'].append(float(data_container[kk][1]))
                transdata['accY'].append(float(data_container[kk][2]))
                transdata['accZ'].append(float(data_container[kk][3]))
                transdata['gyrX'].append(float(data_container[kk][4]))
                transdata['gyrY'].append(float(data_container[kk][5]))
                transdata['gyrZ'].append(float(data_container[kk][6]))                                                
        
        # Time normalise
        transdata['time'] = np.array(transdata['time']) - transdata['time'][0]

        return transdata