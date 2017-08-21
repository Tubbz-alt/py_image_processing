# -*- coding: utf-8 -*-
"""
Center projections and createsinograms

Created on Sat Aug 19 15:50:17 2017

@author: andykiss
"""


import numpy as np
import matplotlib.pyplot as plt
import os

import sys
mod_path = r'C:\Users\andykiss\Documents\programming\python\\'
if (mod_path not in sys.path):
    sys.path.append(mod_path)
import txm_image
import image_handling


# %% Settings
# File names and location
root = r'C:\Users\andykiss\Documents\tmp_work_dir\CAAM\2017Jul\20170723_110810_ATI_powder-processing\bim\imghandled'
ext = '.bim'

# True rotation axis
rot_axis = 521.7

# Ring removal settings
flag_ring_removal = True
wf_str = 'sym16'
wf_N = 6
wf_sig = 2.0

# Output directory
outdir = 'sinos\\'


# %% Find the files
if (root[-1] != '\\' and root[-1] != '/'):
    root += '/'

ls = os.listdir(root)
for fn in ls:
    if (not fn.endswith(ext)):
        ls.remove(fn)
N = len(ls)


# %% Load the files
# Load the first file to get projection size
I, meta = txm_image.read_file(root + ls[0], verbose=False)
row, col = np.shape(I)
th = np.array([], dtype=np.float32)
th = np.append(th, meta.th)

# Initialize the projection array
proj = np.empty((N, row, col), dtype=np.float32)
proj[0, :, :] = I

# Load the files
for i in range(1, N):
    I, meta = txm_image.read_file(root + ls[i], verbose=False)
    proj[i, :, :] = I
    th = np.append(th, meta.th)

# Cleanup
del I


# %% Offset the projections
# rot_axis = np.round(rot_axis)
shift = (col / 2) - rot_axis
shift = 2 * np.round(shift)

blank_roi = np.zeros((N, row, shift), dtype=np.float32)
if (shift < 0):
    proj = np.concatenate((blank_roi, proj), axis=1)
elif (shift > 0):
    proj = np.concatenate((proj, blank_roi), axis=1)

# Cleanup
del blank_roi


# %% Filter sinograms
if (flag_ring_removal):
    print('Filtering sinograms...', end='')
    for i in range(row):
        # Isolate the sinogram
        sino = proj[:, i, :]

        # Filter the sinogram
        sino_f = image_handling.wf_filter(sino.T, N_levels=wf_N,
                                          waveletName=wf_str, sigma=wf_sig,
                                          pad=10, forceZero=True)

        # Rotate the sinogram and crop to the original size
        sino_f = sino_f.T
        sino_size = np.shape(sino)[0]
        sino_f = sino_f[0:sino_size, :]

        # Replace the projection with the filtered sinogram
        proj[:, i, :] = sino_f

# Cleanup
del sino, sino_f, sino_size

print('done')


# %% Export sinograms
for i in range(row):
    print('Writing sinogram (%04d/%04d)...' % (i+1, row), end='')
    txm_image.write_file(root+outdir+fn, proj[:, i, :], th)
    print('done')


# %% Finish script
del proj

print('\nCreating sinograms complete.\n')
