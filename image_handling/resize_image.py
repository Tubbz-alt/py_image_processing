# -*- coding: utf-8 -*-

"""
Bin the image.

Written by: Andy Kiss
Started: 2017-01-25
Last modified: 2017-01-25

"""


# Import modules
import numpy as np
from skimage.transform import resize


def bin_image(img, B=1, method='average'):
    """
    Bin the image in the horizontal and verticle direction

    Parameters
    ----------
    img -- NumPy array
        an array representing the image
    B -- int
        an integer representing the amount of binning
    method -- string (optional)
        average -- this will average the pixels when resizing
        sum -- this will sum the pixels when resizing

    Returns
    -------
    proj -- NumPy array
        returns the binned image
    """

    # Get the starting image size
    if (img.ndim == 2):
        N = 1
        (H, V) = img.shape
    elif (img.ndim == 3):
        (N, H, V) = img.shape
    else:
        print('Bin image ERROR! image is not the right size')
        return

    # Get the new size
    (H_new, V_new) = (H // B, V // B)

    # Resize the image
    if (method == 'average'):
        """
        if (N == 1):
            I = resize(img, (H_new, V_new))
        else:
            I = np.zeros((N, H_new, V_new), dtype=np.float32)
            for i in range(N):
                I[i, :, :] = resize(img[i, :, :], (H_new, V_new))
        """
        if (N == 1):
            I = np.zeros((H_new, V_new), dtype=np.float32)
            for i in range(H_new):
                for j in range(V_new):
                    x = i * B
                    y = j * B
                    I[i, j] = np.mean(img[x:x+B, y:y+B])
        else:
            I = np.zeros((N, H_new, V_new), dtype=np.float32)
            for ii in range(N):
                for i in range(H_new):
                    for j in range(V_new):
                        x = i * B
                        y = j * B
                        I[ii, i, j] = np.mean(img[ii, x:x+B, y:y+B])
    elif (method == 'sum'):
        if (N == 1):
            I = np.zeros((H_new, V_new), dtype=np.float32)
            for i in range(H_new):
                for j in range(V_new):
                    x = i * B
                    y = j * B
                    I[i, j] = np.sum(img[x:x+B, y:y+B])
        else:
            I = np.zeros((N, H_new, V_new), dtype=np.float32)
            for ii in range(N):
                for i in range(H_new):
                    for j in range(V_new):
                        x = i * B
                        y = j * B
                        I[ii, i, j] = np.sum(img[ii, x:x+B, y:y+B])
    else:
        print('Bin Image ERROR! method not found.')
        return

    # Return the new image
    return I


def bin_image_stack(img, bin_size=(1, 1), method='average'):
    """
    Bin the image in the horizontal and verticle direction

    Parameters
    ----------
    img -- NumPy array
        an array representing the image or an image stack
    bin_size -- tuple of integers
        an integer representing the amount of binning in the verticle and
        horizontal directions
    method -- string (optional)
        average -- this will average the pixels when resizing
        sum -- this will sum the pixels when resizing

    Returns
    -------
    proj -- NumPy array
        returns the binned image(s)
    """

    if (bin_size == (1, 1)):
        return img

    if (img.ndim != 3):
        img = img[np.newaxis]

    (n, m) = bin_size
    ims = img[:, :img.shape[1] - np.mod(img.shape[1], n),
                 :img.shape[2] - np.mod(img.shape[2], m)]

    if (method == 'average'):
        ims = ims.reshape(ims.shape[0], ims.shape[1]//n, n,
                                        ims.shape[2]//m, m).mean(4).mean(2)
    elif (method == 'sum'):
        ims = ims.reshape(ims.shape[0], ims.shape[1]//n, n,
                                        ims.shape[2]//m, m).sum(4).sum(2)
    else:
        print('Method \"' + method + '\" not found.')

    return ims.squeeze()
