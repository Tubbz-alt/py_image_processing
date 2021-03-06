# -*- coding: utf-8 -*-
"""
Reconstruct the *.binsino files in a folder using ASTRA

Created on Fri Aug 18 10:04:37 2017

@author: andykiss
"""


import os
import txm_image
from tomo_recon import astra_recon


# %% Define the folders
path = r'C:\Users\andykiss\Documents\tmp_work_dir\Sandia\rad1\20170725_134911_rad1-processing\bim\sinos'
ext = '.binsino'

# ASTRA settings
alg = 'FBP_CUDA'
alg_iter = 100
px = 1.0
flag_matlab_crop = True


# %% Get the files
if (path[-1] != '\\' and path[-1] != '/'):
    path += os.sep

ls = os.listdir(path)
for fn in ls:
    if (not fn.endswith(ext)):
        ls.remove(fn)

N = len(ls)


# %% Start reconstructing
# Make output directories
outdir = 'slices' + os.sep
if (not os.path.isdir(path + outdir)):
    os.mkdir(path + outdir)
outdir = outdir + alg + os.sep
if (not os.path.isdir(path + outdir)):
    os.mkdir(path + outdir)

for i in range(N):
    print('Reconstrucing file (%04i/%04i)...' % (i+1, N), end='')
    # Load the file
    (sino, th) = txm_image.read_file(path+ls[i], verbose=False)

    # Reconstruct the file
    V = astra_recon(sino.T, th, algorithm=alg, num_iter=alg_iter,
                    px=px, flag_matlab_crop=flag_matlab_crop)

    # Save the file
    ind = ls[i].find(ext)
    fn = ls[i][0:ind] + '.binslice'
    txm_image.write_file(path+outdir+fn, V, verbose=False)

    print('done')


# %% Complete
print('\nBatch reconstruction complete.\n')
