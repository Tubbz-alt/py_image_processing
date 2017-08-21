# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12, 2017

Make a workspace file for TXM Wizard.
This will identify the folder with the files, the file names, and the offsets.
This script will create an easier way to set rotation offset and change a
linear change in sample height.

@author: andykiss
"""
import os
import numpy as np
import txm_image


# %% User parameters
fn_workspace = 'workspace.txt'
path = r'C:\Users\andykiss\Documents\tmp_work_dir\CAAM\LENS_1_300_02_top\refcorr_bin4\imghandled\\'
ext = 'tif'

# X, Y offsets
delx = -4
dely = 0


# %% Find the files
fn = os.listdir(path)
fn.sort()
N = np.size(fn)
ind = 0

# Remove non-BIM files
fn_rm = []
for i in range(len(fn)):
    if (not fn[i].endswith(ext)):
        fn_rm.append(fn[i])
for i in range(len(fn_rm)):
    fn.remove(fn_rm[i])

# Get image sizes and calculate offsets
N = np.size(fn)
(img, meta) = txm_image.read_file(path + fn[ind], verbose=False)
# X = np.round(meta.width / 2.0 + delx)
# Y = meta.height // 2
X = np.round(612 / 2.0 + delx)
Y = 512 // 2
Y_new = Y * np.ones((N, ), dtype=np.float)
offset = (dely / np.float(N - 1)) * np.linspace(0, N-1, num=N, dtype=np.float)
Y_new = np.round(Y_new + offset)


# %% Write the workshop file
f = open(path + fn_workspace, 'w')
f.write(path + '\n')
for i in range(N):
    f.write('%s\t%d\t%d\n' % (fn[i], Y_new[i], X))
f.write('ROIregion12\t-0001\t-0001\n')
f.write('ROIregion34\t-0001\t-0001\n')
f.flush()
f.close()

print('done')
