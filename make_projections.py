# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 22:39:41 2017

@author: Andy
"""


import os
import numpy as np
import txm_image
import image_handling


# %% User needs to set these parameters
# fn_scanlog = r'20170724_103450_LENS_1_299_02.log'
# path = r'C:\Users\andykiss\Documents\tmp_work_dir\CAAM\2017Jul\APC\\'

fn_scanlog = '20170723_110810_ATI_powder.log'
path = r'C:\Users\andykiss\Documents\tmp_work_dir\CAAM\2017Jul'


# Despeckling images
flag_despeckle = True
DS_delta = 500
DS_rad = 3

# Bin images
flag_bin = False
B = 2  # Amount to bin (ex. B = 2 --> 2x2 binning)

# Exposure times
t_ref = 500  # [ms] reference exposure time
t_proj = 500  # [ms] projection exposure time

# True -- Average any images together
# False -- Use median averaging
flag_average = True

# Left-right mosaic so that the center of sample rotation is at the edge of the
# field of view so 180 deg is equivalent to 0 flipped and translated
flag_360_mosaic = False
new_xy = (500., 0.)

# True -- Load everything into memory, and then write to file. Faster.
# False -- Load files and write one by one. Slower.
flag_big_memory = True

# True -- Clear some of the big memory items (image stack, ff, df)
# False -- Leave big memory items loaded in memory
flag_clear_big = True

# True -- Make bim files
# False -- Make tiff files
flag_bim = True


# %% Load scanlog information
if (path[-1] != '\\' and path[-1] != '/'):
    path += '/'

LOG = txm_image.microCT_scanlog.read_log(path+fn_scanlog)

# Set folder names
path_df = LOG.sample_name + '-df_1\\'
path_ref1 = LOG.sample_name + '-ref_1\\'
path_ref2 = LOG.sample_name + '-ref_2\\'
path_proj = LOG.sample_name + '_1\\'
# path_proj = LOG.sample_name + '-proj\\'
path_process = LOG.sample_name + '-processing\\'


# %% Process the dark and flat-fields
# Change to the master directory
os.chdir(path)

# Make a processing directory if it does not exist
try:
    os.stat(path_process)
except:
    os.mkdir(path_process)

# Check for dark field images
if (LOG.flag_df is True):
    print('Processing dark field images...', end='')
    # Move into the dark field directory
    os.chdir(path_df)

    # Get the list of files and filter for *.tif
    fn = os.listdir()
    ls_rm = []
    for i in range(len(fn)):
        if (not fn[i].endswith('.tif')):
            ls_rm.append(fn[i])
    for i in range(len(ls_rm)):
        fn.remove(ls_rm[i])

    # Read in the dark field files and average them
    df, _ = txm_image.read_file(fn[0], verbose=False)
    if (flag_average):
        df_avg = image_handling.average_image_stack(df)
    else:
        df_avg = image_handling.median_image_stack(df)

    # Bin the image
    if (flag_bin):
        df_avg = image_handling.bin_image(df_avg, B=B, method='average')

    # Move to the process directory and write the file
    os.chdir('..\\'+path_process)
    if (flag_bim):
        txm_image.write_file('df_avg.bim', df_avg, verbose=False)
    else:
        txm_image.write_file('df_avg.tif', df_avg, verbose=False)

    # Garbage clean up
    df = df_avg
    del df_avg

    # Return to the master directory
    os.chdir('..')
    print('done')
else:
    df = np.zeros((LOG.V_RES, LOG.H_RES), dtype=np.float32)

# Return to the root directory
os.chdir(path)

# Check for flat-field images
if (LOG.flag_ref is True):
    print('Processing flat-field images...', end='')
    # Move into the dark field directory
    os.chdir(path_ref1)

    # Get the list of files and filter for *.tif
    fn = os.listdir()
    ls_rm = []
    for i in range(len(fn)):
        if (not fn[i].endswith('.tif')):
            ls_rm.append(fn[i])
    for i in range(len(ls_rm)):
        fn.remove(ls_rm[i])

    # Read in the dark field files
    ff1, _ = txm_image.read_file(fn[0], verbose=False)

    # Despeckle images
    if (flag_despeckle):
        for i in range(ff1.shape[0]):
            ff1[i, :, :] = image_handling.remove_outliers_scipy(ff1[i, :, :],
                                                                delta=DS_delta,
                                                                radius=DS_rad)

    # Average them
    if (flag_average):
        ff1_avg = image_handling.average_image_stack(ff1)
    else:
        ff1_avg = image_handling.median_image_stack(ff1)

    # Bin the images
    if (flag_bin):
        ff1_avg = image_handling.bin_image(ff1_avg, B=B, method='average')

    # Scale the references
    ff1_avg = (t_proj / t_ref) * ff1_avg

    # Move to the process directory and write the file
    os.chdir('..\\'+path_process)
    if (flag_bim):
        txm_image.write_file('ff1_avg.bim', ff1_avg, verbose=False)
    else:
        txm_image.write_file('ff1_avg.tif', ff1_avg, verbose=False)

    # Garbage clean up
    ff1 = ff1_avg
    del ff1_avg

    # Return to the master directory
    os.chdir('..')

    print('done')
else:
    ff1 = np.ones((LOG.V_RES, LOG.H_RES), dtype=np.float32)

# Check for second flat-field image
ls_dir = os.listdir(path)
try:
    ind_ff2 = ls_dir.index(path_ref2)
except:
    ind_ff = -1

if (ind_ff < 0):
    print('Processing flat-field images...', end='')
    # Move into the dark field directory
    os.chdir(path_ref2)

    # Get the list of files and filter for *.tif
    fn = os.listdir()
    ls_rm = []
    for i in range(len(fn)):
        if (not fn[i].endswith('.tif')):
            ls_rm.append(fn[i])
    for i in range(len(ls_rm)):
        fn.remove(ls_rm[i])

    # Read in the FLAT field files
    ff2, _ = txm_image.read_file(fn[0], verbose=False)

    # Despeckle images
    if (flag_despeckle):
        for i in range(ff2.shape[0]):
            ff2[i, :, :] = image_handling.remove_outliers_scipy(ff2[i, :, :],
                                                                delta=DS_delta,
                                                                radius=DS_rad)

    # And average them
    if (flag_average):
        ff2_avg = image_handling.average_image_stack(ff2)
    else:
        ff2_avg = image_handling.median_image_stack(ff2)

    # Bin the images
    if (flag_bin):
        ff2_avg = image_handling.bin_image(ff2_avg, B=B, method='average')

    # Scale the references
    ff2_avg = (t_proj / t_ref) * ff2_avg

    # Move to the process directory and write the file
    os.chdir('..\\'+path_process)
    if (flag_bim):
        txm_image.write_file('ff2_avg.bim', ff2_avg, verbose=False)
    else:
        txm_image.write_file('ff2_avg.tif', ff2_avg, verbose=False)

    # Garbage clean up
    ff2 = ff2_avg
    del ff2_avg

    # Return to the master directory
    os.chdir('..')

    print('done')
else:
    ff2 = ff1


# %% Start processing projections

# Find all the Tiff projection files
ls_dir = os.listdir(path + path_proj)
ls_dir.sort()
N = len(ls_dir)
ls_rm = []
for i in range(N):
    # Find stuff to remove
    if (not ls_dir[i].endswith('.tif')):
        ls_rm.append(ls_dir[i])
# Remove them
for i in range(len(ls_rm)):
    ls_dir.remove(ls_rm[i])
N = len(ls_dir)
print('\nFound %d files.' % (N))

# Process data
if (flag_big_memory is True):
    # Load all the projection Tiff files
    print('Loading projection images...', end='')
    img, _ = txm_image.read_file(path + path_proj + ls_dir[0], verbose=False)
    if (N > 1 and img.ndim == 2):
        img_tmp = np.zeros((1, img.shape[0], img.shape[1]), dtype=np.float32)
        img_tmp[0, :, :] = img
        img = img_tmp
        del img_tmp
    # img_tmp, _ = txm_image.read_file(path + path_proj + ls_dir[0], verbose=False)
    # img = np.zeros((1, img_tmp.shape[0], img_tmp.shape[1]), dtype=np.float32)
    # img[0, :, :] = img_tmp
    if (img.shape[0] != (LOG.num_proj * LOG.num_mos * LOG.num_exp)):
        if (N > 1):
            # tmp_img = np.zeros((1, img_tmp.shape[0], img_tmp.shape[1]), dtype=np.float32)
            for i in np.arange(1, N):
                tmp_img, _ = txm_image.read_file(path + path_proj + ls_dir[i],
                                                 verbose=False)
                img = np.append(img, tmp_img, axis=0)
    print('done')
    # N_proj = np.size(img)[0]
    N_proj = img.shape[0]
    print('Found %d images.' % (N_proj))

    # Despeckle the images
    if (flag_despeckle):
        print('Removing outliers...      ', end='')
        for i in range(N_proj):
            print('\b\b\b\b\b\b(%3d%%)' % (100 * i // N_proj), end='')
            img[i, :, :] = image_handling.remove_outliers_scipy(img[i, :, :],
                                                                delta=DS_delta,
                                                                radius=DS_rad)
        print('\b\b\b\b\b\bdone  ')

    # Bin the images
    if (flag_bin):
        img = image_handling.bin_image(img, B=B, method='average')

    # Reference correct the images
    # Needs to be split between first half and second half
    print('Applying reference correction...      ', end='')
    Nh = N_proj // 2
    # Need to implement this for stacks
    # img[0:Nh, :, :] = image_handling.external_reference(img[0:Nh, :, :],
    #                                                     ff1, df)
    # img[Nh:N, :, :] = image_handling.external_reference(img[Nh:N, :, :],
    #                                                     ff2, df)
    for i in range(Nh):
        print('\b\b\b\b\b\b(%3d%%)' % (100 * i // N_proj), end='')
        img[i, :, :] = image_handling.external_reference(img[i, :, :], ff1, df)
        # print('proj %04i' % (i))
    for i in np.arange(Nh, N_proj):
        print('\b\b\b\b\b\b(%3d%%)' % (100 * i // N_proj), end='')
        img[i, :, :] = image_handling.external_reference(img[i, :, :], ff2, df)
        # print('proj %04i' % (i))
    print('\b\b\b\b\b\bdone  ')

    # Average multiple exposures before saving files
    if (LOG.num_exp > 1):
        N_avg = N_proj // LOG.num_exp
        img_avg = np.zeros((N_avg, LOG.V_RES, LOG.H_RES), dtype=np.float32)
        for i in range(N_avg):
            i_start = i * LOG.num_exp
            i_end = i_start + LOG.num_exp
            I = img[i_start:i_end, :, :]
            if (flag_average):
                img_avg[i, :, :] = image_handling.average_image_stack(I)
            else:
                img_avg[i, :, :] = image_handling.median_image_stack(I)
        img = img_avg
        del img_avg, I

    # Make the meta data
    # Write the individual bim files
    os.chdir(path + path_process)
    print('Saving files...', end='')
    txm_image.add_metadata_to_img(LOG, img, outdir='bim\\', flag_Nexp=1, verbose=True)
    print('done')
else:
    # Find total number of images
    N_total = 0
    for i in range(N):
        fn = path+path_proj+ls_dir[i]
        N_total += txm_image.formats.tiff.tiff_stack_size(fn)
    Nh = N_total // 2
    print('\nFound %d images.' % (N_total))

    # Create the metadata template
    meta_tmp = txm_image.formats.bim.create_metadata_from_scanlog(LOG)
    if (flag_bin):
        meta_tmp.pixelsize = B * meta_tmp.pixelsize

    # Start looping through stacks
    N_count = 0
    for i in range(N):
        fn = path+path_proj+ls_dir[i]
        N_img = txm_image.formats.tiff.tiff_stack_size(fn)
        for ii in range(N_img):
            # Output to screen
            print('Processing image (%06d/%06d)...' % (N_count+1, N_total),
                  end='')
            # Load the image
            img = txm_image.formats.tiff.read_tiff(fn, ind=ii)

            # Despeckle the image
            if (flag_despeckle):
                img = image_handling.remove_outliers_scipy(img, delta=DS_delta,
                                                           radius=DS_rad)
            # Bin the images
            if (flag_bin):
                img = image_handling.bin_image(img, B=B, method='average')

            # Reference correct
            if (ii < Nh):
                img = image_handling.external_reference(img, ff1, df)
            else:
                img = image_handling.external_reference(img, ff2, df)

            # Modify metadata for the image
            meta_tmp.height, meta_tmp.width = np.shape(img)
            th = LOG.th_start + np.floor(ii / np.double(LOG.num_exp) / np.double(LOG.num_mos)) * LOG.th_step
            meta_tmp.angles = np.deg2rad(th)
            meta_tmp.MotPos[3] = th

            # Convert postions to microns
            meta_tmp.MotPos[0] = LOG.X[ii % LOG.num_mos] * -1000.
            meta_tmp.MotPos[1] = LOG.Y[ii % LOG.num_mos] * 1000.

            fn_out = 'proj_%06d.bim' % (N_count)

            # Check for 360 mosaic
            if (flag_360_mosaic):
                fn_out = 'proj_%09.4f_a.bim' % (th)
                if (th >= 180):
                    th = np.mod(th, 180)
                    meta_tmp.angles = np.deg2rad(th)
                    meta_tmp.MotPos[3] = th
                    meta_tmp.MotPos[0] = new_xy[0]
                    meta_tmp.MotPos[1] = new_xy[1]
                    fn_out = 'proj%09.4f_b.bim' % (th)
                if (th >= 360):
                    continue
            # Write
            os.chdir(path + path_process)
            txm_image.write_file(fn_out, img, meta_tmp, verbose=False)
            N_count += 1
            print('done')


# %% Clear big memory items
if (flag_clear_big):
    del df
    del ff1, ff2
    del img


# %% Next step
os.chdir(path)
print('\nDone.\n')
