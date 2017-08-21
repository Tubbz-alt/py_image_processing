# -*- coding: utf-8 -*-

"""
This module will load different files that are used by the microCT and TXM.
Each format file, will include a read and write function.
The read functions will return any metadata associated with the file along with
a NumPy array of the image information.
The write functions will require the necessary metadata and the image in a
NumPy array.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07
"""

import numpy as np
import txm_image.formats
import txm_image.microCT_scanlog
from txm_image.add_metadata import add_metadata_to_img
from txm_image.add_metadata import add_metadata_to_files


def read_file(fn, verbose=True):
    """ A general function to read images

    Parameters
    ----------
    fn -- string
        a string with the location of the file to be opened
    verbose -- boolean (default=True)
        a flag for extra output to the console

    Returns
    -------
    img -- NumPy array
        a NumPy array of the loaded image
    meta -- class metadata
        a metadata class with the image information

    """

    # Redirect to the correct import function
    if (fn.endswith('.bim') or fn.endswith('.BIM')):
        if (verbose):
            print('Importing BIM file.')
        img, meta = formats.bim.read_bim(fn)
    elif (fn.endswith('.tif') or fn.endswith('.TIF')):
        if (verbose):
            print('Importing TIFF file.')
        img = formats.tiff.read_tiff_stack_io(fn)
        meta = None
    elif (fn.endswith('.binprj') or fn.endswith('.BINPRJ')):
        if (verbose):
            print('Importing binprj file.')
        img = formats.binfile.read_bin(fn)
        meta = None
    elif (fn.endswith('.binslice') or fn.endswith('.BINSLICE')):
        if (verbose):
            print('Importing binslice file.')
        img = formats.binfile.read_bin(fn)
        meta = None
    elif (fn.endswith('.binsino') or fn.endswith('.BINSINO')):
        if (verbose):
            print('Importing binsino file.')
        (img, meta) = formats.binsino.read_binsino(fn)
        # meta = None
    else:
        print('The image format was not found.')
        img = None
        meta = None

    return img, meta


def write_file(fn, img, meta=None, verbose=True):
    """ A general function to write images

    Parameters
    ----------
    fn -- string
        a string with the location of the file to be written
    img -- NumPy array
        a NumPy array of the image
    meta -- class metadata (optional, default=None)
        a metadata class with the image information
    verbose -- boolean (default=True)
        a flag for extra output to the console

    Returns
    -------
    None

    """

    # Redirect to the correct import function
    if (fn.endswith('.bim') or fn.endswith('.BIM')):
        if (verbose):
            print('Exporting BIM file.')
        formats.bim.write_bim(fn, img, meta)
    elif (fn.endswith('.tif') or fn.endswith('.TIF')):
        if (verbose):
            print('Exporting TIFF file.')
        formats.tiff.write_tiff_stack_io(fn, img)
    elif (fn.endswith('.binprj') or fn.endswith('.BINPRJ')):
        if (verbose):
            print('Exporting binprj file.')
        formats.binfile.write_bin(fn, img)
    elif (fn.endswith('.binslice') or fn.endswith('.BINSLICE')):
        if (verbose):
            print('Exporting binslice file.')
        formats.binfile.write_bin(fn, img)
    elif (fn.endswith('.binsino') or fn.endswith('.BINSINO')):
        if (verbose):
            print('Exporting binsino file.')
        formats.binsino.write_binsino(fn, img, meta)
    else:
        print('The image format was not found.')

    return
