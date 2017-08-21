# -*- coding: utf-8 -*-

"""
A collection of functions for averaging image stacks.

Written by: Andy Kiss
Started: 2017-01-25
Last modified: 2017-01-25

"""


import numpy as np


def average_image_stack(img, axis=0):
    """
    Average a NumPy array along the provided axis

    The Numpy array will typically represent an image stack

    Parameters
    ----------
    img -- NumPy array
        a 3D array where the first dimension is the index of each image.
        img[0, :, :] represents the first image
    axis -- int (default = 0)
        the axis to average over

    Returns
    -------
    avg_img -- NumPy array
        returns the averaged image

    """
    # Average the images
    avg_img = np.mean(img, axis, dtype=np.float32)

    # Return the image
    return avg_img


def median_image_stack(img, axis=0):
    """
    Return the median average of a NumPy array along the provided axis

    The Numpy array will typically represent an image stack

    Parameters
    ----------
    img -- NumPy array
        a 3D array where the first dimension is the index of each image.
        img[0, :, :] represents the first image
    axis -- int (default = 0)
        the axis to median average over

    Returns
    -------
    avg_img -- NumPy array
        returns the median averaged image

    """
    # Average the images
    avg_img = np.median(img, axis)

    # Return the image
    return avg_img
