# -*- coding: utf-8 -*-

"""
This module will manipulate images in a similar way to Image Handling in
TXM Wizard

Written by: Andy Kiss
Started: 2017-01-27
Last modified: 2017-01-27
"""


import numpy as np
from scipy.ndimage.interpolation import rotate


def rotate_image(img, angle):
    """
    This function will rotate a NumPy array, representing an image, clockwise
    by angle degrees.

    Parameters
    ----------
    img -- 2D NumPy array
        the image to be rotated
    angle -- float
        the amount to rotate the sample clockwise by in degrees

    Returns
    -------
    img_rot -- 2D NumPy array
        the rotated image
    """

    # Use SciPy to rotate the image
    img_rot = rotate(img, angle)

    # Return the image
    return img_rot


def bin_image(img, binning):
    """
    This function will bin a NumPy array, representing an image.

    Parameters
    ----------
    img -- 2D NumPy array
        the image to be binned
    binning -- int
        the amount to bin the image

    Returns
    -------
    img_bin -- 2D NumPy array
        the binned image
    """

    # Use SciPy to rotate the image
    # img_bin = rotate(img, angle)

    # Return the image
    return img_bin
