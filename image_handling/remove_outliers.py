# -*- coding: utf-8 -*-

"""
Remove Outliers

This function is designed to remove bright outliers from 2D arrays (images).
It does this by comparing this array value to the mean of the surrounding
values. If the array value exceeds a threshold, then it is replaced by the mean
of the surrounding pixels.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-01-25

"""


import numpy as np
import scipy.ndimage.filters as filters


def remove_outliers(arr, delta=100, radius=2):
    """ Remove outliers from a 2D NumPy array.

    Parameters
    ----------
    arr -- 2D NumPy array
        the input array to remove outliers
    delta -- float (optional)
        the difference necessary to replace the array value with the mean of
        the surrounding values
    radius -- int (optional)
        the radius around each value to search around

    Returns
    -------
    2D NumPy array
        a new array with the outliers removed

    """
    # Assume that the array is a 2D array that is much larger than the radius
    h, w = arr.shape

    # Make a duplicate array
    arr_new = np.zeros((h, w))

    # Make the location and averaging array
    L = 2 * radius + 1
    x0 = L * radius + radius
    x_loc = np.concatenate((np.arange(0, x0, dtype=np.int),
                            np.arange(x0 + 1, L*L, dtype=np.int)))
    arr_avg = np.zeros((L * L, ))

    # Start looping
    for i in range(h):
        loc_i = np.linspace(i - radius, i + radius,
                            num=L, dtype=np.int)
        for k in range(L):
            if (loc_i[k] < 0):
                loc_i[k] = np.abs(loc_i[k])
            if (loc_i[k] > (h - 1)):
                loc_i[k] = (h - 1) - (loc_i[k] - (h - 1))

        for j in range(w):
            loc_j = np.linspace(j - radius, j + radius,
                                num=L, dtype=np.int)
            for k in range(L):
                if (loc_j[k] < 0):
                    loc_j[k] = np.abs(loc_j[k])
                if (loc_j[k] > (w - 1)):
                    loc_j[k] = (w - 1) - (loc_j[k] - (w - 1))

            # Build the average matrix
            for ii in range(L):
                for jj in range(L):
                    arr_avg[jj + L*ii] = arr[loc_i[ii], loc_j[jj]]

            # Calculate the mean
            x_bar = np.mean(arr_avg[x_loc])

            # check for outlier
            if (arr[i, j] > (x_bar + delta)):
                arr_new[i, j] = x_bar
            else:
                arr_new[i, j] = arr[i, j]

    # Return the new array
    return arr_new


def remove_outliers_scipy(arr, delta=100, radius=3):
    """ Remove outliers from a 2D NumPy array using SciPy.
    Based on the algorithm in TomoPy

    Parameters
    ----------
    arr -- 2D NumPy array
        the input array to remove outliers
    delta -- float (optional)
        the difference necessary to replace the array value with the mean of
        the surrounding values
    radius -- int (optional)
        the radius around each value to search around

    Returns
    -------
    2D NumPy array
        a new array with the outliers removed

    """

    # Calculate the median image
    row, col = arr.shape
    arr_med = np.zeros((row, col))
    filters.median_filter(arr, size=radius, output=arr_med)

    # If the pixel value plus delta is greater than the median value,
    # replace it
    arr_new = arr
    (locx, locy) = np.where((arr_new - arr_med) > delta)
    arr_new[locx, locy] = arr_med[locx, locy]

    # Return the new array
    return arr_new
