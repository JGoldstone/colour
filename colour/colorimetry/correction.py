"""
Spectral Bandpass Dependence Correction
=======================================

Define the objects to perform spectral bandpass dependence correction.

The following correction methods are available:

-   :func:`colour.colorimetry.bandpass_correction_Stearns1988`:
    *Stearns and Stearns (1988)* spectral bandpass dependence correction
    method.
-   :attr:`colour.BANDPASS_CORRECTION_METHODS`: Supported spectral bandpass
    dependence correction methods.
-   :func:`colour.bandpass_correction`: Spectral bandpass dependence
    correction using given method.

References
----------
-   :cite:`Stearns1988a` : Stearns, E. I., & Stearns, R. E. (1988). An example
    of a method for correcting radiance data for Bandpass error. Color Research
    & Application, 13(4), 257-259. doi:10.1002/col.5080130410
-   :cite:`Westland2012f` : Westland, S., Ripamonti, C., & Cheung, V. (2012).
    Correction for Spectral Bandpass. In Computational Colour Science Using
    MATLAB (2nd ed., p. 38). ISBN:978-0-470-66569-5
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from colour.colorimetry import SpectralDistribution
    from colour.hints import Literal

from colour.utilities import CanonicalMapping, validate_method

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "bandpass_correction_Stearns1988",
    "BANDPASS_CORRECTION_METHODS",
    "bandpass_correction",
]

CONSTANT_ALPHA_STEARNS: float = 0.083


def bandpass_correction_Stearns1988(
    sd: SpectralDistribution,
) -> SpectralDistribution:
    """
    Implement spectral bandpass dependence correction on given spectral
    distribution using *Stearns and Stearns (1988)* method.

    Parameters
    ----------
    sd
        Spectral distribution.

    Returns
    -------
    :class:`colour.SpectralDistribution`
        Spectral bandpass dependence corrected spectral distribution.

    References
    ----------
    :cite:`Stearns1988a`, :cite:`Westland2012f`

    Examples
    --------
    >>> from colour import SpectralDistribution
    >>> from colour.utilities import numpy_print_options
    >>> data = {
    ...     500: 0.0651,
    ...     520: 0.0705,
    ...     540: 0.0772,
    ...     560: 0.0870,
    ...     580: 0.1128,
    ...     600: 0.1360,
    ... }
    >>> with numpy_print_options(suppress=True):
    ...     bandpass_correction_Stearns1988(SpectralDistribution(data))
    ... # doctest: +ELLIPSIS
    SpectralDistribution([[ 500.        ,    0.0646518...],
                          [ 520.        ,    0.0704293...],
                          [ 540.        ,    0.0769485...],
                          [ 560.        ,    0.0856928...],
                          [ 580.        ,    0.1129644...],
                          [ 600.        ,    0.1379256...]],
                         SpragueInterpolator,
                         {},
                         Extrapolator,
                         {'method': 'Constant', 'left': None, 'right': None})
    """

    A_S = CONSTANT_ALPHA_STEARNS
    values = sd.values

    values[0] = (1 + A_S) * values[0] - A_S * values[1]
    values[-1] = (1 + A_S) * values[-1] - A_S * values[-2]
    for i in range(1, len(values) - 1):
        values[i] = (
            -A_S * values[i - 1] + (1 + 2 * A_S) * values[i] - A_S * values[i + 1]
        )

    sd.values = values

    return sd


BANDPASS_CORRECTION_METHODS: CanonicalMapping = CanonicalMapping(
    {"Stearns 1988": bandpass_correction_Stearns1988}
)
BANDPASS_CORRECTION_METHODS.__doc__ = """
Supported spectral bandpass dependence correction methods.
"""


def bandpass_correction(
    sd: SpectralDistribution,
    method: Literal["Stearns 1988"] | str = "Stearns 1988",
) -> SpectralDistribution:
    """
    Implement spectral bandpass dependence correction on given spectral
    distribution using given method.

    Parameters
    ----------
    sd
        Spectral distribution.
    method
        Correction method.

    Returns
    -------
    :class:`colour.SpectralDistribution`
        Spectral bandpass dependence corrected spectral distribution.

    References
    ----------
    :cite:`Stearns1988a`, :cite:`Westland2012f`

    Examples
    --------
    >>> from colour import SpectralDistribution
    >>> from colour.utilities import numpy_print_options
    >>> data = {
    ...     500: 0.0651,
    ...     520: 0.0705,
    ...     540: 0.0772,
    ...     560: 0.0870,
    ...     580: 0.1128,
    ...     600: 0.1360,
    ... }
    >>> with numpy_print_options(suppress=True):
    ...     bandpass_correction(SpectralDistribution(data))
    ... # doctest: +ELLIPSIS
    SpectralDistribution([[ 500.        ,    0.0646518...],
                          [ 520.        ,    0.0704293...],
                          [ 540.        ,    0.0769485...],
                          [ 560.        ,    0.0856928...],
                          [ 580.        ,    0.1129644...],
                          [ 600.        ,    0.1379256...]],
                         SpragueInterpolator,
                         {},
                         Extrapolator,
                         {'method': 'Constant', 'left': None, 'right': None})
    """

    method = validate_method(method, tuple(BANDPASS_CORRECTION_METHODS))

    return BANDPASS_CORRECTION_METHODS[method](sd)
