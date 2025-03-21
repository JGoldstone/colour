"""
:math:`\\Delta E^*_{ab}` - Delta E Colour Difference
====================================================

Define the :math:`\\Delta E^*_{ab}` colour difference computation objects:

The following attributes and methods are available:

-   :attr:`colour.difference.JND_CIE1976`
-   :func:`colour.difference.delta_E_CIE1976`
-   :func:`colour.difference.delta_E_CIE1994`
-   :func:`colour.difference.delta_E_CIE2000`
-   :func:`colour.difference.delta_E_CMC`
-   :func:`colour.difference.delta_E_ITP`
-   :func:`colour.difference.delta_E_HyAB`
-   :func:`colour.difference.delta_E_HyCH`

References
----------
-   :cite:`Abasi2020a` : Abasi, S., Amani Tehran, M., & Fairchild, M. D. (2020).
    Distance metrics for very large color differences. Color Research &
    Application, 45(2), 208-223. doi:10.1002/col.22451
-   :cite:`InternationalTelecommunicationUnion2019` : International
    Telecommunication Union. (2019). Recommendation ITU-R BT.2124-0 -
    Objective metric for the assessment of the potential visibility of colour
    differences in television (pp. 1-36).
    https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2124-0-201901-I!!PDF-E.pdf
-   :cite:`Lindbloom2003c` : Lindbloom, B. (2003). Delta E (CIE 1976).
    Retrieved February 24, 2014, from
    http://brucelindbloom.com/Eqn_DeltaE_CIE76.html
-   :cite:`Lindbloom2009f` : Lindbloom, B. (2009). Delta E (CMC). Retrieved
    February 24, 2014, from http://brucelindbloom.com/Eqn_DeltaE_CMC.html
-   :cite:`Lindbloom2011a` : Lindbloom, B. (2011). Delta E (CIE 1994).
    Retrieved February 24, 2014, from
    http://brucelindbloom.com/Eqn_DeltaE_CIE94.html
-   :cite:`Melgosa2013b` : Melgosa, M. (2013). CIE / ISO new standard:
    CIEDE2000. http://www.color.org/events/colorimetry/\
Melgosa_CIEDE2000_Workshop-July4.pdf
-   :cite:`Sharma2005b` : Sharma, G., Wu, W., & Dalal, E. N. (2005). The
    CIEDE2000 color-difference formula: Implementation notes, supplementary
    test data, and mathematical observations. Color Research & Application,
    30(1), 21-30. doi:10.1002/col.20070
-   :cite:`Mokrzycki2011` : Mokrzycki, W., & Tatol, M. (2011). Color difference
    Delta E - A survey. Machine Graphics and Vision, 20, 383-411.
"""

from __future__ import annotations

import typing
from dataclasses import astuple, dataclass, field

import numpy as np

from colour.algebra import euclidean_distance

if typing.TYPE_CHECKING:
    from colour.hints import ArrayLike, NDArrayFloat

from colour.utilities import (
    MixinDataclassArithmetic,
    as_float,
    to_domain_100,
    tsplit,
    zeros,
)
from colour.utilities.documentation import DocstringFloat, is_documentation_building

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "JND_CIE1976",
    "delta_E_CIE1976",
    "delta_E_CIE1994",
    "intermediate_attributes_CIE2000",
    "delta_E_CIE2000",
    "delta_E_CMC",
    "delta_E_ITP",
    "delta_E_HyAB",
    "delta_E_HyCH",
]

JND_CIE1976 = 2.3
if is_documentation_building():  # pragma: no cover
    JND_CIE1976 = DocstringFloat(JND_CIE1976)
    JND_CIE1976.__doc__ = """
Just Noticeable Difference (JND) according to *CIE 1976* colour difference
formula, i.e., Euclidean distance in *CIE L\\*a\\*b\\** colourspace.

Notes
-----
A standard observer sees the difference in colour as follows:

-   0 < :math:`\\Delta E^*_{ab}` < 1 : Observer does not notice the difference.
-   1 < :math:`\\Delta E^*_{ab}` < 2 : Only experienced observer can notice the
    difference.
-   2 < :math:`\\Delta E^*_{ab}` < 3:5 : Unexperienced observer also notices
    the difference.
-   3:5 < :math:`\\Delta E^*_{ab}` < 5 : Clear difference in colour is noticed.
-   5 < :math:`\\Delta E^*_{ab}` : Observer notices two different colours.

References
----------
:cite:`Mokrzycki2011`
"""


def delta_E_CIE1976(Lab_1: ArrayLike, Lab_2: ArrayLike) -> NDArrayFloat:
    """
    Return the difference :math:`\\Delta E_{76}` between two given
    *CIE L\\*a\\*b\\** colourspace arrays using *CIE 1976* recommendation.

    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference :math:`\\Delta E_{76}`.

    Notes
    -----
    +------------+-----------------------+-------------------+
    | **Domain** | **Scale - Reference** | **Scale - 1**     |
    +============+=======================+===================+
    | ``Lab_1``  | ``L_1`` : [0, 100]    | ``L_1`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_1`` : [-100, 100] | ``a_1`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_1`` : [-100, 100] | ``b_1`` : [-1, 1] |
    +------------+-----------------------+-------------------+
    | ``Lab_2``  | ``L_2`` : [0, 100]    | ``L_2`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_2`` : [-100, 100] | ``a_2`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_2`` : [-100, 100] | ``b_2`` : [-1, 1] |
    +------------+-----------------------+-------------------+

    References
    ----------
    :cite:`Lindbloom2003c`

    Examples
    --------
    >>> Lab_1 = np.array([48.99183622, -0.10561667, 400.65619925])
    >>> Lab_2 = np.array([50.65907324, -0.11671910, 402.82235718])
    >>> delta_E_CIE1976(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    2.7335037...
    """

    return euclidean_distance(to_domain_100(Lab_1), to_domain_100(Lab_2))


def delta_E_CIE1994(
    Lab_1: ArrayLike, Lab_2: ArrayLike, textiles: bool = False
) -> NDArrayFloat:
    """
    Return the difference :math:`\\Delta E_{94}` between two given
    *CIE L\\*a\\*b\\** colourspace arrays using *CIE 1994* recommendation.

    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.
    textiles
        Textiles application specific parametric factors,
        :math:`k_L=2,\\ k_C=k_H=1,\\ k_1=0.048,\\ k_2=0.014` weights are used
        instead of :math:`k_L=k_C=k_H=1,\\ k_1=0.045,\\ k_2=0.015`.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference :math:`\\Delta E_{94}`.

    Notes
    -----
    +------------+-----------------------+-------------------+
    | **Domain** | **Scale - Reference** | **Scale - 1**     |
    +============+=======================+===================+
    | ``Lab_1``  | ``L_1`` : [0, 100]    | ``L_1`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_1`` : [-100, 100] | ``a_1`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_1`` : [-100, 100] | ``b_1`` : [-1, 1] |
    +------------+-----------------------+-------------------+
    | ``Lab_2``  | ``L_2`` : [0, 100]    | ``L_2`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_2`` : [-100, 100] | ``a_2`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_2`` : [-100, 100] | ``b_2`` : [-1, 1] |
    +------------+-----------------------+-------------------+

    -   *CIE 1994* colour differences are not symmetrical: difference between
        ``Lab_1`` and ``Lab_2`` may not be the same as difference between
        ``Lab_2`` and ``Lab_1`` thus one colour must be understood to be the
        reference against which a sample colour is compared.

    References
    ----------
    :cite:`Lindbloom2011a`

    Examples
    --------
    >>> Lab_1 = np.array([48.99183622, -0.10561667, 400.65619925])
    >>> Lab_2 = np.array([50.65907324, -0.11671910, 402.82235718])
    >>> delta_E_CIE1994(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    1.6711191...
    >>> delta_E_CIE1994(Lab_1, Lab_2, textiles=True)  # doctest: +ELLIPSIS
    0.8404677...
    """

    L_1, a_1, b_1 = tsplit(to_domain_100(Lab_1))
    L_2, a_2, b_2 = tsplit(to_domain_100(Lab_2))

    k_1 = 0.048 if textiles else 0.045
    k_2 = 0.014 if textiles else 0.015
    k_L = 2 if textiles else 1
    k_C = 1
    k_H = 1

    C_1 = np.hypot(a_1, b_1)
    C_2 = np.hypot(a_2, b_2)

    s_L = 1
    s_C = 1 + k_1 * C_1
    s_H = 1 + k_2 * C_1

    delta_L = L_1 - L_2
    delta_C = C_1 - C_2
    delta_A = a_1 - a_2
    delta_B = b_1 - b_2

    radical = delta_A**2 + delta_B**2 - delta_C**2
    delta_H = zeros(radical.shape)
    delta_H[radical > 0] = np.sqrt(radical[radical > 0])

    L = (delta_L / (k_L * s_L)) ** 2
    C = (delta_C / (k_C * s_C)) ** 2
    H = (delta_H / (k_H * s_H)) ** 2

    d_E = np.sqrt(L + C + H)

    return as_float(d_E)


@dataclass
class Attributes_Specification_CIE2000(MixinDataclassArithmetic):
    """
    Define the *CAM16* colour appearance model specification.

    Parameters
    ----------
    J
        Correlate of *Lightness* :math:`J`.
    C
        Correlate of *chroma* :math:`C`.
    h
        *Hue* angle :math:`h` in degrees.
    s
        Correlate of *saturation* :math:`s`.
    Q
        Correlate of *brightness* :math:`Q`.
    M
        Correlate of *colourfulness* :math:`M`.
    H
        *Hue* :math:`h` quadrature :math:`H`.
    HC
        *Hue* :math:`h` composition :math:`H^C`.
    """

    S_L: float | NDArrayFloat | None = field(default_factory=lambda: None)
    S_C: float | NDArrayFloat | None = field(default_factory=lambda: None)
    S_H: float | NDArrayFloat | None = field(default_factory=lambda: None)
    delta_L_p: float | NDArrayFloat | None = field(default_factory=lambda: None)
    delta_C_p: float | NDArrayFloat | None = field(default_factory=lambda: None)
    delta_H_p: float | NDArrayFloat | None = field(default_factory=lambda: None)
    R_T: float | NDArrayFloat | None = field(default_factory=lambda: None)


def intermediate_attributes_CIE2000(
    Lab_1: ArrayLike, Lab_2: ArrayLike
) -> Attributes_Specification_CIE2000:
    """
    Return the intermediate attributes to compute the difference
    :math:`\\Delta E_{00}` between two given *CIE L\\*a\\*b\\** colourspace
    arrays using *CIE 2000* recommendation.

    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.

    Returns
    -------
    :class:`numpy.ndarray`
        Intermediate attributes to compute the difference :math:`\\Delta E_{00}`.

    References
    ----------
    :cite:`Melgosa2013b`, :cite:`Sharma2005b`

    Examples
    --------
    >>> Lab_1 = np.array([48.99183622, -0.10561667, 400.65619925])
    >>> Lab_2 = np.array([50.65907324, -0.11671910, 402.82235718])
    >>> intermediate_attributes_CIE2000(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    Attributes_Specification_CIE2000(S_L=1.0001021..., S_C=19.0782682..., \
S_H=4.7226695..., delta_L_p=1.6672370..., delta_C_p=2.1661609..., \
delta_H_p=0.0105030..., R_T=-3...)
    """

    L_1, a_1, b_1 = tsplit(to_domain_100(Lab_1))
    L_2, a_2, b_2 = tsplit(to_domain_100(Lab_2))

    C_1_ab = np.hypot(a_1, b_1)
    C_2_ab = np.hypot(a_2, b_2)

    C_bar_ab = (C_1_ab + C_2_ab) / 2
    C_bar_ab_7 = C_bar_ab**7

    G = 0.5 * (1 - np.sqrt(C_bar_ab_7 / (C_bar_ab_7 + 25**7)))

    a_p_1 = (1 + G) * a_1
    a_p_2 = (1 + G) * a_2

    C_p_1 = np.hypot(a_p_1, b_1)
    C_p_2 = np.hypot(a_p_2, b_2)

    h_p_1 = np.where(
        np.logical_and(b_1 == 0, a_p_1 == 0),
        0,
        np.degrees(np.arctan2(b_1, a_p_1)) % 360,
    )
    h_p_2 = np.where(
        np.logical_and(b_2 == 0, a_p_2 == 0),
        0,
        np.degrees(np.arctan2(b_2, a_p_2)) % 360,
    )

    delta_L_p = L_2 - L_1

    delta_C_p = C_p_2 - C_p_1

    h_p_2_s_1 = h_p_2 - h_p_1
    C_p_1_m_2 = C_p_1 * C_p_2
    delta_h_p = np.select(
        [
            C_p_1_m_2 == 0,
            np.fabs(h_p_2_s_1) <= 180,
            h_p_2_s_1 > 180,
            h_p_2_s_1 < -180,
        ],
        [
            0,
            h_p_2_s_1,
            h_p_2_s_1 - 360,
            h_p_2_s_1 + 360,
        ],
    )

    delta_H_p = 2 * np.sqrt(C_p_1_m_2) * np.sin(np.deg2rad(delta_h_p / 2))

    L_bar_p = (L_1 + L_2) / 2

    C_bar_p = (C_p_1 + C_p_2) / 2

    a_h_p_1_s_2 = np.fabs(h_p_1 - h_p_2)
    h_p_1_a_2 = h_p_1 + h_p_2
    h_bar_p = np.select(
        [
            C_p_1_m_2 == 0,
            a_h_p_1_s_2 <= 180,
            np.logical_and(a_h_p_1_s_2 > 180, h_p_1_a_2 < 360),
            np.logical_and(a_h_p_1_s_2 > 180, h_p_1_a_2 >= 360),
        ],
        [
            h_p_1_a_2,
            h_p_1_a_2 / 2,
            (h_p_1_a_2 + 360) / 2,
            (h_p_1_a_2 - 360) / 2,
        ],
    )

    T = (
        1
        - 0.17 * np.cos(np.deg2rad(h_bar_p - 30))
        + 0.24 * np.cos(np.deg2rad(2 * h_bar_p))
        + 0.32 * np.cos(np.deg2rad(3 * h_bar_p + 6))
        - 0.20 * np.cos(np.deg2rad(4 * h_bar_p - 63))
    )

    delta_theta = 30 * np.exp(-(((h_bar_p - 275) / 25) ** 2))

    C_bar_p_7 = C_bar_p**7
    R_C = 2 * np.sqrt(C_bar_p_7 / (C_bar_p_7 + 25**7))

    L_bar_p_2 = (L_bar_p - 50) ** 2
    S_L = 1 + ((0.015 * L_bar_p_2) / np.sqrt(20 + L_bar_p_2))

    S_C = 1 + 0.045 * C_bar_p

    S_H = 1 + 0.015 * C_bar_p * T

    R_T = -np.sin(np.deg2rad(2 * delta_theta)) * R_C

    return Attributes_Specification_CIE2000(
        S_L,
        S_C,
        S_H,
        delta_L_p,
        delta_C_p,
        delta_H_p,
        R_T,
    )


def delta_E_CIE2000(
    Lab_1: ArrayLike, Lab_2: ArrayLike, textiles: bool = False
) -> NDArrayFloat:
    """
    Return the difference :math:`\\Delta E_{00}` between two given
    *CIE L\\*a\\*b\\** colourspace arrays using *CIE 2000* recommendation.

    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.
    textiles
        Textiles application specific parametric factors.
        :math:`k_L=2,\\ k_C=k_H=1` weights are used instead of
        :math:`k_L=k_C=k_H=1`.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference :math:`\\Delta E_{00}`.

    Notes
    -----
    +------------+-----------------------+-------------------+
    | **Domain** | **Scale - Reference** | **Scale - 1**     |
    +============+=======================+===================+
    | ``Lab_1``  | ``L_1`` : [0, 100]    | ``L_1`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_1`` : [-100, 100] | ``a_1`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_1`` : [-100, 100] | ``b_1`` : [-1, 1] |
    +------------+-----------------------+-------------------+
    | ``Lab_2``  | ``L_2`` : [0, 100]    | ``L_2`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_2`` : [-100, 100] | ``a_2`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_2`` : [-100, 100] | ``b_2`` : [-1, 1] |
    +------------+-----------------------+-------------------+

    -   Parametric factors :math:`k_L=k_C=k_H=1` weights under
        *reference conditions*:

        -   Illumination: D65 source
        -   Illuminance: 1000 lx
        -   Observer: Normal colour vision
        -   Background field: Uniform, neutral gray with :math:`L^*=50`
        -   Viewing mode: Object
        -   Sample size: Greater than 4 degrees
        -   Sample separation: Direct edge contact
        -   Sample colour-difference magnitude: Lower than 5.0
            :math:`\\Delta E_{00}`
        -   Sample structure: Homogeneous (without texture)

    References
    ----------
    :cite:`Melgosa2013b`, :cite:`Sharma2005b`

    Examples
    --------
    >>> Lab_1 = np.array([48.99183622, -0.10561667, 400.65619925])
    >>> Lab_2 = np.array([50.65907324, -0.11671910, 402.82235718])
    >>> delta_E_CIE2000(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    1.6709303...
    >>> delta_E_CIE2000(Lab_1, Lab_2, textiles=True)  # doctest: +ELLIPSIS
    0.8412338...
    """

    S_L, S_C, S_H, delta_L_p, delta_C_p, delta_H_p, R_T = astuple(
        intermediate_attributes_CIE2000(Lab_1, Lab_2)
    )

    k_L = 2 if textiles else 1
    k_C = 1
    k_H = 1

    d_E = np.sqrt(
        (delta_L_p / (k_L * S_L)) ** 2
        + (delta_C_p / (k_C * S_C)) ** 2
        + (delta_H_p / (k_H * S_H)) ** 2
        + R_T * (delta_C_p / (k_C * S_C)) * (delta_H_p / (k_H * S_H))
    )

    return as_float(d_E)


def delta_E_CMC(
    Lab_1: ArrayLike,
    Lab_2: ArrayLike,
    l: float = 2,  # noqa: E741
    c: float = 1,
) -> NDArrayFloat:
    """
    Return the difference :math:`\\Delta E_{CMC}` between two given
    *CIE L\\*a\\*b\\** colourspace arrays using *Colour Measurement Committee*
    recommendation.

    The quasimetric has two parameters: *Lightness* (l) and *chroma* (c),
    allowing the users to weight the difference based on the ratio of l:c.
    Commonly used values are 2:1 for acceptability and 1:1 for the threshold of
    imperceptibility.

    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.
    l
        Lightness weighting factor.
    c
        Chroma weighting factor.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference :math:`\\Delta E_{CMC}`.

    Notes
    -----
    +------------+-----------------------+-------------------+
    | **Domain** | **Scale - Reference** | **Scale - 1**     |
    +============+=======================+===================+
    | ``Lab_1``  | ``L_1`` : [0, 100]    | ``L_1`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_1`` : [-100, 100] | ``a_1`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_1`` : [-100, 100] | ``b_1`` : [-1, 1] |
    +------------+-----------------------+-------------------+
    | ``Lab_2``  | ``L_2`` : [0, 100]    | ``L_2`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_2`` : [-100, 100] | ``a_2`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_2`` : [-100, 100] | ``b_2`` : [-1, 1] |
    +------------+-----------------------+-------------------+

    References
    ----------
    :cite:`Lindbloom2009f`

    Examples
    --------
    >>> Lab_1 = np.array([48.99183622, -0.10561667, 400.65619925])
    >>> Lab_2 = np.array([50.65907324, -0.11671910, 402.82235718])
    >>> delta_E_CMC(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    0.8996999...
    """

    L_1, a_1, b_1 = tsplit(to_domain_100(Lab_1))
    L_2, a_2, b_2 = tsplit(to_domain_100(Lab_2))

    C_1 = np.hypot(a_1, b_1)
    C_2 = np.hypot(a_2, b_2)
    s_L = np.where(L_1 < 16, 0.511, (0.040975 * L_1) / (1 + 0.01765 * L_1))
    s_C = 0.0638 * C_1 / (1 + 0.0131 * C_1) + 0.638
    h_1 = np.degrees(np.arctan2(b_1, a_1)) % 360

    t = np.where(
        np.logical_and(h_1 >= 164, h_1 <= 345),
        0.56 + np.fabs(0.2 * np.cos(np.deg2rad(h_1 + 168))),
        0.36 + np.fabs(0.4 * np.cos(np.deg2rad(h_1 + 35))),
    )

    C_4 = C_1 * C_1 * C_1 * C_1
    f = np.sqrt(C_4 / (C_4 + 1900))
    s_h = s_C * (f * t + 1 - f)

    delta_L = L_1 - L_2
    delta_C = C_1 - C_2
    delta_A = a_1 - a_2
    delta_B = b_1 - b_2
    delta_H2 = delta_A**2 + delta_B**2 - delta_C**2

    v_1 = delta_L / (l * s_L)
    v_2 = delta_C / (c * s_C)
    v_3 = s_h

    d_E = np.sqrt(v_1**2 + v_2**2 + (delta_H2 / (v_3 * v_3)))

    return as_float(d_E)


def delta_E_ITP(ICtCp_1: ArrayLike, ICtCp_2: ArrayLike) -> NDArrayFloat:
    """
    Return the difference :math:`\\Delta E_{ITP}` between two given
    :math:`IC_TC_P` colour encoding arrays using
    *Recommendation ITU-R BT.2124*.

    Parameters
    ----------
    ICtCp_1
        :math:`IC_TC_P` colour encoding array 1.
    ICtCp_2
        :math:`IC_TC_P` colour encoding array 2.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference :math:`\\Delta E_{ITP}`.

    Notes
    -----
    -   A value of 1 is equivalent to a just noticeable difference when viewed
        in the most critical adaptation state.

    References
    ----------
    :cite:`InternationalTelecommunicationUnion2019`

    Examples
    --------
    >>> ICtCp_1 = np.array([0.4885468072, -0.04739350675, 0.07475401302])
    >>> ICtCp_2 = np.array([0.4899203231, -0.04567508203, 0.07361341775])
    >>> delta_E_ITP(ICtCp_1, ICtCp_2)  # doctest: +ELLIPSIS
    1.42657228...
    """

    I_1, T_1, P_1 = tsplit(ICtCp_1)
    T_1 *= 0.5

    I_2, T_2, P_2 = tsplit(ICtCp_2)
    T_2 *= 0.5

    d_E_ITP = 720 * np.sqrt(
        ((I_2 - I_1) ** 2) + ((T_2 - T_1) ** 2) + ((P_2 - P_1) ** 2)
    )

    return as_float(d_E_ITP)


def delta_E_HyAB(Lab_1: ArrayLike, Lab_2: ArrayLike) -> NDArrayFloat:
    """
    Return the difference between two *CIE L\\*a\\*b\\** colourspace arrays
    using a combination of a Euclidean metric in hue and chroma with a
    city-block metric to incorporate lightness differences.

    This metric is intended for large colour differences, on the order of 10
    CIE L\\*a\\*b\\** units or greater.

    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference HyAB.

    Notes
    -----
    +------------+-----------------------+-------------------+
    | **Domain** | **Scale - Reference** | **Scale - 1**     |
    +============+=======================+===================+
    | ``Lab_1``  | ``L_1`` : [0, 100]    | ``L_1`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_1`` : [-100, 100] | ``a_1`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_1`` : [-100, 100] | ``b_1`` : [-1, 1] |
    +------------+-----------------------+-------------------+
    | ``Lab_2``  | ``L_2`` : [0, 100]    | ``L_2`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_2`` : [-100, 100] | ``a_2`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_2`` : [-100, 100] | ``b_2`` : [-1, 1] |
    +------------+-----------------------+-------------------+

    References
    ----------
    :cite:`Abasi2020a`

    Examples
    --------
    >>> Lab_1 = np.array([39.91531343, 51.16658481, 146.12933781])
    >>> Lab_2 = np.array([53.12207516, -39.92365056, 249.54831278])
    >>> delta_E_HyAB(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    151.0215481...
    """

    dLab = to_domain_100(Lab_1) - to_domain_100(Lab_2)
    dL, da, db = tsplit(dLab)
    HyAB = np.abs(dL) + np.hypot(da, db)

    return as_float(HyAB)


def delta_E_HyCH(
    Lab_1: ArrayLike, Lab_2: ArrayLike, textiles: bool = False
) -> NDArrayFloat:
    """
    Return the difference between two *CIE L\\*a\\*b\\** colourspace arrays
    using a combination of a Euclidean metric in hue and chroma with a
    city-block metric to incorporate lightness differences based on
    *CIE 2000* recommendation attributes.

    This metric is intended for large colour differences, on the order of 10
    CIE L\\*a\\*b\\** units or greater.


    Parameters
    ----------
    Lab_1
        *CIE L\\*a\\*b\\** colourspace array 1.
    Lab_2
        *CIE L\\*a\\*b\\** colourspace array 2.

    Returns
    -------
    :class:`numpy.ndarray`
        Colour difference HyCH.

    Notes
    -----
    +------------+-----------------------+-------------------+
    | **Domain** | **Scale - Reference** | **Scale - 1**     |
    +============+=======================+===================+
    | ``Lab_1``  | ``L_1`` : [0, 100]    | ``L_1`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_1`` : [-100, 100] | ``a_1`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_1`` : [-100, 100] | ``b_1`` : [-1, 1] |
    +------------+-----------------------+-------------------+
    | ``Lab_2``  | ``L_2`` : [0, 100]    | ``L_2`` : [0, 1]  |
    |            |                       |                   |
    |            | ``a_2`` : [-100, 100] | ``a_2`` : [-1, 1] |
    |            |                       |                   |
    |            | ``b_2`` : [-100, 100] | ``b_2`` : [-1, 1] |
    +------------+-----------------------+-------------------+

    References
    ----------
    :cite:`Abasi2020a`

    Examples
    --------
    >>> Lab_1 = np.array([39.91531343, 51.16658481, 146.12933781])
    >>> Lab_2 = np.array([53.12207516, -39.92365056, 249.54831278])
    >>> delta_E_HyCH(Lab_1, Lab_2)  # doctest: +ELLIPSIS
    48.664279419760369...
    """

    S_L, S_C, S_H, delta_L_p, delta_C_p, delta_H_p, R_T = astuple(
        intermediate_attributes_CIE2000(Lab_1, Lab_2)
    )

    k_L = 2 if textiles else 1
    k_C = 1
    k_H = 1

    HyCH = np.abs(delta_L_p / (k_L * S_L)) + np.sqrt(
        (delta_C_p / (k_C * S_C)) ** 2 + (delta_H_p / (k_H * S_H)) ** 2
    )

    return as_float(HyCH)
