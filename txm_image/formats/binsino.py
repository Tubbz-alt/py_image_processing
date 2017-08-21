# -*- coding: utf-8 -*-

"""
This module will load BINSINO files.
The read functions will return a NumPy array of the image and angle information
The write functions will require the image in a NumPy array.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07
"""


import numpy as np


def read_binsino(fn):
    """ Function to read a binsino file

    Parameters
    ----------
    fn -- string
        a string with the file name

    Returns
    -------
    img -- NumPy array
        a NumPy array of the image
    th -- NumPy array
        a NumPy array of the angles

    """

    # Open the file
    f = open(fn, 'rb')

    # Get the size of the file
    tmp = np.fromfile(f, dtype=np.float32, count=2)
    h = np.int(tmp[0])
    w = np.int(tmp[1])

    # Read in all the data
    tmp = np.fromfile(f, dtype=np.float32, count=w*h)
    tmp = np.reshape(tmp, (h, w), order='F')

    # Isolate the angle information
    th = tmp[0, :]

    # Isolate the sinogram
    sino = tmp[1:, :]

    # Close the file
    f.close

    # Return the sinogram and angle information
    return sino, th


def write_binsino(fn, sino, th):
    """ Function to write a binsino file

    Parameters
    ----------
    fn -- string
        a string with the filename
    sino -- NumPy array
        a NumPy array of the sinogram
    th -- NumPy array
        a NumPy array with the angle information

    Returns
    -------
    0 -- for success
    -1 -- for error creating file

    """

    # Open the file
    try:
        f = open(fn, 'wb')
    except:
        print('Error: Could not create file.')
        return -1

    # Start writing data
    # Write image size
    h = sino.shape[0] + 1
    w = sino.shape[1]
    size = np.array([h, w], dtype='float32')
    size.tofile(f)

    # Collect and write the data
    tmp = np.zeros((h, w), dtype='float32')
    tmp[0, :] = th
    tmp[1:, :] = sino
    tmp = tmp.T
    tmp.tofile(f)

    # Close the file
    f.close

    # Return success
    return 0

