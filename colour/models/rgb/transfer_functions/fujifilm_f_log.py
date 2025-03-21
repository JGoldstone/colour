"""
Fujifilm F-Log Log Encoding
===========================

Define the *Fujifilm F-Log* log encoding:

-   :func:`colour.models.log_encoding_FLog`
-   :func:`colour.models.log_decoding_FLog`
-   :func:`colour.models.log_encoding_FLog2`
-   :func:`colour.models.log_decoding_FLog2`

References
----------
-   :cite:`Fujifilm2022` : Fujifilm. (2022). F-Log Data Sheet Ver.1.1 (pp.
    1-4). https://dl.fujifilm-x.com/support/lut/F-Log_DataSheet_E_Ver.1.1.pdf
-   :cite:`Fujifilm2022a` : Fujifilm. (2022). F-Log2 Data Sheet Ver.1.0 (pp.
    1-4). https://dl.fujifilm-x.com/support/lut/F-Log2_DataSheet_E_Ver.1.0.pdf
"""

from __future__ import annotations

import typing

import numpy as np

if typing.TYPE_CHECKING:
    from colour.hints import ArrayLike, NDArrayFloat

from colour.models.rgb.transfer_functions import full_to_legal, legal_to_full
from colour.utilities import Structure, as_float, from_range_1, to_domain_1

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "CONSTANTS_FLOG",
    "CONSTANTS_FLOG2",
    "log_encoding_FLog",
    "log_decoding_FLog",
    "log_encoding_FLog2",
    "log_decoding_FLog2",
]

CONSTANTS_FLOG: Structure = Structure(
    cut1=0.00089,
    cut2=0.100537775223865,
    a=0.555556,
    b=0.009468,
    c=0.344676,
    d=0.790453,
    e=8.735631,
    f=0.092864,
)
"""*Fujifilm F-Log* constants."""

CONSTANTS_FLOG2: Structure = Structure(
    cut1=0.000889,
    cut2=0.100686685370811,
    a=5.555556,
    b=0.064829,
    c=0.245281,
    d=0.384316,
    e=8.799461,
    f=0.092864,
)
"""*Fujifilm F-Log2* colourspace constants."""


def log_encoding_FLog(
    in_r: ArrayLike,
    bit_depth: int = 10,
    out_normalised_code_value: bool = True,
    in_reflection: bool = True,
    constants: Structure = CONSTANTS_FLOG,
) -> NDArrayFloat:
    """
    Define the *Fujifilm F-Log* log encoding curve / opto-electronic transfer
    function.

    Parameters
    ----------
    in_r
        Linear reflection data :math`in`.
    bit_depth
        Bit-depth used for conversion.
    out_normalised_code_value
        Whether the non-linear *Fujifilm F-Log* data :math:`out` is encoded as
        normalised code values.
    in_reflection
        Whether the light level :math`in` to a camera is reflection.
    constants
        *Fujifilm F-Log* constants.

    Returns
    -------
    :class:`numpy.ndarray`
        Non-linear data :math:`out`.

    Notes
    -----
    +------------+-----------------------+---------------+
    | **Domain** | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``in_r``   | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    +------------+-----------------------+---------------+
    | **Range**  | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``out_r``  | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    References
    ----------
    :cite:`Fujifilm2022`

    Examples
    --------
    >>> log_encoding_FLog(0.18)  # doctest: +ELLIPSIS
    0.4593184...

    The values of *2-2. F-Log Code Value* table in :cite:`Fujifilm2022` are
    obtained as follows:

    >>> x = np.array([0, 18, 90]) / 100
    >>> np.around(log_encoding_FLog(x, 10, False) * 100, 1)
    array([  3.5,  46.3,  73.2])
    >>> np.around(log_encoding_FLog(x) * (2**10 - 1)).astype(np.int_)
    array([ 95, 470, 705])
    """

    in_r = to_domain_1(in_r)

    if not in_reflection:
        in_r = in_r * 0.9

    cut1 = constants.cut1
    a = constants.a
    b = constants.b
    c = constants.c
    d = constants.d
    e = constants.e
    f = constants.f

    out_r = np.where(
        in_r < cut1,
        e * in_r + f,
        c * np.log10(a * in_r + b) + d,
    )

    out_r_cv = out_r if out_normalised_code_value else legal_to_full(out_r, bit_depth)

    return as_float(from_range_1(out_r_cv))


def log_decoding_FLog(
    out_r: ArrayLike,
    bit_depth: int = 10,
    in_normalised_code_value: bool = True,
    out_reflection: bool = True,
    constants: Structure = CONSTANTS_FLOG,
) -> NDArrayFloat:
    """
    Define the *Fujifilm F-Log* log decoding curve / electro-optical transfer
    function.

    Parameters
    ----------
    out_r
        Non-linear data :math:`out`.
    bit_depth
        Bit-depth used for conversion.
    in_normalised_code_value
        Whether the non-linear *Fujifilm F-Log* data :math:`out` is encoded as
        normalised code values.
    out_reflection
        Whether the light level :math`in` to a camera is reflection.
    constants
        *Fujifilm F-Log* constants.

    Returns
    -------
    :class:`numpy.ndarray`
        Linear reflection data :math`in`.

    Notes
    -----
    +------------+-----------------------+---------------+
    | **Domain** | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``out_r``  | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    +------------+-----------------------+---------------+
    | **Range**  | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``in_r``   | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    References
    ----------
    :cite:`Fujifilm2022`

    Examples
    --------
    >>> log_decoding_FLog(0.45931845866162124)  # doctest: +ELLIPSIS
    0.1800000...
    """

    out_r = to_domain_1(out_r)

    out_r = out_r if in_normalised_code_value else full_to_legal(out_r, bit_depth)

    cut2 = constants.cut2
    a = constants.a
    b = constants.b
    c = constants.c
    d = constants.d
    e = constants.e
    f = constants.f

    in_r = np.where(
        out_r < cut2,
        (out_r - f) / e,
        (10 ** ((out_r - d) / c)) / a - b / a,
    )

    if not out_reflection:
        in_r = in_r / 0.9

    return as_float(from_range_1(in_r))


def log_encoding_FLog2(
    in_r: ArrayLike,
    bit_depth: int = 10,
    out_normalised_code_value: bool = True,
    in_reflection: bool = True,
    constants: Structure = CONSTANTS_FLOG2,
) -> NDArrayFloat:
    """
    Define the *Fujifilm F-Log2* log encoding curve / opto-electronic transfer
    function.

    Parameters
    ----------
    in_r
        Linear reflection data :math`in`.
    bit_depth
        Bit depth used for conversion.
    out_normalised_code_value
        Whether the non-linear *Fujifilm F-Log2* data :math:`out` is encoded as
        normalised code values.
    in_reflection
        Whether the light level :math`in` to a camera is reflection.
    constants
        *Fujifilm F-Log2* constants.

    Returns
    -------
    :class:`numpy.floating` or :class:`numpy.ndarray`
        Non-linear data :math:`out`.

    Notes
    -----
    +------------+-----------------------+---------------+
    | **Domain** | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``in_r``   | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    +------------+-----------------------+---------------+
    | **Range**  | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``out_r``  | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    References
    ----------
    :cite:`Fujifilm2022a`

    Examples
    --------
    >>> log_encoding_FLog2(0.18)  # doctest: +ELLIPSIS
    0.3910072...

    The values of *2-2. F-Log2 Code Value* table in :cite:`Fujifilm2022a` are
    obtained as follows:

    >>> x = np.array([0, 18, 90]) / 100
    >>> np.around(log_encoding_FLog2(x, 10, False) * 100, 1)
    array([  3.5,  38.4,  57.8])
    >>> np.around(log_encoding_FLog2(x) * (2**10 - 1)).astype(np.int_)
    array([ 95, 400, 570])
    """

    return log_encoding_FLog(
        in_r, bit_depth, out_normalised_code_value, in_reflection, constants
    )


def log_decoding_FLog2(
    out_r: ArrayLike,
    bit_depth: int = 10,
    in_normalised_code_value: bool = True,
    out_reflection: bool = True,
    constants: Structure = CONSTANTS_FLOG2,
) -> NDArrayFloat:
    """
    Define the *Fujifilm F-Log2* log decoding curve / electro-optical transfer
    function.

    Parameters
    ----------
    out_r
        Non-linear data :math:`out`.
    bit_depth
        Bit depth used for conversion.
    in_normalised_code_value
        Whether the non-linear *Fujifilm F-Log2* data :math:`out` is encoded as
        normalised code values.
    out_reflection
        Whether the light level :math`in` to a camera is reflection.
    constants
        *Fujifilm F-Log2* constants.

    Returns
    -------
    :class:`numpy.floating` or :class:`numpy.ndarray`
        Linear reflection data :math`in`.

    Notes
    -----
    +------------+-----------------------+---------------+
    | **Domain** | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``out_r``  | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    +------------+-----------------------+---------------+
    | **Range**  | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``in_r``   | [0, 1]                | [0, 1]        |
    +------------+-----------------------+---------------+

    References
    ----------
    :cite:`Fujifilm2022a`

    Examples
    --------
    >>> log_decoding_FLog2(0.39100724189123004)  # doctest: +ELLIPSIS
    0.1799999...
    """

    return log_decoding_FLog(
        out_r, bit_depth, in_normalised_code_value, out_reflection, constants
    )
