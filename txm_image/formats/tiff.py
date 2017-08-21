# -*- coding: utf-8 -*-

"""
This module will load individual TIFF files or TIFF stacks.
The read functions will return a NumPy array of the image.
The write functions will require the image in a NumPy array.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07
"""


from PIL import Image
from skimage.io import imread, imsave
import numpy as np
import txm_image


def read_tiff(fn, ind=0):
    """ Load a TIFF file

    Parameters
    ----------
    fn -- string
        a string with the filename
    ind -- integer (default=0)
        a specific page to look at in the TIFF stack

    Returns
    -------
    img -- NumPy array
        a NumPy array of the image

    """

    # Open the file
    f = Image.open(fn)
    f.seek(ind)

    # Initialize an array
    [w, h] = f.size
    img = np.empty((h, w))

    # Read in the image stack
    img[:, :] = np.array(f)

    # Close the file
    f.close

    return img


def read_tiff_stack(fn):
    """ Load a TIFF stack

    Parameters
    ----------
    fn -- string
        a string with the filename

    Returns
    -------
    img -- NumPy array
        a NumPy array of the images

    """

    # Open the file
    f = Image.open(fn)

    N = txm_image.formats.tiff.tiff_stack_size(fn)

    # Get image size
    (w, h) = f.size

    # Initialize and read
    if (N == 1):
        img = np.empty((h, w), dtype=np.float32)
        img[:, :] = np.array(f, dtype=np.float32)
    else:
        img = np.empty((N, h, w), dtype=np.float32)
        # Read in the image stack
        for i in range(N):
            f.seek(i)
            img[i, :, :] = np.array(f)

    # Close the file
    f.close

    return img


def read_tiff_stack_io(fn):
    """ Load a TIFF stack

    Parameters
    ----------
    fn -- string
        a string with the filename

    Returns
    -------
    img -- NumPy array
        a NumPy array of the images

    """

    # Read the file
    I = imread(fn)

    # Convert to a NumPy array as float32
    img = np.array(I, dtype=np.float32)

    # Garbage collection
    del I

    # Return img
    return img


def tiff_stack_size(fn):
    """ Determine the TIFF stack size

    Parameters
    ----------
    fn -- string
        a string with the filename

    Returns
    -------
    i -- integer
        the size of the TIFF stack

    """

    # Open the file
    f = Image.open(fn)

    # Determine the number of images in the TIFF stack
    i = 0
    f.seek(i)
    while (True):
        try:
            f.seek(i)
            i += 1
        except EOFError:
            break

    # Close the file
    f.close()

    # Return the number of images in the stack
    return i


def write_tiff(fn, img):
    """ Write a TIFF file

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

    # Convert the NumPy array to an Image and then save
    img_tmp = Image.fromarray(img)
    img_tmp.save(fn)

    return


def write_tiff_stack_io(fn, img):
    """ Write a TIFF stack

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

    # Ensure the image stack is float32
    img = np.array(img, dtype=np.float32)

    # Write the imag
    imsave(fn, img)

    # Return
    return