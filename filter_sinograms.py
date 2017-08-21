# -*- coding: utf-8 -*-

"""
Filter sinograms

Load the sinograms in a folder, filter them using Wavelet-Fourier filtering,
and export them to a new folder.

Parameters
----------
path -- string
    folder location of the sinograms
fn_ext -- string
    filename extension for the sinograms (*.tif, *.binsino)

Returns
-------
0 -- integer
    no errors

"""


# %% Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
import txm_image
import image_handling
from tomo_recon import astra_recon


# %% Set parameters
path = r'C:\Users\andykiss\Documents\tmp_work_dir\CAAM\2017Jul\20170723_110810_ATI_powder-processing\bim\imghandled\croped\sinos\\'
fn_ext = '.binsino'

# Output files in this directory
out_dir = 'filtered_sinogram\\'

# Filtering parameters
strWave = 'sym16'
nLevels = 6
sig = 2.0

# Flag to run the reconstruction
flag_recon = True
# CPU: FP, BP, FBP, SIRT, SART, ART, CGLS
# GPU: FP_CUDA, BP_CUDA, FBP_CUDA, SIRT_CUDA, SART_CUDA, CGLS_CUDA, EM_CUDA
alg = 'FBP_CUDA'


# %% Preprocessing
# Go to the directory
try:
    os.stat(path)
except:
    print('There was an error locating the starting folder.')
    raise SystemExit
os.chdir(path)

# Identify the total number of sinograms in the folder
ls_dir = os.listdir(path)
ls_dir.sort()
ls_rm = []
num = len(ls_dir)
for i in range(num):
    if (not ls_dir[i].endswith(fn_ext)):
        ls_rm.append(ls_dir[i])
for i in range(len(ls_rm)):
    ls_dir.remove(ls_rm[i])
num = len(ls_dir)

if (num == 0):
    print('There were no sinograms found.')
    raise SystemExit
else:
    print('There were %d sinograms found.' % (num))

# Create the filtered directory if not already created
try:
    os.stat(path + out_dir)
except:
    try:
        os.mkdir(path + out_dir)
    except:
        print('There was an error creating the export directory.')
        raise SystemExit

# %% Test filtering one image
test_i = num // 2
# test_i = ls_proj.index('_00308.binsino')

# Update progress
print('Processing test sinogram...', end='')

# Load the sinogram
(sino, th) = txm_image.read_file(path+ls_dir[test_i], verbose=False)

# Filter the sinogram
sino_filtered = image_handling.wf_filter(sino.T, N_levels=nLevels,
                                         waveletName=strWave, sigma=sig,
                                         pad=10, forceZero=True)

# Rotate the sinogram and crop to the original size
sino_filtered = sino_filtered.T
sino_size = np.shape(sino)[0]
sino_filtered = sino_filtered[0:sino_size, :]

# Update status
print('done')

# Export the sinogram
txm_image.write_file(path+out_dir+ls_dir[test_i]+'.binsino',
                     sino_filtered, th,
                     verbose=False)

# Run the reconstruction
if (flag_recon):
    print('Reconstructing sinogram...', end='')
    V = astra_recon(sino_filtered.T, th, algorithm=alg)
    # (row, col) = V.shape
    # ML_size = 2 * np.floor(row / (2 * np.sqrt(2)))
    # ML_X = np.int(np.ceil(0.5 * (row - ML_size)))
    # V = V[ML_X:row-ML_X, ML_X:col-ML_X]
    print('done')

    # Display the reconstruction
    plt.figure(1)
    plt.ion()
    plt.imshow(V, cmap='gray', vmin=np.amin(V), vmax=np.amax(V))
    plt.title('Filtered Reconstruction')
    plt.show(block=False)
    plt.pause(0.001)


# Wait for user response
ans = input('Would you like to continue? (Y/n) ')
if (ans == 'Y' or ans == 'y'):
    print('\n')
else:
    print('\n')
    raise SystemExit

# %% Start filtering all the images
for i in range(num):
    # Update the progress
    print('Processing sinogram (%04d/%04d)...' % (i+1, num), end='')

    # Load the sinogram
    (sino, th) = txm_image.read_file(path+ls_dir[i], verbose=False)

    # Filter the sinogram
    sino_filtered = image_handling.wf_filter(sino.T, N_levels=nLevels,
                                             waveletName=strWave, sigma=sig,
                                             pad=10, forceZero=True)

    # Rotate the sinogram and crop to the original size
    sino_filtered = sino_filtered.T
    sino_size = np.shape(sino)[0]
    sino_filtered = sino_filtered[0:sino_size, :]

    # Export the sinogram
    txm_image.write_file(path+out_dir+ls_dir[i]+'.binsino',
                         sino_filtered, th,
                         verbose=False)

    # Success
    print('done')


# %% Clean up and exit
# Clean up some memory
del sino, sino_filtered, th

# Exit
print('\nFiltering completed successfully.')
