# -*- coding: utf-8 -*-

"""
Apply a flat-field and dark-field correction.

Written by: Andy Kiss
Started: 2017-01-25
Last modified: 2017-01-25

"""


import numpy as np


def external_reference(img, ff, df=None, flag_remove_neg=True):
    """
    Apply a flat-field and dark-field corrections to an image

    Parameters
    ----------
    img -- NumPy array
        a 2D array representing the image
    ff -- NumPy array
        a 2D array representing the flat-field image
    df -- NumPy array (optional)
        a 2D array representing the dark-field image

    Returns
    -------
    proj -- NumPy array
        returns the reference corrected image

    """

    # Check that all images are not integers
    img = img.astype(dtype=np.float32)
    ff = ff.astype(dtype=np.float32)
    if (df is not None):
        df = df.astype(dtype=np.float32)

    # Subtract the dark field
    if (df is not None):
        img = img - df
        ff = ff - df

    # Perform reference correction
    proj = img / ff
    proj = -1 * np.log(proj)

    # Check for NaN
    proj[np.isnan(proj)] = 0

    # Check for inf
    max_real = np.amax(proj[np.isfinite(proj)])
    proj[np.isinf(proj)] = max_real

    # Remove negative values
    if (flag_remove_neg):
        proj[proj < 0] = 0

    # Return the image
    return proj
