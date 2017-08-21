# -*- coding: utf-8 -*-
"""
Find Rotation Center

Created on Sat Aug 19 14:46:46 2017

@author: andykiss
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import register_translation
from skimage.transform import warp, SimilarityTransform

import sys
mod_path = r'C:\Users\andykiss\Documents\programming\python\\'
if (mod_path not in sys.path):
    sys.path.append(mod_path)
import txm_image


# %% Registration Settings
# File names and location
root = r'C:\Users\andykiss\Documents\tmp_work_dir\CAAM\2017Jul\20170723_110810_ATI_powder-processing\bim\imghandled'
fn0 = 'proj_000000.bim.bim'
fn1 = 'proj_000360.bim.bim'

# Upscaling factor
up = 10


# %% Perform registration
# Check root path
if (root[-1] != '\\' and root[-1] != '/'):
    root += '/'

# Load files
I0, _ = txm_image.read_file(root + fn0, verbose=False)
I1, _ = txm_image.read_file(root + fn1, verbose=False)

# Flip I1 left-right
I1 = np.fliplr(I1)

# Calculate the shift (dely, delx)
shift, _, _ = register_translation(I0, I1, upsample_factor=up)

# Convert for transform (delx, dely)
shift = np.flipud(shift)
shift *= -1

# Offset I1
tform = SimilarityTransform(translation=shift)
I1_reg = warp(np.float64(I1), tform)
I1_reg = np.float32(I1_reg)

# Calculate difference
I_diff = I0 - I1_reg

# Calculate the rotation axis
rot_axis = (np.shape(I0)[1] / 2) - shift[0]


# %% Output results
print('The offset is (delx, dely) = (%.2f, %.2f)' % (shift[0], shift[1]))
print('The rotation axis is at %.2f' % (rot_axis))

# Plot
plt.figure(1)
plt.clf()
plt.subplot(131)
plt.imshow(I0, cmap='gray')
plt.title('Original Image, $I_0$')
plt.subplot(132)
plt.imshow(I1_reg, cmap='gray')
plt.title('Registered Image, $I_{1,reg}$')
plt.subplot(133)
plt.imshow(I_diff, cmap='gray')
plt.title('Difference Image, $I_0 - I_{1,reg}$')
