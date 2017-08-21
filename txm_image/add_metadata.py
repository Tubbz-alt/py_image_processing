# -*- coding: utf-8 -*-

"""
Add Metadata

This function will add metadata for BIM files.

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-07

"""

import os
import numpy as np
import txm_image


def add_metadata_to_files(scanlog, path, outdir='bim\\'):
    """
    Add metadata for *.bim files

    Parameters
    ----------
    scanlog -- string
        a string with the full path and filename of the scanlog file
    path -- string
        a string with the folder location of the files to add metadata
        NOTE: the string should end in a backslash '\\'
    outdir -- string (default = 'bim\\')
        a string with the output directory for the *.bim files

    Returns
    -------
    0 -- success

    """

    # Read the scanlog
    log = txm_image.microCT_scanlog.read_log(scanlog)

    # Go to the master directory
    os.chdir(path)

    # Check for the processing directory
    try:
        os.stat(outdir)
    except:
        os.mkdir(outdir)

    # Find the files
    fn = os.listdir(path)
    fn.sort()
    fn = fn[1:]
    N = np.size(fn)
    ind = 0

    # Read the scanlog and assign some values that won't change
    meta = txm_image.formats.bim.create_metadata_from_scanlog(log)
    N_exp = log.num_exp
    N_mos = log.num_mos
    th0 = log.th_start
    del_th = log.th_step

    # Start moving through the files
    for i in range(N):
        print('Working on image (%06d/%06d)...' % (i+1, N), end='')
        tmp_img, tmp_meta = txm_image.read_file(path+fn[i])
        if (tmp_img is not None):
            ind += 1
        else:
            print('skipped')
            continue
        meta.height, meta.width = np.shape(tmp_img)
        th = th0 + np.floor(ind / np.double(N_exp) / np.double(N_mos)) * del_th
        meta.angles = np.deg2rad(th)
        meta.MotPos[3] = th

        # Convert postions to microns
        meta.MotPos[0] = log.X[ind % N_mos] * -1000.
        meta.MotPos[1] = log.Y[ind % N_mos] * 1000.

        # Write the file
        txm_image.write_file(path+outdir+fn[i]+'.bim', tmp_img, meta, verbose=False)
        print('done')

    # Return
    return 0


def add_metadata_to_img(scanlog, img, outdir='bim\\',
                        flag_Nexp=0, verbose=False):
    """
    Add metadata for images loaded in memory files

    Parameters
    ----------
    scanlog -- class scanlog
        a scanlog class already loaded into memory
    img -- NumPy array
        a NumPy array loaded in memory to add metadata to
    outdir -- string (default = 'bim\\')
        a string with the output directory for the *.bim files
    flag_Nexp -- integer
        0 - use the scanlog file for number of exposures
        N - use N number of exposures

    Returns
    -------
    0 -- success

    """

    # Check for the processing directory
    try:
        os.stat(outdir)
    except:
        os.mkdir(outdir)

    # Assign some values
    meta = txm_image.formats.bim.create_metadata_from_scanlog(scanlog)
    if (flag_Nexp == 0):
        N_exp = scanlog.num_exp
    else:
        N_exp = flag_Nexp
    N_mos = scanlog.num_mos
    th0 = scanlog.th_start
    del_th = scanlog.th_step

    # Start moving through the files
    N = np.size(img, axis=0)
    for i in range(N):
        if (verbose):
            print('Working on image (%06d/%06d)...\r' % (i+1, N), end='')
        tmp_img = img[i, :, :]
        meta.height, meta.width = np.shape(tmp_img)
        th = th0 + np.floor(i / np.double(N_exp) / np.double(N_mos)) * del_th
        meta.angles = np.deg2rad(th)
        meta.MotPos[3] = th

        # Convert postions to microns
        meta.MotPos[0] = scanlog.X[i % N_mos] * -1000.
        meta.MotPos[1] = scanlog.Y[i % N_mos] * 1000.

        # Write the file
        tmp_str = 'proj_%06d.bim' % (i)
        txm_image.write_file(outdir+tmp_str, tmp_img, meta, verbose=False)
        if (verbose):
            print('done')

    # Return
    return 0
