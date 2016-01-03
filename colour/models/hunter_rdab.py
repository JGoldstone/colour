#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hunter Rd,a,b Colour Scale
==========================

Defines the *Hunter Rd,a,b* colour scale transformations:

-   :func:`XYZ_to_Hunter_Rdab`

See Also
--------
`Hunter Rd,a,b Colour Scale IPython Notebook
<http://nbviewer.ipython.org/github/colour-science/colour-ipython/\
blob/master/notebooks/models/hunter_rdab.ipynb>`_

References
----------
.. [1]  HunterLab. (2012). Hunter Rd , a , b Color Scale –
        History and Application. Retrieved from
        https://hunterlabdotcom.files.wordpress.com/2012/07/\
an-1016-hunter-rd-a-b-color-scale-update-12-07-03.pdf
"""

from __future__ import division, unicode_literals

import numpy as np

from colour.colorimetry import HUNTERLAB_ILLUMINANTS
from colour.models import XYZ_to_K_ab_HunterLab1966
from colour.utilities import tsplit, tstack

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013 - 2015 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['XYZ_to_Hunter_Rdab']


def XYZ_to_Hunter_Rdab(
        XYZ,
        XYZ_n=HUNTERLAB_ILLUMINANTS.get(
            'CIE 1931 2 Degree Standard Observer').get('D50').XYZ_n,
        K_ab=HUNTERLAB_ILLUMINANTS.get(
            'CIE 1931 2 Degree Standard Observer').get('D50').K_ab):
    """
    Computes the *Hunter L,a,b* :math:`R_{d} ab` colour scale from given
    *CIE XYZ* and reference *illuminant* tristimulus values.

    Parameters
    ----------
    XYZ : array_like
        *CIE XYZ* tristimulus values.
    XYZ_n : array_like, optional
        Reference *illuminant* tristimulus values.
    K_ab : array_like, optional
        Reference *illuminant* chromaticity coefficients, if `K_ab` is set to
        `None` it will be computed using :func:`XYZ_to_K_ab_HunterLab1966`.

    Returns
    -------
    ndarray
        *Hunter L,a,b* :math:`R_{d} ab` colour scale array.

    Notes
    -----
    -   Input *CIE XYZ* and reference *illuminant* tristimulus values are in
        domain [0, 100].

    Examples
    --------
    >>> XYZ = np.array([0.07049534, 0.10080000, 0.09558313]) * 100
    >>> D50 = HUNTERLAB_ILLUMINANTS.get(
    ...     'CIE 1931 2 Degree Standard Observer').get('D50')
    >>> XYZ_to_Hunter_Rdab(
    ...     XYZ,
    ...     D50.XYZ_n,
    ...     D50.K_ab)   # doctest: +ELLIPSIS
    array([ 10.08      , -18.6765376...,  -3.4432992...])
    """

    X, Y, Z = tsplit(XYZ)
    X_n, Y_n, Z_n = tsplit(XYZ_n)
    K_a, K_b = (tsplit(XYZ_to_K_ab_HunterLab1966(XYZ_n))
                if K_ab is None else
                tsplit(K_ab))

    f = 0.51 * ((21 + 0.2 * Y) / (1 + 0.2 * Y))
    Y_Yn = Y / Y_n

    R_d = Y
    a_Rd = K_a * f * (X / X_n - Y_Yn)
    b_Rd = K_b * f * (Y_Yn - Z / Z_n)

    R_d_ab = tstack((R_d, a_Rd, b_Rd))

    return R_d_ab
