from processing.dataplot import DataPlot
from processing.data_process import DataProcess
from processing.settings import Settings as s
from processing.data_read import DataRead
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")


def run():
    """
    ----------------- LOADING -----------------
    """
    Data = DataRead()
    rawdata = Data.read(s.folderpath, filetype=s.filetype)
    timestamps = rawdata['time']

    """
    ---------------- PROCESSING -------------------
    """
    Data = DataProcess(rawdata)

    combAcc = Data.combineAccelerations()

    GCT, steps = Data.findGCT()

    Freq, steps2 = Data.findFrequency()

    # Todo: Compute GCT DATA here
    # This is all for testing purposes now
    # steps2 = [1, 2, 3, 4, 5, 6, 7, 8]
    # GCT = [0.250, 0.183, 0.133, 0.135, 0.178, 0.185, 0.200, 0.200]
    # Freq = [2.2, 1.83, 2.05, 1.8, 1.65, 1.58, 1.5, 1.48]

    # Todo: Compute step frequency here

    """
    ---------------- PLOTTING ----------------
    """
    dataPlot = DataPlot()

    img = dataPlot.img1by1(
        timestamps, combAcc, ylab='Acceleration [m/s2]', xlab='time [ms]', title='Combined Acceleration')
    img2 = dataPlot.img1by1(steps, GCT, line=False, color=1, marker=0,
                            ylab='GCT [ms]', xlab='stepnr', title='GCT')
    img3 = dataPlot.img1by1(steps2, Freq, line=False, color=2, marker=1,
                            ylab='Step Frequency [steps/s]', xlab='stepnr', title='Step frequency')

    return img, img2, img3
