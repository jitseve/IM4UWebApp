from sys import intern
from typing import Type
import numpy as np
from math import factorial

from numpy.core.numeric import indices
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

        stepnumbers = list(range(1, len(gct_list) + 1))

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

    def findFrequency(self):
        peaks, valleys, indices = self.stepRegister()
        averageStepFrequencies, singleStepFrequencies = self.findStepFrequency(
            valleys)

        stepnumbers = list(range(1, len(singleStepFrequencies)+1))

        return singleStepFrequencies, stepnumbers

    def stepRegister(self):
        K0, alpha, W2, TH_pk, TH_s, TH, W1, TH_vy, = s.stepRegisterInit()

        maxima = [[], []]
        minima = [[], []]
        indices = []

        # * Valid valley detection
        # 1. Minima detection
        for i in range(1, len(self.combAcc)-1):
            if ((self.combAcc[i] < self.combAcc[i+1]) and (self.combAcc[i] < self.combAcc[i-1]) and (self.combAcc[i] < TH_vy)):
                minima[0].append(self.combAcc[i])
                minima[1].append(self.time[i])
                indices.append(i)

            # 1. Maxima Detection
            if ((self.combAcc[i] > self.combAcc[i+1]) and (self.combAcc[i] > self.combAcc[i-1]) and (self.combAcc[i] > TH_pk)):
                maxima[0].append(self.combAcc[i])
                maxima[1].append(self.time[i])

        # . Adapt TH_PK threshold according to the maximum value and remove all the wrong maxima
        TH_pk = max(maxima[0])*0.3  # TODO Choose the right value
        ind = 0
        while ind < len(maxima[0]):
            if maxima[0][ind] <= TH_pk:
                maxima[0].pop(ind)
                maxima[1].pop(ind)

                ind = ind
            else:
                ind += 1

        # . Remove all the valleys before first peak
        ind = 0
        while (ind < len(minima[0])-1 and minima[1][ind] < maxima[1][0]):
            if minima[1][ind] < maxima[1][0] and minima[1][ind+1] < maxima[1][0]:
                minima[1].pop(ind)
                minima[0].pop(ind)
                indices.pop(ind)

                ind = ind
            else:
                ind += 1

        # 2. Single valley detection with temporal threshold constraint
        for i in range(1, len(self.combAcc)-1):

            t_i = self.time[i]
            n = self.find_nearest(np.asarray(minima[1]), t_i)
            t_n = minima[1][n]

            if ((np.abs(t_i-t_n)) < TH_s):
                if (minima[1][n]-minima[1][max(0, n-W2)]) == 0:
                    Ki = K0
                else:
                    Ki = alpha*(minima[1][n]-minima[1][max(0, n-W2)])/W2
            elif (np.abs(t_i - t_n) >= TH_s):
                Ki = K0

            # * Valid valley detection
            Ki = max(Ki, K0)
            if ((minima[1][max(n, 1)]-minima[1][max(n-1, 0)]) < Ki):
                index = minima[0].index(
                    max([minima[0][max(n, 1)], minima[0][max(n-1, 0)]]))
                minima[0].pop(index)
                minima[1].pop(index)
                indices.pop(index)

        j = 1
        while j < len(maxima[0]):
            if ((maxima[1][j]-maxima[1][j-1]) < K0):
                if maxima[0][j] > maxima[0][j-1]:
                    index = j-1     # Determine the index of the smallest peak
                else:
                    index = j
                # Delete smallest peak
                maxima[0].pop(index)
                maxima[1].pop(index)
                j = j
            else:
                j += 1

        # Clean extra valleys
        if len(minima[0]) >= 2 and len(maxima[0]) >= 1:
            if minima[1][-1] > maxima[1][-1] and minima[1][-2] > maxima[1][-1]:
                minima[0].pop()
                minima[1].pop()
                indices.pop()

        return maxima, minima, indices

    def find_nearest(self, array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    def findStepFrequency(self, peaks):
        stepFreq = []

        for i in range(len(peaks[0]) - 1):
            timeOneStep = (peaks[1][i+1] - peaks[1][i]) / 1000
            stepFreq.append(1 / timeOneStep)

        avgStepFreq = sum(stepFreq) / max(1, len(stepFreq))

        return avgStepFreq, stepFreq
