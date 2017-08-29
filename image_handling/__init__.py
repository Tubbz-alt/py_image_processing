# -*- coding: utf-8 -*-

"""
Image Handling

This collection of functions will perform operations on NumPy arrays
(or images).

Written by: Andy Kiss
Started: 2017-01-24
Last modified: 2017-02-15

"""

__all__ = ['remove_outliers', 'average_image', 'reference_correction']
__version__ = '0.1'
__author__ = 'Andy Kiss'

from image_handling.remove_outliers import remove_outliers_scipy
from image_handling.average_image import average_image_stack
from image_handling.average_image import median_image_stack
from image_handling.reference_correction import external_reference
from image_handling.wavelet_fourier_filter import wf_filter
from image_handling.resize_image import bin_image
from image_handling.resize_image import bin_image_stack