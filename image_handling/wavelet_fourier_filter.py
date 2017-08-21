# -*- coding: utf-8 -*-
"""
Functions required to perform a Wavelet-Fourier filter on a sinogram

Written by: Andy Kiss
Started: 2017-02-15
Last modified: 2017-02-15

"""

import numpy as np
from numpy import matlib
from scipy import fftpack
import pywt


def wf_filter(sino, N_levels=0, waveletName='sym16', sigma=2.0,
              pad=10, forceZero=True):
    """    Wavelet-Fourier Ring Removal Filter

    This function will filter the image (or sinogram) using a discrete wavelet
    transform and a Fourier transform. The original reference can be found at:

    Parameters
    ----------
    sino -- 2D NumPy array
        the sinogram to be filtered. Each row should represent a different
        projection
    N_levels -- integer (default = 0)
        the number of levels to filter
    waveletName -- string
        the discrete wavelet transform to use
    sigma -- float (default = 2.0)
        the amount of dampening in Fourier space
    pad -- int (default = 10)
        pad the sinogram with (pad%) zeros
    forceZero -- boolean (default = True)
        force the filtered sinogram to have all positive numbers

    Returns
    -------
    sino_f = 2D NumPy array
        the filtered sinogram

    """

    # Check input parameters
    # Check N_levels size
    (dx, dy) = sino.shape
    N_max = np.max((dx, dy))
    N_levels_max = np.int(np.ceil(np.log2(N_max)))
    if (N_levels == 0):
        N_levels = N_levels_max
    if (N_levels > N_levels_max):
        print('Warning: Maximum number of levels is %d.' % (N_levels_max))
        N_levels = N_levels_max

    # Check that waveletName is in the wavelist
    if (waveletName not in pywt.wavelist()):
        print('Error: waveletName not found in wavelist.')
        return

    # Check for positive sigma
    if (sigma <= 0):
        print('Error: Sigma must be positive.')
        return

    # Add padding
    xshift = 0
    if (pad != 0):
        nx = dx + dx // pad
        xshift = (nx - dx) // 2
        sino_tmp = np.zeros((nx, dy), dtype=np.float32)
        sino_tmp[xshift:dx+xshift] = sino[:]
        sino = sino_tmp
        del sino_tmp

    # Wavelet decomposition
    Ch = []
    Cv = []
    Cd = []
    for i in range(N_levels):
        (sino, (Ch_tmp, Cv_tmp, Cd_tmp)) = pywt.dwt2(sino, waveletName)
        Ch.append(Ch_tmp)
        Cv.append(Cv_tmp)
        Cd.append(Cd_tmp)
    del Ch_tmp, Cv_tmp, Cd_tmp

    # Fourier transform of horizontal frequency bands
    for i in range(N_levels):
        # FFT
        fCv = fftpack.fftshift(fftpack.fft(Cv[i], axis=0))
        (my, mx) = fCv.shape

        # Dampening of verticle stripes
        damp = 1 - np.exp(-(np.arange(-np.floor(my/2.0),
                                      -np.floor(my/2.0) + my,
                                      step=1)**2) / (2 * sigma**2))
        fCv = fCv * np.transpose(matlib.repmat(damp, mx, 1))

        # Inverse FFT
        Cv[i] = np.real(fftpack.ifft(fftpack.ifftshift(fCv), axis=0))

    # Wavelet reconstruction
    sino_filtered = sino
    for i in range(N_levels)[::-1]:
        sino_filtered = sino_filtered[0:Ch[i].shape[0], 0:Ch[i].shape[1]]
        sino_filtered = pywt.idwt2((sino_filtered, (Ch[i], Cv[i], Cd[i])),
                                   waveletName)
    sino_tmp = sino_filtered[xshift:dx+xshift]
    sino_filtered = sino_tmp
    del sino_tmp

    # Remove negative numbers
    if (forceZero):
        sino_filtered[sino_filtered < 0] = 0

    # Return
    return sino_filtered
