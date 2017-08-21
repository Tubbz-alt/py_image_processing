# -*- coding: utf-8 -*-

"""
This module will load BIM files that are used by the microCT and TXM.
The read functions will return any metadata associated with the file along with
a NumPy array of the image information.
The write functions will require the necessary metadata and the image in a
NumPy array.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07
"""


import numpy as np


class metadata:
    """
    Define a class to hold the metadata
    """
    def __init__(self):
        self.width = []
        self.height = []
        self.angles = []
        self.pixelsize = []
        self.HBin = []
        self.VBin = []
        self.energy = []
        self.MotPos = []
        self.AxisNames = []
        self.ExpTimes = []
        self.ImagesTaken = []
        self.datatype = []
        self.date = []


def create_metadata(img=None):
    """ Create a blank (default) metadata object

    Parameters
    ----------
    img -- NumPy array (optional)
        an image as a NumPy array

    Returns
    -------
    meta -- metadata class
        a metadata class with default information

    """

    # Create the metadata class
    meta = metadata()

    # Start inserting (default) values
    if (img is None):
        [meta.height, meta.width] = [1024, 1024]
    else:
        [meta.height, meta.width] = img.shape
    meta.angles = 0.0
    meta.pixelsize = 1.0
    meta.HBin = 1
    meta.VBin = 1
    meta.energy = 0.0
    meta.MotPos = np.zeros((20, 1))
    meta.AxisNames = 'Sample X            Sample Y            ' \
                     'Sample Z            Sample Theta        ' \
                     'Condenser X         Condenser Y         ' \
                     'Condenser Z         Condenser Tip       ' \
                     'Condenser Tilt      Pinhole X           ' \
                     'Pinhole Y           Pinhole Z           ' \
                     'Zoneplate X         Zoneplate Y         ' \
                     'Zoneplate Z         Phasering X         ' \
                     'Phasering Y         Phasering Z         ' \
                     'Phasering W         Tubelens            '
    meta.ExpTimes = 1.0
    meta.ImagesTaken = 1
    meta.datatype = 'float32'
    meta.date = '03/21/1988 22:00'

    # Return the created metadata
    return meta


def create_metadata_from_scanlog(scanlog):
    """ Create a metadata object based on input from a microCT scanlog
    file

    Parameters
    ----------
    scanlog -- scanlog class
        a scanlog class with the scan information

    Returns
    -------
    meta -- metadata class
        a metadata class with the scanlog information

    """

    # Create the metadata class
    meta = metadata()

    # Start inserting values from scanlog
    [meta.height, meta.width] = [scanlog.V_RES, scanlog.H_RES]
    meta.angles = 0.0
    meta.pixelsize = scanlog.px / scanlog.binning
    meta.HBin = scanlog.binning
    meta.VBin = scanlog.binning
    meta.energy = scanlog.eV
    meta.MotPos = np.zeros((20, 1))
    meta.AxisNames = 'Sample X            Sample Y            ' \
                     'Sample Z            Sample Theta        ' \
                     'Condenser X         Condenser Y         ' \
                     'Condenser Z         Condenser Tip       ' \
                     'Condenser Tilt      Pinhole X           ' \
                     'Pinhole Y           Pinhole Z           ' \
                     'Zoneplate X         Zoneplate Y         ' \
                     'Zoneplate Z         Phasering X         ' \
                     'Phasering Y         Phasering Z         ' \
                     'Phasering W         Tubelens            '
    meta.ExpTimes = scanlog.exp_ms
    meta.ImagesTaken = 1
    meta.datatype = 'float32'
    meta.date = '03/21/1988 22:00'

    # Return the created metadata
    return meta


def read_bim(fn_img):
    """ Function to read a BIM file

    Parameters
    ----------
    fn_img -- string
        a string with the location of the filename

    Returns
    -------
    img -- NumPy array
        a NumPy array of the image
    meta -- class metadata
        a metadata class with the image information

    """

    # Define a local function to convert the byte characters to a string
    def bytechar2str(inchar):
        try:
            outstr = str(inchar, 'utf-8')
        except:
            outstr = ''
            for i in inchar:
                try:
                    outstr += str(i, 'utf-8')
                except:
                    outstr += ' '
        return outstr

    # Open the file
    f = open(fn_img, 'rb')

    # Initialize metadata variable
    meta = metadata()

    # Start reading in data
    # Read in string lengths
    tmp = np.fromfile(f, dtype=np.uint32, count=4)
    MotPosL = tmp[0]
    datatypeL = tmp[1]
    dateL = tmp[2]
    AxisNamesL = tmp[3]

    # Read in image properties
    tmp = np.fromfile(f, dtype=np.uint32, count=2)
    meta.width = tmp[0]  # pixels
    meta.height = tmp[1]  # pixels
    tmp = np.fromfile(f, dtype=np.float64, count=1)
    meta.angles = tmp[0]  # radians
    tmp = np.fromfile(f, dtype=np.float32, count=1)
    meta.pixelsize = tmp[0]  # microns
    tmp = np.fromfile(f, dtype=np.uint32, count=2)
    meta.HBin = tmp[0]  # pixels
    meta.VBin = tmp[1]  # pixels
    tmp = np.fromfile(f, dtype=np.float64, count=1)
    meta.energy = tmp[0]  # eV

    # Read motor positions into array
    tmp = np.fromfile(f, dtype=np.float32, count=MotPosL)
    meta.MotPos = tmp

    # Read motor labels
    tmp = np.fromfile(f, dtype='c', count=AxisNamesL)
    # meta.AxisNames = ''.join([chr(i) for i in tmp])
    # meta.AxisNames = ''.join(tmp)
    # meta.AxisNames = str(tmp, 'utf-8')
    meta.AxisNames = bytechar2str(tmp)

    tmp = np.fromfile(f, dtype=np.float32, count=1)
    meta.ExpTimes = tmp[0]  # seconds
    tmp = np.fromfile(f, dtype=np.uint32, count=1)
    meta.ImagesTaken = tmp[0]  # number of images taken

    # Read in datatype
    tmp = np.fromfile(f, dtype='c', count=datatypeL)
    # meta.datatype = ''.join(tmp)
    # meta.datatype = ''.join([chr(i) for i in tmp])
    meta.datatype = bytechar2str(tmp)

    # Read in date
    tmp = np.fromfile(f, dtype='c', count=dateL)
    # meta.date = ''.join(tmp)
    # meta.date = ''.join([chr(i) for i in tmp])
    meta.date = bytechar2str(tmp)

    # Read in image data
    img = np.fromfile(f, dtype=np.float32, count=meta.height*meta.width)
    img = np.reshape(img, (meta.height, meta.width), order='F')

    # Close the file
    f.close

    # Return data
    return img, meta


def write_bim(fn, img, meta=None):
    """ Function to write a BIM file

    Parameters
    ----------
    fn -- string
        a string with the filename
    img -- NumPy array
        a NumPy array with the image to be written
    meta -- class metadata (optional)
        a metadata class with the image information

    Returns
    -------
    None

    """

    # Look for metadata and create some if not provided
    if (meta is None):
        meta = create_metadata(img)

    # Open the file
    f = open(fn, 'wb')

    # Write string lengths
    MotPosL = len(meta.MotPos)
    datatypeL = len(meta.datatype)
    dateL = len(meta.date)
    AxisNamesL = len(meta.AxisNames)
    tmp = np.array([MotPosL, datatypeL, dateL, AxisNamesL], dtype=np.uint32)
    tmp.tofile(f)

    # Write image properties
    tmp = np.array([meta.width, meta.height], dtype=np.uint32)
    tmp.tofile(f)
    tmp = np.array([meta.angles], dtype=np.float64)
    tmp.tofile(f)
    tmp = np.array([meta.pixelsize], dtype=np.float32)
    tmp.tofile(f)
    tmp = np.array([meta.HBin, meta.VBin], dtype=np.uint32)
    tmp.tofile(f)
    tmp = np.array([meta.energy], dtype=np.float64)
    tmp.tofile(f)

    # Write motor positions
    tmp = np.array(meta.MotPos, dtype=np.float32)
    tmp.tofile(f)

    # Write motor labels
    # tmp = np.array(meta.AxisNames, dtype=np.chararray)
    tmp = np.array(list(meta.AxisNames), dtype='c')
    tmp.tofile(f)

    tmp = np.array(meta.ExpTimes, dtype=np.float32)
    tmp.tofile(f)
    tmp = np.array(meta.ImagesTaken, dtype=np.uint32)
    tmp.tofile(f)

    # Write datatype
    # tmp = np.array(meta.datatype, dtype=np.chararray)
    tmp = np.array(list(meta.datatype), dtype='c')
    tmp.tofile(f)

    # Write date
    # tmp = np.array(meta.date, dtype=np.chararray)
    tmp = np.array(list(meta.date), dtype='c')
    tmp.tofile(f)

    # Write image data
    tmp = img.astype(dtype=np.float32)
    np.transpose(tmp).tofile(f)

    # Close the file
    f.close

    # Return
    return

