# -*- coding: utf-8 -*-
"""
Tomographic Reconstruction Functions

Written by: Andy Kiss
Created: 2017-02-15
Last modified: 2017-02-15

"""


import numpy as np
import astra


def astra_recon(sino, th, algorithm='FBP', num_iter=10, px=1.0,
                flag_matlab_crop=True):
    """
    ASTRA Reconstruction

    The function will reconstruct the sinogram using the ASTRA-Toolbox

    Parameters
    ----------
    sino -- 2D NumPy array
        a sinogram with each row representing a different angle
    th -- 1D NumPy array
        the angle (in degrees) corresponding to each row in the sinogram
    algorithm -- string
        the algorithm to use for the reconstruction
    num_iter -- integer (default=10)
        the number of iterations to perform for iterative techniques
    px -- float
        the pixel size
    flag_matlab_crop -- boolean (default=True)
        crop the image similar to MATLAB's reconstruction code

    Returns
    -------
    recon -- 2D NumPy array
        the reconstructed slice

    """

    # Check the algorithm

    # Check CUDA compatibility
    if (algorithm.endswith('_CUDA')):
        if (not astra.astra.use_cuda()):
            print('\nCUDA is not enabled on this system.')
            print('Please check the algorithm.')
            raise SystemExit
    else:
        if (astra.astra.use_cuda()):
            print('\nThe algorithm may run faster using the GPU.')
            print('Consider running %s_CUDA instead.' % (algorithm))

    # Convert the angles to radians
    th = np.deg2rad(th)
    (num_angles, num_col) = np.shape(sino)

    # Create the geometries
    proj_geom = astra.create_proj_geom('parallel', px, num_col, th)
    vol_geom = astra.create_vol_geom(num_col, num_col)
    if (not algorithm.endswith('CUDA')):
        proj_id = astra.create_projector('strip', proj_geom, vol_geom)

    # Move the loaded sinogram into ASTRA memory
    sino_id = astra.data2d.create('-sino', proj_geom, sino)

    # Perform the reconstruction
    recon_id = astra.data2d.create('-vol', vol_geom, 0)
    cfg = astra.astra_dict(algorithm)
    cfg['ProjectionDataId'] = sino_id
    cfg['ReconstructionDataId'] = recon_id
    if (not algorithm.endswith('CUDA')):
        cfg['ProjectorId'] = proj_id
    cfg['MinConstraint'] = 0
    alg_id = astra.algorithm.create(cfg)

    if (algorithm == 'FBP' or algorithm == 'FBP_CUDA'):
        astra.algorithm.run(alg_id)
    else:
        astra.algorithm.run(alg_id, iterations=num_iter)

    # Get and crop the reconstructed slice
    recon = astra.data2d.get(recon_id)
    if (flag_matlab_crop):
        ML_recon_size = 2.0 * np.floor(num_col / (2.0 * np.sqrt(2)))
        minX = np.int(np.ceil(0.5 * (num_col - ML_recon_size)))
        maxX = np.int(num_col - minX + 1)
        minY = minX
        maxY = maxX
        recon = recon[minX:maxX, minY:maxY]

    # Garbage clean up
    astra.data2d.delete((sino_id, recon_id))
    if (not algorithm.endswith('CUDA')):
        astra.data2d.delete((proj_id))
    astra.algorithm.delete(alg_id)

    # Return the reconstructed slice
    return recon
