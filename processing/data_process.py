from sys import intern
from typing import Type
import numpy as np
from math import factorial
from processing.settings import Settings as s
from scipy.signal import find_peaks


class DataProcess(object):
    """

    """

    def __init__(self, storeddata):  # TODO make everything that can be array an array
        self.gyro = [storeddata['gyrX'],
                     storeddata['gyrY'], storeddata['gyrZ']]
        self.acc = [storeddata['accX'], storeddata['accY'], storeddata['accZ']]
        self.time = storeddata['time']

        self.combAcc = []
        return

    def combineAccelerations(self):
        """
    Function that combines the accelerations
        """
        self.combAcc = (np.sqrt(np.square(self.acc[0]) +
                                np.square(self.acc[1]) +
                                np.square(self.acc[2]))
                        - s.gravity)
        return self.combAcc

    def findGCT(self):
        noisy_signal = self.performSW(s.sw_width, s.sw_type)
        peaks_idx = self.findPeaks(noisy_signal)
        gct_list = self.gctFromPeaks(peaks_idx)

        stepnumbers = list(range(1, gct_list.size + 1))

        return gct_list, stepnumbers

    def performSW(self, width: int, signal_type: str):
        if signal_type == 'x':
            signal = self.acc[0]
        elif signal_type == 'y':
            signal = self.acc[1]
        elif signal_type == 'z':
            signal = self.acc[2]
        elif signal_type == 'combined':
            signal = self.combineAccelerations()
        else:
            exit()

        noise_signal = np.zeros(len(signal))
        signal_arr = np.array(signal + [0]*width)

        for i in range(len(signal)):
            noise_signal[i] = np.sum(np.abs(signal_arr[i]
                                            - signal_arr[np.arange(i+1, i+width)]))

        filtered_signal = self.savityzky_golay(noise_signal, 81, 2)
        ordered_signal = np.sort(filtered_signal)
        scndmaximum = ordered_signal[-1]

        return filtered_signal/scndmaximum

    def savityzky_golay(self, y, window_size, order, deriv=0, rate=1) -> np.ndarray:
        """
        Todo: insert documentation from idrottsmatta4U
        """

        try:
            window_size = np.abs(np.int(window_size))
            order = np.abs(np.int(order))
        except ValueError as msg:
            raise ValueError("windowsize and order have to be of type int")

        if window_size % 2 != 1 or window_size < 1:
            raise TypeError(" windowsize must be a positive odd number")

        if window_size < order + 2:
            raise TypeError(
                " windowsize is too small for the polynomials number ")

        order_range = range(order+1)
        half_window = (window_size - 1) // 2

        # precompute coefficients
        b = np.mat([[k**i for i in order_range]
                   for k in range(-half_window, half_window + 1)])
        m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)

        # pad the signals at the extremes with values from the signal
        firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
        lastvals = y[-1] + np.abs(y[-half_window-1:1][::-1] - y[-1])

        y = np.concatenate((firstvals, y, lastvals))

        return np.convolve(m[::-1], y, mode='valid')

    def findPeaks(self, signal, threshold=0.8):
        peaks_idx, _ = find_peaks(signal, distance=50, height=0.4)
        final_peaks_idx = []

        for i in range(peaks_idx.size - 1):
            if signal[peaks_idx[i]] > threshold:
                final_peaks_idx.append(peaks_idx[i])
                final_peaks_idx.append(peaks_idx[i+1])

        return final_peaks_idx

    def gctFromPeaks(self, peaks_idx: list):
        return self.time[peaks_idx[1::2]] - self.time[peaks_idx[::2]]
