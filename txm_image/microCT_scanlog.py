# -*- coding: utf-8 -*-

"""
This function will read the scan information from a microCT scan log.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07
"""


class scan_metadata:
    """
    Define a class to hold the scan data
    """
    def __init__(self):
        self.sample_name = []
        self.eV = []
        self.obj = []
        self.bit = []
        self.unbinned_px = []
        self.binning = []
        self.px = []
        self.H_RES = []
        self.V_RES = []
        self.th_start = []
        self.th_end = []
        self.th_step = []
        self.num_proj = []
        self.flag_fly_scan = []
        self.traj = []
        self.exp_ms = []
        self.rest_ms = []
        self.num_exp = []
        self.num_rows = []
        self.num_cols = []
        self.num_mos = []
        self.vel = []
        self.X = []
        self.Y = []
        self.Z = []
        self.flag_df = []
        self.flag_ref = []
        self.num_ref = []
        self.refX = []
        self.refY = []
        self.refZ = []


def read_log(fn):
    """ Open the log file and read in the experimental parameters

    Parameters
    ----------
    fn -- string
        a string the with scan log location

    Returns
    -------
    meta -- class metadata
        a metadata class with the scan log information

    """

    # Create the metadata structure
    meta = scan_metadata()

    # Open the log file and read in the data
    fLOG = open(fn, 'r')
    LOG = fLOG.read()
    fLOG.close()

    # Start parsing the data in the log file
    a = LOG.find('SAMPLE NAME') + 13
    b = LOG[a:].find('\n') + a
    meta.sample_name = LOG[a:b]

    a = LOG.find('ENERGY') + 13
    b = LOG[a:].find('\n') + a
    meta.eV = float(LOG[a:b])

    a = LOG.find('OBJECTIVE') + 11
    b = LOG[a:].find('\n') + a
    meta.obj = float(LOG[a:b])

    a = LOG.find('BIT DEPTH') + 11
    b = LOG[a:].find('\n') + a
    meta.bit = int(LOG[a:b])

    a = LOG.find('UNBINNED') + 30
    b = LOG[a:].find('\n') + a
    meta.unbinned_px = float(LOG[a:b])

    a = LOG.find('BINNING') + 9
    b = LOG[a:].find('\n') + a
    meta.binning = int(LOG[a:b])

    a = LOG.find('ACTUAL') + 28
    b = LOG[a:].find('\n') + a
    meta.px = float(LOG[a:b])

    a = LOG.find('H_RES') + 6
    b = LOG[a:].find('\n') + a
    meta.H_RES = int(LOG[a:b])

    a = LOG.find('V_RES') + 6
    b = LOG[a:].find('\n') + a
    meta.V_RES = int(LOG[a:b])

    a = LOG.find('STARTING THETA') + 15
    b = LOG[a:].find('\n') + a
    meta.th_start = float(LOG[a:b])

    a = LOG.find('FINISHING THETA') + 16
    b = LOG[a:].find('\n') + a
    meta.th_end = float(LOG[a:b])

    a = LOG.find('STEP THETA') + 11
    b = LOG[a:].find('\n') + a
    meta.th_step = float(LOG[a:b])

    a = LOG.find('NUMBER OF PROJECTIONS') + 22
    b = LOG[a:].find('\n') + a
    meta.num_proj = int(LOG[a:b])

    a = LOG.find('FLY') + 10
    b = LOG[a:].find('\n') + a
    if (LOG[a:b] == 'True'):
        meta.flag_fly_scan = True
    else:
        meta.flag_fly_scan = False

    a = LOG.find('TRAJECTORY') + 12
    b = LOG[a:].find('\n') + a
    meta.traj = LOG[a:b]

    a = LOG.find('EXPOSURE') + 19
    b = LOG[a:].find('\n') + a
    meta.exp_ms = int(LOG[a:b])

    a = LOG.find('REST') + 15
    b = LOG[a:].find('\n') + a
    meta.rest_ms = int(LOG[a:b])

    a = LOG.find('NUMBER OF EXPOSURES') + 20
    b = LOG[a:].find('\n') + a
    meta.num_exp = int(LOG[a:b])

    a = LOG.find('NUMBER OF MOSAIC ROWS') + 22
    b = LOG[a:].find('\n') + a
    meta.num_rows = int(LOG[a:b])

    a = LOG.find('NUMBER OF MOSAIC COLS') + 22
    b = LOG[a:].find('\n') + a
    meta.num_cols = int(LOG[a:b])

    a = LOG.find('NUMBER OF MOSAIC IMAGES') + 24
    b = LOG[a:].find('\n') + a
    meta.num_mos = int(LOG[a:b])

    a = LOG.find('VELOCITY') + 17
    b = LOG[a:].find('\n') + a
    meta.vel = float(LOG[a:b])

    a = LOG.find('MOTOR POS') + 16
    b = LOG[a:].find('\n') + a
    if (LOG[a:b] == '(X, Y)'):
        for i in range(meta.num_mos):
            a = b + 2
            b = LOG[a:].find(',') + a
            meta.X.append(float(LOG[a:b]))
            a = b + 1
            b = LOG[a:].find(')') + a
            meta.Y.append(float(LOG[a:b]))
    elif (LOG[a:b] == '(X, Y, Z)'):
        for i in range(meta.num_mos):
            a = LOG[b:].find('(') + b + 1
            # a = b + 2
            b = LOG[a:].find(',') + a
            meta.X.append(float(LOG[a:b]))
            a = b + 1
            b = LOG[a:].find(',') + a
            meta.Y.append(float(LOG[a:b]))
            a = b + 1
            b = LOG[a:].find(')') + a
            meta.Z.append(float(LOG[a:b]))

    a = LOG.find('DARK FIELD') + 22
    b = LOG[a:].find('\n') + a
    if (LOG[a:b] == 'True'):
        meta.flag_df = True
    else:
        meta.flag_df = False

    a = LOG.find('REFERENCE COLLECTED') + 21
    b = LOG[a:].find('\n') + a
    if (LOG[a:b] == 'True'):
        meta.flag_ref = True
    else:
        meta.flag_ref = False

    a = LOG.find('NUMBER OF REFERENCES') + 21
    b = LOG[a:].find('\n') + a
    meta.num_ref = int(LOG[a:b])

    a = LOG.find('REF POS') + 14
    b = LOG[a:].find('\n') + a
    if (LOG[a:b] == '(X, Y)' or LOG[a:b] == '(X,Y)'):
        a = b + 2
        b = LOG[a:].find(',') + a
        meta.refX = float(LOG[a:b])
        a = b + 1
        b = LOG[a:].find(')') + a
        meta.refY = float(LOG[a:b])
    elif (LOG[a:b] == '(X, Y, Z)'):
        a = b + 2
        b = LOG[a:].find(',') + a
        meta.refX = float(LOG[a:b])
        a = b + 1
        b = LOG[a:].find(',') + a
        meta.refY = float(LOG[a:b])
        a = b + 1
        b = LOG[a:].find(')') + a
        meta.refZ = float(LOG[a:b])

    # Return
    return meta

