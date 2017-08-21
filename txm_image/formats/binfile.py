# -*- coding: utf-8 -*-

"""
This module will read and write BIN files.
The read functions will return a NumPy array of the image .
The write functions will require the image in a NumPy array.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07
"""


import numpy as np


def read_bin(fn):
    """" Function to read a binprj or binslice file

    Parameters
    ----------
    fn -- string
        a string with the filename

    Returns
    -------
    img -- NumPy array
        a NumPy array of the image

    """

    # Open the file
    f = open(fn, 'rb')

    # Get the size of the file
    tmp = np.fromfile(f, dtype=np.float32, count=2)
    h = np.int(tmp[0])
    w = np.int(tmp[1])

    # Initialize image array
    img = np.zeros((h, w), dtype='float32')

    # Read in values
    img = np.fromfile(f, dtype=np.float32, count=h*w)
    img = np.reshape(img, (h, w), order='F')

    # Close the file
    f.close

    # Return the image as a NumPy array
    return img


def write_bin(fn, img):
    """ Function to write a binprj or binslice file

    Parameters
    ----------
    fn -- string
        a string with the filename
    img -- NumPy array
        a NumPy array of the image

    Returns
    -------
    None

    """

    # Open the file
    f = open(fn, 'wb')

    # Get the size of the array and write it to the file
    tmp = img.shape
    np.array(tmp, dtype=np.float32).tofile(f)

    # Reshape and write
    # img = np.reshape(img, (tmp[1], tmp[0]), order='C')
    img = img.T
    img.tofile(f)

    # Close the file
    f.close

    # Return
    return
