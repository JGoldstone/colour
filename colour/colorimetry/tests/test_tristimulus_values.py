"""
Define the unit tests for the :mod:`colour.colorimetry.tristimulus_values`
module.

References
----------
-   :cite:`ASTMInternational2015b` : ASTM International. (2015). ASTM E308-15 -
    Standard Practice for Computing the Colors of Objects by Using the CIE
    System (pp. 1-47). doi:10.1520/E0308-15
"""

from __future__ import annotations

import typing

import numpy as np
import pytest

from colour.algebra import LinearInterpolator, SpragueInterpolator
from colour.characterisation import SDS_COLOURCHECKERS
from colour.colorimetry import (
    MSDS_CMFS,
    SDS_ILLUMINANTS,
    MultiSpectralDistributions,
    SpectralDistribution,
    SpectralShape,
    adjust_tristimulus_weighting_factors_ASTME308,
    handle_spectral_arguments,
    lagrange_coefficients_ASTME2022,
    msds_to_XYZ,
    msds_to_XYZ_ASTME308,
    msds_to_XYZ_integration,
    reshape_msds,
    reshape_sd,
    sd_CIE_standard_illuminant_A,
    sd_ones,
    sd_to_XYZ,
    sd_to_XYZ_ASTME308,
    sd_to_XYZ_integration,
    sd_to_XYZ_tristimulus_weighting_factors_ASTME308,
    sd_zeros,
    sds_and_msds_to_msds,
    tristimulus_weighting_factors_ASTME2022,
    wavelength_to_XYZ,
)
from colour.constants import TOLERANCE_ABSOLUTE_TESTS

if typing.TYPE_CHECKING:
    from colour.hints import NDArrayFloat

from colour.utilities import domain_range_scale

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "SD_SAMPLE",
    "LAGRANGE_COEFFICIENTS_A",
    "LAGRANGE_COEFFICIENTS_B",
    "TWF_A_CIE_1964_10_10",
    "TWF_A_CIE_1964_10_20",
    "TWF_D65_CIE_1931_2_20",
    "TWF_D65_CIE_1931_2_20_K1",
    "TWF_D65_CIE_1931_2_20_A",
    "DATA_TWO",
    "MSDS_TWO",
    "TVS_D65_INTEGRATION_MSDS",
    "TVS_D65_ARRAY_INTEGRATION",
    "TVS_D65_ARRAY_K1_INTEGRATION",
    "TVS_D65_ASTME308_MSDS",
    "TVS_D65_ASTME308_K1_MSDS",
    "TestHandleSpectralArguments",
    "TestLagrangeCoefficientsASTME2022",
    "TestTristimulusWeightingFactorsASTME2022",
    "TestAdjustTristimulusWeightingFactorsASTME308",
    "TestSd_to_XYZ_integration",
    "TestSd_to_XYZ_ASTME308",
    "TestSd_to_XYZ",
    "TestMsds_to_XYZ_integration",
    "TestMsds_to_XYZ_ASTME308",
    "TestAbsoluteIntegrationToXYZ",
    "TestWavelength_to_XYZ",
]

SD_SAMPLE: SpectralDistribution = SpectralDistribution(
    {
        340: 0.0000,
        345: 0.0000,
        350: 0.0000,
        355: 0.0000,
        360: 0.0000,
        365: 0.0000,
        370: 0.0000,
        375: 0.0000,
        380: 0.0000,
        385: 0.0000,
        390: 0.0000,
        395: 0.0000,
        400: 0.0641,
        405: 0.0650,
        410: 0.0654,
        415: 0.0652,
        420: 0.0645,
        425: 0.0629,
        430: 0.0605,
        435: 0.0581,
        440: 0.0562,
        445: 0.0551,
        450: 0.0543,
        455: 0.0539,
        460: 0.0537,
        465: 0.0538,
        470: 0.0541,
        475: 0.0547,
        480: 0.0559,
        485: 0.0578,
        490: 0.0603,
        495: 0.0629,
        500: 0.0651,
        505: 0.0667,
        510: 0.0680,
        515: 0.0691,
        520: 0.0705,
        525: 0.0720,
        530: 0.0736,
        535: 0.0753,
        540: 0.0772,
        545: 0.0791,
        550: 0.0809,
        555: 0.0833,
        560: 0.0870,
        565: 0.0924,
        570: 0.0990,
        575: 0.1061,
        580: 0.1128,
        585: 0.1190,
        590: 0.1251,
        595: 0.1308,
        600: 0.1360,
        605: 0.1403,
        610: 0.1439,
        615: 0.1473,
        620: 0.1511,
        625: 0.1550,
        630: 0.1590,
        635: 0.1634,
        640: 0.1688,
        645: 0.1753,
        650: 0.1828,
        655: 0.1909,
        660: 0.1996,
        665: 0.2088,
        670: 0.2187,
        675: 0.2291,
        680: 0.2397,
        685: 0.2505,
        690: 0.2618,
        695: 0.2733,
        700: 0.2852,
        705: 0.0000,
        710: 0.0000,
        715: 0.0000,
        720: 0.0000,
        725: 0.0000,
        730: 0.0000,
        735: 0.0000,
        740: 0.0000,
        745: 0.0000,
        750: 0.0000,
        755: 0.0000,
        760: 0.0000,
        765: 0.0000,
        770: 0.0000,
        775: 0.0000,
        780: 0.0000,
        785: 0.0000,
        790: 0.0000,
        795: 0.0000,
        800: 0.0000,
        805: 0.0000,
        810: 0.0000,
        815: 0.0000,
        820: 0.0000,
        825: 0.0000,
        830: 0.0000,
    }
)

LAGRANGE_COEFFICIENTS_A: NDArrayFloat = np.array(
    [
        [-0.0285, 0.9405, 0.1045, -0.0165],
        [-0.0480, 0.8640, 0.2160, -0.0320],
        [-0.0595, 0.7735, 0.3315, -0.0455],
        [-0.0640, 0.6720, 0.4480, -0.0560],
        [-0.0625, 0.5625, 0.5625, -0.0625],
        [-0.0560, 0.4480, 0.6720, -0.0640],
        [-0.0455, 0.3315, 0.7735, -0.0595],
        [-0.0320, 0.2160, 0.8640, -0.0480],
        [-0.0165, 0.1045, 0.9405, -0.0285],
    ]
)

LAGRANGE_COEFFICIENTS_B: NDArrayFloat = np.array(
    [
        [0.8550, 0.1900, -0.0450],
        [0.7200, 0.3600, -0.0800],
        [0.5950, 0.5100, -0.1050],
        [0.4800, 0.6400, -0.1200],
        [0.3750, 0.7500, -0.1250],
        [0.2800, 0.8400, -0.1200],
        [0.1950, 0.9100, -0.1050],
        [0.1200, 0.9600, -0.0800],
        [0.0550, 0.9900, -0.0450],
    ]
)

TWF_A_CIE_1964_10_10: NDArrayFloat = np.array(
    [
        [-0.000, -0.000, -0.000],
        [-0.000, -0.000, -0.000],
        [-0.000, -0.000, -0.000],
        [0.002, 0.000, 0.008],
        [0.025, 0.003, 0.110],
        [0.134, 0.014, 0.615],
        [0.377, 0.039, 1.792],
        [0.686, 0.084, 3.386],
        [0.964, 0.156, 4.944],
        [1.080, 0.259, 5.806],
        [1.006, 0.424, 5.812],
        [0.731, 0.696, 4.919],
        [0.343, 1.082, 3.300],
        [0.078, 1.616, 1.973],
        [0.022, 2.422, 1.152],
        [0.218, 3.529, 0.658],
        [0.750, 4.840, 0.382],
        [1.642, 6.100, 0.211],
        [2.842, 7.250, 0.102],
        [4.336, 8.114, 0.032],
        [6.200, 8.758, 0.001],
        [8.262, 8.988, -0.000],
        [10.227, 8.760, 0.000],
        [11.945, 8.304, 0.000],
        [12.746, 7.468, 0.000],
        [12.337, 6.323, 0.000],
        [10.817, 5.033, 0.000],
        [8.560, 3.744, 0.000],
        [6.014, 2.506, 0.000],
        [3.887, 1.560, 0.000],
        [2.309, 0.911, 0.000],
        [1.276, 0.499, 0.000],
        [0.666, 0.259, 0.000],
        [0.336, 0.130, 0.000],
        [0.166, 0.065, 0.000],
        [0.082, 0.032, 0.000],
        [0.040, 0.016, 0.000],
        [0.020, 0.008, 0.000],
        [0.010, 0.004, 0.000],
        [0.005, 0.002, 0.000],
        [0.003, 0.001, 0.000],
        [0.001, 0.001, 0.000],
        [0.001, 0.000, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
    ]
)

TWF_A_CIE_1964_10_20: NDArrayFloat = np.array(
    [
        [-0.000, -0.000, -0.001],
        [-0.009, -0.001, -0.041],
        [0.060, 0.005, 0.257],
        [0.773, 0.078, 3.697],
        [1.900, 0.304, 9.755],
        [1.971, 0.855, 11.487],
        [0.718, 2.146, 6.785],
        [0.043, 4.899, 2.321],
        [1.522, 9.647, 0.743],
        [5.677, 14.461, 0.196],
        [12.445, 17.474, 0.005],
        [20.554, 17.584, -0.003],
        [25.332, 14.896, 0.000],
        [21.571, 10.080, 0.000],
        [12.179, 5.068, 0.000],
        [4.668, 1.830, 0.000],
        [1.324, 0.513, 0.000],
        [0.318, 0.123, 0.000],
        [0.075, 0.029, 0.000],
        [0.018, 0.007, 0.000],
        [0.005, 0.002, 0.000],
        [0.001, 0.001, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
    ]
)

TWF_D65_CIE_1931_2_20: NDArrayFloat = np.array(
    [
        [-0.001, -0.000, -0.005],
        [-0.008, -0.000, -0.039],
        [0.179, 0.002, 0.829],
        [2.542, 0.071, 12.203],
        [6.670, 0.453, 33.637],
        [6.333, 1.316, 36.334],
        [2.213, 2.933, 18.278],
        [0.052, 6.866, 5.543],
        [1.348, 14.106, 1.611],
        [5.767, 18.981, 0.382],
        [11.301, 18.863, 0.068],
        [16.256, 15.455, 0.025],
        [17.933, 10.699, 0.013],
        [14.020, 6.277, 0.003],
        [7.057, 2.743, 0.000],
        [2.527, 0.927, -0.000],
        [0.670, 0.242, -0.000],
        [0.140, 0.050, 0.000],
        [0.035, 0.013, 0.000],
        [0.008, 0.003, 0.000],
        [0.002, 0.001, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
        [0.000, 0.000, 0.000],
    ]
)

TWF_D65_CIE_1931_2_20_K1: NDArrayFloat = np.array(
    [
        [-0.10095678, -0.00265636, -0.48295051],
        [-0.83484763, -0.02190274, -4.11563004],
        [18.94315946, 0.22803520, 87.62930101],
        [268.66426663, 7.45156533, 1289.46785306],
        [704.84093814, 47.85119956, 3554.47729494],
        [669.16372619, 139.09334752, 3839.47028848],
        [233.89418975, 309.95075927, 1931.47489098],
        [5.51347204, 725.55154566, 585.77542998],
        [142.48116090, 1490.55009270, 170.27819443],
        [609.43424752, 2005.73581058, 40.34233506],
        [1194.21293134, 1993.32004423, 7.15981395],
        [1717.79835378, 1633.12477710, 2.59651081],
        [1895.00791740, 1130.54333854, 1.34461357],
        [1481.55235852, 663.25632432, 0.29999368],
        [745.76471129, 289.85683288, 0.01943154],
        [267.01875994, 97.97358872, -0.00261658],
        [70.75239887, 25.56445574, -0.00019929],
        [14.78862574, 5.31713332, 0.00000000],
        [3.67620064, 1.32650433, 0.00000000],
        [0.89699648, 0.32392186, 0.00000000],
        [0.16623785, 0.06003153, 0.00000000],
        [0.04824448, 0.01742197, 0.00000000],
        [0.01310759, 0.00473339, 0.00000000],
        [0.00223616, 0.00080752, 0.00000000],
    ]
)

TWF_D65_CIE_1931_2_20_A: NDArrayFloat = np.array(
    [
        [0.170, 0.002, 0.785],
        [2.542, 0.071, 12.203],
        [6.670, 0.453, 33.637],
        [6.333, 1.316, 36.334],
        [2.213, 2.933, 18.278],
        [0.052, 6.866, 5.543],
        [1.348, 14.106, 1.611],
        [5.767, 18.981, 0.382],
        [11.301, 18.863, 0.068],
        [16.256, 15.455, 0.025],
        [17.933, 10.699, 0.013],
        [14.020, 6.277, 0.003],
        [7.057, 2.743, 0.000],
        [2.527, 0.927, -0.000],
        [0.670, 0.242, -0.000],
        [0.185, 0.067, 0.000],
    ]
)

DATA_TWO: NDArrayFloat = np.array(
    [
        [
            [
                0.01367208,
                0.09127947,
                0.01524376,
                0.02810712,
                0.19176012,
                0.04299992,
            ],
            [
                0.01591516,
                0.31454948,
                0.08416876,
                0.09071489,
                0.71026170,
                0.04374762,
            ],
            [
                0.00959792,
                0.25822842,
                0.41388571,
                0.22275120,
                0.00407416,
                0.37439537,
            ],
            [
                0.01106279,
                0.07090867,
                0.02204929,
                0.12487984,
                0.18168917,
                0.00202945,
            ],
            [
                0.01791409,
                0.29707789,
                0.56295109,
                0.23752193,
                0.00236515,
                0.58190280,
            ],
            [
                0.10565346,
                0.46204320,
                0.19180590,
                0.56250858,
                0.42085907,
                0.00270085,
            ],
        ],
        [
            [
                0.04325933,
                0.26825359,
                0.23732357,
                0.05175860,
                0.01181048,
                0.08233768,
            ],
            [
                0.02577249,
                0.08305486,
                0.04303044,
                0.32298771,
                0.23022813,
                0.00813306,
            ],
            [
                0.02484169,
                0.12027161,
                0.00541695,
                0.00654612,
                0.18603799,
                0.36247808,
            ],
            [
                0.01861601,
                0.12924391,
                0.00785840,
                0.40062562,
                0.94044405,
                0.32133976,
            ],
            [
                0.03102159,
                0.16815442,
                0.37186235,
                0.08610666,
                0.00413520,
                0.78492409,
            ],
            [
                0.04727245,
                0.32210270,
                0.22679484,
                0.31613642,
                0.11242847,
                0.00244144,
            ],
        ],
    ]
)

MSDS_TWO: MultiSpectralDistributions = MultiSpectralDistributions(
    np.transpose(np.reshape(DATA_TWO, [-1, 6])),
    SpectralShape(400, 700, 60).wavelengths,
)

TVS_D65_INTEGRATION_MSDS: NDArrayFloat = np.array(
    [
        [7.50219602, 3.95048275, 8.40152163],
        [26.92629005, 15.07170066, 28.71020457],
        [16.70060700, 28.21421317, 25.64802044],
        [11.57577260, 8.64108703, 6.57740493],
        [18.73108262, 35.07369122, 30.14365007],
        [45.16559608, 39.61411218, 43.68158810],
        [8.17318743, 13.09236381, 25.93755134],
        [22.46715798, 19.31066951, 7.95954422],
        [6.58106180, 2.52865132, 11.09122159],
        [43.91745731, 27.98043364, 11.73313699],
        [8.53693599, 19.70195654, 17.70110118],
        [23.91114755, 26.21471641, 30.67613685],
    ]
)

TVS_D65_ARRAY_INTEGRATION: NDArrayFloat = np.array(
    [
        [
            [7.19510558, 3.86227393, 10.09950719],
            [25.57464912, 14.71934603, 34.84931928],
            [17.58300551, 28.56388139, 30.18370150],
            [11.32631694, 8.46087304, 7.90263107],
            [19.65793587, 35.59047030, 35.14042633],
            [45.82162927, 39.26057155, 51.79537877],
        ],
        [
            [8.82617380, 13.38600040, 30.56510531],
            [22.33167167, 18.95683859, 9.39034481],
            [6.69130415, 2.57592352, 13.25898396],
            [41.81950400, 27.11920225, 14.26746010],
            [9.24148668, 20.20448258, 20.19416075],
            [24.78545992, 26.22388193, 36.44325237],
        ],
    ]
)

TVS_D65_ARRAY_K1_INTEGRATION: NDArrayFloat = np.array(
    [
        [
            [7.7611755347, 4.1661356647, 10.8940789347],
            [27.5867169575, 15.8773804035, 37.5910653835],
            [18.9663363103, 30.8111250154, 32.5583833518],
            [12.2174071019, 9.1265263825, 8.5243651028],
            [21.2045103874, 38.3905259546, 37.9050750799],
            [49.4266142767, 42.3493698798, 55.8703443988],
        ],
        [
            [9.5205669281, 14.4391347280, 32.9697938475],
            [24.0886005021, 20.4482547598, 10.1291236929],
            [7.2177378835, 2.7785825207, 14.3021253594],
            [45.1096245706, 29.2527867434, 15.3899426670],
            [9.9685542597, 21.7940562871, 21.7829223889],
            [26.7354388456, 28.2870277157, 39.3104000571],
        ],
    ]
)

TVS_D65_ASTME308_MSDS: NDArrayFloat = np.array(
    [
        [7.50450425, 3.95744742, 8.38735462],
        [26.94116124, 15.09801442, 28.66753115],
        [16.70212538, 28.20596151, 25.65809190],
        [11.57025728, 8.64549437, 6.55935421],
        [18.74248163, 35.06128859, 30.17576781],
        [45.12240306, 39.62432052, 43.58455883],
        [8.17632546, 13.09396693, 25.92811880],
        [22.44582614, 19.31227394, 7.92623840],
        [6.57937576, 2.53370970, 11.07068448],
        [43.91405117, 28.00039763, 11.68910584],
        [8.54996478, 19.69029667, 17.73601959],
        [23.88899194, 26.21653407, 30.62958339],
    ]
)

TVS_D65_ASTME308_K1_MSDS: NDArrayFloat = np.array(
    [
        [7.9300584037, 4.1818604067, 8.8629721234],
        [28.4689001419, 15.9541699464, 30.2931664392],
        [17.6492444185, 29.8054228038, 27.1130724359],
        [12.2263660519, 9.1357500818, 6.9313122104],
        [19.8053021265, 37.0494914782, 31.8869299177],
        [47.6811365133, 41.8712769685, 46.0560865221],
        [8.6399762445, 13.8364799389, 27.3984116154],
        [23.7186503263, 20.4074053594, 8.3757076242],
        [6.9524691183, 2.6773875067, 11.6984642292],
        [46.4042632139, 29.5882021193, 12.3519540951],
        [9.0348033348, 20.8068644330, 18.7417671434],
        [25.2436530136, 27.7031818974, 32.3664797963],
    ]
)


class TestHandleSpectralArguments:
    """
    Define :func:`colour.colorimetry.tristimulus_values.\
handle_spectral_arguments` definition unit tests methods.
    """

    def test_handle_spectral_arguments(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
handle_spectral_arguments` definition.
        """

        cmfs, illuminant = handle_spectral_arguments()
        assert cmfs == reshape_msds(MSDS_CMFS["CIE 1931 2 Degree Standard Observer"])
        assert illuminant == reshape_sd(SDS_ILLUMINANTS["D65"])

        shape = SpectralShape(400, 700, 20)
        cmfs, illuminant = handle_spectral_arguments(shape_default=shape)
        assert cmfs.shape == shape
        assert illuminant.shape == shape

        cmfs, illuminant = handle_spectral_arguments(
            cmfs_default="CIE 2015 2 Degree Standard Observer",
            illuminant_default="E",
            shape_default=shape,
        )
        assert cmfs == reshape_msds(
            MSDS_CMFS["CIE 2015 2 Degree Standard Observer"], shape=shape
        )
        assert illuminant == sd_ones(shape, interpolator=LinearInterpolator) * 100


class TestLagrangeCoefficientsASTME2022:
    """
    Define :func:`colour.colorimetry.tristimulus_values.\
lagrange_coefficients_ASTME2022` definition unit tests methods.
    """

    def test_lagrange_coefficients_ASTME2022(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
lagrange_coefficients_ASTME2022` definition.
        """

        np.testing.assert_allclose(
            lagrange_coefficients_ASTME2022(10, "inner"),
            LAGRANGE_COEFFICIENTS_A,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            lagrange_coefficients_ASTME2022(10, "boundary"),
            LAGRANGE_COEFFICIENTS_B,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        # Testing that the cache returns a copy of the data.
        lagrange_coefficients = lagrange_coefficients_ASTME2022(10)

        np.testing.assert_allclose(
            lagrange_coefficients,
            LAGRANGE_COEFFICIENTS_A,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        lagrange_coefficients *= 10

        np.testing.assert_allclose(
            lagrange_coefficients_ASTME2022(10),
            LAGRANGE_COEFFICIENTS_A,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestTristimulusWeightingFactorsASTME2022:
    """
    Define :func:`colour.colorimetry.tristimulus_values.\
tristimulus_weighting_factors_ASTME2022` definition unit tests methods.
    """

    def test_tristimulus_weighting_factors_ASTME2022(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
tristimulus_weighting_factors_ASTME2022` definition.

        Notes
        -----
        -   :attr:`TWF_A_CIE_1964_10_10`, :attr:`TWF_A_CIE_1964_10_20` and
            :attr:`TWF_D65_CIE_1931_2_20` attributes data is matching
            :cite:`ASTMInternational2015b`.

        References
        ----------
        :cite:`ASTMInternational2015b`
        """

        cmfs = MSDS_CMFS["CIE 1964 10 Degree Standard Observer"]
        A = sd_CIE_standard_illuminant_A(cmfs.shape)

        twf = tristimulus_weighting_factors_ASTME2022(
            cmfs, A, SpectralShape(360, 830, 10)
        )
        np.testing.assert_allclose(np.round(twf, 3), TWF_A_CIE_1964_10_10, atol=1e-5)

        twf = tristimulus_weighting_factors_ASTME2022(
            cmfs, A, SpectralShape(360, 830, 20)
        )
        np.testing.assert_allclose(np.round(twf, 3), TWF_A_CIE_1964_10_20, atol=1e-5)

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        D65 = reshape_sd(
            SDS_ILLUMINANTS["D65"], cmfs.shape, interpolator=LinearInterpolator
        )
        twf = tristimulus_weighting_factors_ASTME2022(
            cmfs, D65, SpectralShape(360, 830, 20)
        )
        np.testing.assert_allclose(
            np.round(twf, 3),
            TWF_D65_CIE_1931_2_20,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        twf = tristimulus_weighting_factors_ASTME2022(
            cmfs, D65, SpectralShape(360, 830, 20), k=1
        )
        np.testing.assert_allclose(
            twf, TWF_D65_CIE_1931_2_20_K1, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        # Testing that the cache returns a copy of the data.
        cmfs = MSDS_CMFS["CIE 1964 10 Degree Standard Observer"]
        twf = tristimulus_weighting_factors_ASTME2022(
            cmfs, A, SpectralShape(360, 830, 10)
        )
        np.testing.assert_allclose(
            np.round(twf, 3),
            TWF_A_CIE_1964_10_10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            np.round(
                tristimulus_weighting_factors_ASTME2022(
                    cmfs, A, SpectralShape(360, 830, 10)
                ),
                3,
            ),
            TWF_A_CIE_1964_10_10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_raise_exception_tristimulus_weighting_factors_ASTME2022(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
tristimulus_weighting_factors_ASTME2022` definition raised exception.
        """

        shape = SpectralShape(360, 830, 10)
        cmfs_1 = MSDS_CMFS["CIE 1964 10 Degree Standard Observer"]
        cmfs_2 = reshape_msds(cmfs_1, shape)
        A_1 = sd_CIE_standard_illuminant_A(cmfs_1.shape)
        A_2 = sd_CIE_standard_illuminant_A(cmfs_2.shape)

        pytest.raises(
            ValueError,
            tristimulus_weighting_factors_ASTME2022,
            cmfs_1,
            A_2,
            shape,
        )

        pytest.raises(
            ValueError,
            tristimulus_weighting_factors_ASTME2022,
            cmfs_2,
            A_1,
            shape,
        )


class TestAdjustTristimulusWeightingFactorsASTME308:
    """
    Define :func:`colour.colorimetry.tristimulus_values.\
adjust_tristimulus_weighting_factors_ASTME308` definition unit tests methods.
    """

    def test_adjust_tristimulus_weighting_factors_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
adjust_tristimulus_weighting_factors_ASTME308` definition.
        """

        np.testing.assert_allclose(
            adjust_tristimulus_weighting_factors_ASTME308(
                TWF_D65_CIE_1931_2_20,
                SpectralShape(360, 830, 20),
                SpectralShape(400, 700, 20),
            ),
            TWF_D65_CIE_1931_2_20_A,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestSd_to_XYZ_integration:
    """
    Define :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_integration`
    definition unit tests methods.
    """

    def test_sd_to_XYZ_integration(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
sd_to_XYZ_integration` definition.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        np.testing.assert_allclose(
            sd_to_XYZ_integration(SD_SAMPLE, cmfs, SDS_ILLUMINANTS["A"]),
            np.array([14.46341147, 10.85819624, 2.04695585]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_integration(
                SD_SAMPLE.values,
                cmfs,
                SDS_ILLUMINANTS["A"],
                shape=SD_SAMPLE.shape,
            ),
            np.array([14.46365947, 10.85828084, 2.04663993]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        cmfs = MSDS_CMFS["CIE 1964 10 Degree Standard Observer"]
        np.testing.assert_allclose(
            sd_to_XYZ_integration(SD_SAMPLE, cmfs, SDS_ILLUMINANTS["C"]),
            np.array([10.77002699, 9.44876636, 6.62415290]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_integration(SD_SAMPLE, cmfs, SDS_ILLUMINANTS["FL2"]),
            np.array([11.57540576, 9.98608874, 3.95242590]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_integration(SD_SAMPLE, cmfs, SDS_ILLUMINANTS["FL2"], k=683),
            np.array([1223.7509261493, 1055.7284645912, 417.8501342332]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_integration(
                SD_SAMPLE,
                cmfs,
                SDS_ILLUMINANTS["FL2"],
                shape=SpectralShape(400, 700, 20),
            ),
            np.array([11.98232967, 10.13543929, 3.66442524]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_sd_to_XYZ_integration(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
sd_to_XYZ_integration` definition domain and range scale support.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        XYZ = sd_to_XYZ_integration(SD_SAMPLE, cmfs, SDS_ILLUMINANTS["A"])

        d_r = (("reference", 1), ("1", 0.01), ("100", 1))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    sd_to_XYZ_integration(SD_SAMPLE, cmfs, SDS_ILLUMINANTS["A"]),
                    XYZ * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )


class TestSd_to_XYZ_tristimulus_weighting_factors_ASTME308:
    """
    Define :func:`colour.colorimetry.tristimulus_values.\
sd_to_XYZ_tristimulus_weighting_factors_ASTME308`
    definition unit tests methods.
    """

    def test_sd_to_XYZ_tristimulus_weighting_factors_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
sd_to_XYZ_tristimulus_weighting_factors_ASTME308`
        definition.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                SD_SAMPLE, cmfs, SDS_ILLUMINANTS["A"]
            ),
            np.array([14.46341867, 10.85820227, 2.04697034]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        cmfs = MSDS_CMFS["CIE 1964 10 Degree Standard Observer"]
        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                SD_SAMPLE, cmfs, SDS_ILLUMINANTS["C"]
            ),
            np.array([10.77005571, 9.44877491, 6.62428210]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                SD_SAMPLE, cmfs, SDS_ILLUMINANTS["FL2"]
            ),
            np.array([11.57542759, 9.98605604, 3.95273304]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                reshape_sd(SD_SAMPLE, SpectralShape(400, 700, 5), "Trim"),
                cmfs,
                SDS_ILLUMINANTS["A"],
            ),
            np.array([14.38153638, 10.74503131, 2.01613844]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                reshape_sd(SD_SAMPLE, SpectralShape(400, 700, 10), "Interpolate"),
                cmfs,
                SDS_ILLUMINANTS["A"],
            ),
            np.array([14.38257202, 10.74568178, 2.01588427]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                reshape_sd(SD_SAMPLE, SpectralShape(400, 700, 20), "Interpolate"),
                cmfs,
                SDS_ILLUMINANTS["A"],
            ),
            np.array([14.38329645, 10.74603515, 2.01561113]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                reshape_sd(SD_SAMPLE, SpectralShape(400, 700, 20), "Interpolate"),
                cmfs,
                SDS_ILLUMINANTS["A"],
                k=1,
            ),
            np.array([1636.74881983, 1222.84626486, 229.36669308]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_sd_to_XYZ_twf_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
sd_to_XYZ_tristimulus_weighting_factors_ASTME308` definition domain and
        range scale support.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        XYZ = sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
            SD_SAMPLE, cmfs, SDS_ILLUMINANTS["A"]
        )

        d_r = (("reference", 1), ("1", 0.01), ("100", 1))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    sd_to_XYZ_tristimulus_weighting_factors_ASTME308(
                        SD_SAMPLE, cmfs, SDS_ILLUMINANTS["A"]
                    ),
                    XYZ * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )


class TestSd_to_XYZ_ASTME308:
    """
    Define :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_ASTME308`
    definition unit tests methods.
    """

    def setup_method(self) -> None:
        """Initialise the common tests attributes."""

        self._sd = SD_SAMPLE.copy()
        self._cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        self._A = sd_CIE_standard_illuminant_A(self._cmfs.shape)

    def test_sd_to_XYZ_ASTME308_mi_1nm(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_ASTME308`
        definition for 1 nm measurement intervals.
        """

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, self._cmfs.shape), self._cmfs, self._A
            ),
            np.array([14.46372680, 10.85832950, 2.04663200]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, self._cmfs.shape),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.46366018, 10.85827949, 2.04662258]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 1)),
                self._cmfs,
                self._A,
            ),
            np.array([14.54173397, 10.88628632, 2.04965822]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 1)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.54203076, 10.88636754, 2.04964877]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 1)),
                self._cmfs,
                self._A,
                k=1,
            ),
            np.array([15.6898152997, 11.7457671769, 2.2114803420]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_sd_to_XYZ_ASTME308_mi_5nm(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_ASTME308`
        definition for 5 nm measurement intervals.
        """

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 830, 5)),
                self._cmfs,
                self._A,
            ),
            np.array([14.46372173, 10.85832502, 2.04664734]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 830, 5)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.46366388, 10.85828159, 2.04663915]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 830, 5)),
                self._cmfs,
                self._A,
                mi_5nm_omission_method=False,
            ),
            np.array([14.46373399, 10.85833553, 2.0466465]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 5)),
                self._cmfs,
                self._A,
            ),
            np.array([14.54025742, 10.88576251, 2.04950226]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 5)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.54051517, 10.88583304, 2.04949406]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 5)),
                self._cmfs,
                self._A,
                mi_5nm_omission_method=False,
            ),
            np.array([14.54022093, 10.88575468, 2.04951057]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 830, 5)),
                self._cmfs,
                self._A,
                use_practice_range=False,
                mi_5nm_omission_method=False,
            ),
            np.array([14.46366737, 10.85828552, 2.04663707]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 5)),
                self._cmfs,
                self._A,
                use_practice_range=False,
                mi_5nm_omission_method=False,
            ),
            np.array([14.54051772, 10.88583590, 2.04950113]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 5)),
                self._cmfs,
                self._A,
                k=1,
            ),
            np.array([15.6882479013, 11.7452212708, 2.2113156963]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_sd_to_XYZ_ASTME308_mi_10nm(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_ASTME308`
        definition for 10 nm measurement intervals.
        """

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 830, 10)),
                self._cmfs,
                self._A,
            ),
            np.array([14.47779980, 10.86358645, 2.04751388]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 830, 10)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.47773312, 10.86353641, 2.04750445]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 10)),
                self._cmfs,
                self._A,
            ),
            np.array([14.54137532, 10.88641727, 2.04931318]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 10)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.54167211, 10.88649849, 2.04930374]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 10)),
                self._cmfs,
                self._A,
                k=1,
            ),
            np.array([15.6894283333, 11.7459084705, 2.2111080639]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(401, 701, 10)),
                self._cmfs,
                self._A,
                k=1,
            ),
            np.array([15.6713226093, 11.7392254489, 2.2117708792]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_sd_to_XYZ_ASTME308_mi_20nm(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_ASTME308`
        definition for 20 nm measurement intervals.
        """

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 820, 20)),
                self._cmfs,
                self._A,
            ),
            np.array([14.50187464, 10.87217124, 2.04918305]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 820, 20)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.50180785, 10.87212116, 2.04917361]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 820, 20)),
                self._cmfs,
                self._A,
                mi_20nm_interpolation_method=False,
            ),
            np.array([14.50216194, 10.87236873, 2.04977256]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 20)),
                self._cmfs,
                self._A,
            ),
            np.array([14.54114025, 10.88634755, 2.04916445]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 20)),
                self._cmfs,
                self._A,
                use_practice_range=False,
            ),
            np.array([14.54143704, 10.88642877, 2.04915501]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 20)),
                self._cmfs,
                self._A,
                mi_20nm_interpolation_method=False,
            ),
            np.array([14.54242562, 10.88694088, 2.04919645]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(360, 820, 20)),
                self._cmfs,
                self._A,
                use_practice_range=False,
                mi_20nm_interpolation_method=False,
            ),
            np.array([14.50209515, 10.87231865, 2.04976312]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 20)),
                self._cmfs,
                self._A,
                use_practice_range=False,
                mi_20nm_interpolation_method=False,
            ),
            np.array([14.54272240, 10.88702210, 2.04918701]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(400, 700, 20)),
                self._cmfs,
                self._A,
                k=1,
            ),
            np.array([15.6891747040, 11.7458332427, 2.2109475945]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ_ASTME308(
                reshape_sd(self._sd, SpectralShape(401, 701, 20)),
                self._cmfs,
                self._A,
            ),
            np.array([14.5220164311, 10.8790959535, 2.0490905325]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_raise_exception_sd_to_XYZ_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ_ASTME308`
        definition raised exception.
        """

        pytest.raises(
            ValueError,
            sd_to_XYZ_ASTME308,
            reshape_sd(self._sd, SpectralShape(360, 820, 2)),
        )


class TestSd_to_XYZ:
    """
    Define :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ` definition
    unit tests methods.
    """

    def setup_method(self) -> None:
        """Initialise the common tests attributes."""

        self._cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        self._A = sd_CIE_standard_illuminant_A(self._cmfs.shape)
        self._sd = reshape_sd(SD_SAMPLE, self._cmfs.shape)

    def test_sd_to_XYZ(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.sd_to_XYZ`
        definition.
        """

        # Testing that the cache returns a copy of the data.
        XYZ = sd_to_XYZ(self._sd, self._cmfs, self._A)

        np.testing.assert_allclose(
            XYZ,
            np.array([14.46372680, 10.85832950, 2.04663200]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ *= 10

        np.testing.assert_allclose(
            sd_to_XYZ(self._sd, self._cmfs, self._A),
            np.array([14.46372680, 10.85832950, 2.04663200]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ(
                self._sd,
                self._cmfs,
                self._A,
                method="Integration",
                shape=SpectralShape(400, 700, 20),
            ),
            np.array([14.52005467, 10.88000966, 2.03888717]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            sd_to_XYZ(
                sds_and_msds_to_msds(SDS_COLOURCHECKERS["babel_average"].values()),
            ),
            np.array(
                [
                    [12.06344619, 10.33615020, 6.25100082],
                    [40.27284790, 35.29615976, 23.01540616],
                    [18.09306423, 18.50797244, 31.67770084],
                    [11.16523793, 13.25122619, 6.36666038],
                    [25.83420330, 23.32560917, 40.31232440],
                    [31.64244829, 41.64149301, 40.76605171],
                    [40.89999141, 31.22508083, 5.82002195],
                    [13.60742370, 11.51655221, 35.39885724],
                    [30.69032237, 19.87942885, 12.46562439],
                    [8.93362430, 6.46162368, 13.07228804],
                    [35.66114785, 44.08411919, 10.28724123],
                    [49.24169657, 43.46327044, 7.13506647],
                    [7.81888273, 5.89050934, 25.75773837],
                    [15.18817149, 22.93975934, 8.94663877],
                    [22.23187260, 12.73987267, 4.62599881],
                    [60.68157753, 60.55780947, 8.43465082],
                    [32.27071879, 20.22049576, 28.85354643],
                    [14.49902213, 19.10377565, 35.60283004],
                    [90.78293221, 91.26928233, 87.29499532],
                    [58.53195263, 58.84257471, 58.34877604],
                    [35.77113141, 35.94371650, 35.85712527],
                    [18.98962045, 19.11651714, 19.15115933],
                    [8.87518188, 8.93947283, 9.06486638],
                    [3.21099614, 3.20073667, 3.25495104],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestMsds_to_XYZ_integration:
    """
    Define :func:`colour.colorimetry.tristimulus_values.\
msds_to_XYZ_integration` definition unit tests methods.
    """

    def test_msds_to_XYZ_integration(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
msds_to_XYZ_integration` definition.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        np.testing.assert_allclose(
            msds_to_XYZ_integration(MSDS_TWO, cmfs, SDS_ILLUMINANTS["D65"]),
            TVS_D65_INTEGRATION_MSDS,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            msds_to_XYZ_integration(
                DATA_TWO,
                cmfs,
                SDS_ILLUMINANTS["D65"],
                shape=SpectralShape(400, 700, 60),
            ),
            TVS_D65_ARRAY_INTEGRATION,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            msds_to_XYZ_integration(
                DATA_TWO,
                cmfs,
                SDS_ILLUMINANTS["D65"],
                1,
                shape=SpectralShape(400, 700, 60),
            ),
            TVS_D65_ARRAY_K1_INTEGRATION,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_msds_to_XYZ_integration(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
msds_to_XYZ_integration` definition domain and range scale support.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        d_r = (("reference", 1), ("1", 0.01), ("100", 1))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    msds_to_XYZ_integration(
                        DATA_TWO,
                        cmfs,
                        SDS_ILLUMINANTS["D65"],
                        shape=SpectralShape(400, 700, 60),
                    ),
                    TVS_D65_ARRAY_INTEGRATION * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )


class TestMsds_to_XYZ_ASTME308:
    """
    Define :func:`colour.colorimetry.tristimulus_values.msds_to_XYZ_ASTME308`
    definition unit tests methods.
    """

    def test_msds_to_XYZ_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
msds_to_XYZ_ASTME308` definition.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        msds = reshape_msds(MSDS_TWO, SpectralShape(400, 700, 20))
        np.testing.assert_allclose(
            msds_to_XYZ_ASTME308(msds, cmfs, SDS_ILLUMINANTS["D65"]),
            TVS_D65_ASTME308_MSDS,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            msds_to_XYZ_ASTME308(msds, cmfs, SDS_ILLUMINANTS["D65"], k=1),
            TVS_D65_ASTME308_K1_MSDS,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_msds_to_XYZ_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
msds_to_XYZ_ASTME308` definition domain and range scale support.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        d_r = (("reference", 1), ("1", 0.01), ("100", 1))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    msds_to_XYZ_ASTME308(
                        reshape_msds(MSDS_TWO, SpectralShape(400, 700, 20)),
                        cmfs,
                        SDS_ILLUMINANTS["D65"],
                    ),
                    TVS_D65_ASTME308_MSDS * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    def test_raise_exception_msds_to_XYZ_ASTME308(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.\
msds_to_XYZ_ASTME308` definition raise exception.
        """

        pytest.raises(TypeError, msds_to_XYZ_ASTME308, DATA_TWO)


class TestAbsoluteIntegrationToXYZ:
    """
    Test the absolute integration to tristimulus values for :math:`k = 683`
    """

    def test_absolute_integration_to_TVS_1nm(self) -> None:
        """
        Test the absolute, i.e., user given :math:`k` value, integration to
        tristimulus values for 1nm interval.
        """

        sd = sd_zeros(SpectralShape(380, 780, 1))

        k = 683
        sd[555] = 1  # 1 watt at 555nm, 0 watt everywhere else.

        methods = [
            sd_to_XYZ,
            sd_to_XYZ_ASTME308,
            sd_to_XYZ_integration,
            msds_to_XYZ,
            msds_to_XYZ_ASTME308,
            msds_to_XYZ_integration,
        ]

        # Test single spectral distribution integration methods.
        for method in methods[0:3]:
            XYZ = method(sd, k=k)
            XYZ = np.reshape(XYZ, 3) if len(XYZ.shape) > 1 else XYZ
            (
                np.testing.assert_allclose(XYZ[1], k, atol=5e-5),
                (
                    "1 watt @ 555nm should be approximately 683 candela."
                    f" Failed method: {method}"
                ),
            )

        # Test multi-spectral distributions integration methods.
        msds = MultiSpectralDistributions(sd)
        for method in methods[3:6]:
            XYZ: np.ndarray = method(msds, k=k)
            if len(XYZ.shape) > 1:
                XYZ = np.reshape(XYZ, 3)
            (
                np.testing.assert_allclose(XYZ[1], k, atol=5e-5),
                (
                    "1 watt @ 555nm should be approximately 683 candela."
                    f" Failed method: {method}"
                ),
            )

    def test_absolute_integration_to_TVS_5nm(self) -> None:
        """
        Test the absolute, i.e., user given :math:`k` value, integration to
        tristimulus values for 5nm interval by ensuring that the *Riemann Sum*
        accounts for the :math:`\\delta w` term.
        """

        sd = sd_zeros(SpectralShape(380, 780, 5), interpolator=SpragueInterpolator)

        # 1 watt at 555nm, 0 watt everywhere else.
        # For 5nm average sampling, this corresponds to 0.2 watt at 555nm.
        k = 683
        sd[555] = 0.2

        methods = [
            sd_to_XYZ,
            sd_to_XYZ_ASTME308,
            sd_to_XYZ_integration,
            msds_to_XYZ,
            msds_to_XYZ_ASTME308,
            msds_to_XYZ_integration,
        ]

        # Test single spectral distribution integration methods.
        for method in methods[0:3]:
            XYZ: np.ndarray = method(sd, k=k)
            XYZ = np.reshape(XYZ, 3) if len(XYZ.shape) > 1 else XYZ
            (
                np.testing.assert_allclose(XYZ[1], k, atol=5e-2),
                (
                    "1 watt @ 555nm should be approximately 683 candela. "
                    f"Failed method: {method}"
                ),
            )

        # Test multi-spectral distributions integration methods.
        msds = MultiSpectralDistributions(sd)
        for method in methods[3:6]:
            XYZ: np.ndarray = method(msds, k=k)
            if len(XYZ.shape) > 1:
                XYZ = np.reshape(XYZ, 3)
            (
                np.testing.assert_allclose(XYZ[1], k, atol=5e-2),
                (
                    "1 watt @ 555nm should be approximately 683 candela."
                    f"Failed method: {method}"
                ),
            )


class TestWavelength_to_XYZ:
    """
    Define :func:`colour.colorimetry.tristimulus_values.wavelength_to_XYZ`
    definition unit tests methods.
    """

    def test_wavelength_to_XYZ(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.wavelength_to_XYZ`
        definition.
        """

        np.testing.assert_allclose(
            wavelength_to_XYZ(480, MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]),
            np.array([0.09564, 0.13902, 0.81295]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            wavelength_to_XYZ(480, MSDS_CMFS["CIE 2015 2 Degree Standard Observer"]),
            np.array([0.08182895, 0.17880480, 0.75523790]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            wavelength_to_XYZ(641.5, MSDS_CMFS["CIE 2015 2 Degree Standard Observer"]),
            np.array([0.44575583, 0.18184213, 0.00000000]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_raise_exception_wavelength_to_XYZ(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.wavelength_to_XYZ`
        definition raised exception.
        """

        pytest.raises(ValueError, wavelength_to_XYZ, 1)

        pytest.raises(ValueError, wavelength_to_XYZ, 1000)

    def test_n_dimensional_wavelength_to_XYZ(self) -> None:
        """
        Test :func:`colour.colorimetry.tristimulus_values.wavelength_to_XYZ`
        definition n-dimensional arrays support.
        """

        cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        wl = 480
        XYZ = wavelength_to_XYZ(wl, cmfs)

        wl = np.tile(wl, 6)
        XYZ = np.tile(XYZ, (6, 1))
        np.testing.assert_allclose(
            wavelength_to_XYZ(wl, cmfs), XYZ, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        wl = np.reshape(wl, (2, 3))
        XYZ = np.reshape(XYZ, (2, 3, 3))
        np.testing.assert_allclose(
            wavelength_to_XYZ(wl, cmfs), XYZ, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        wl = np.reshape(wl, (2, 3, 1))
        XYZ = np.reshape(XYZ, (2, 3, 1, 3))
        np.testing.assert_allclose(
            wavelength_to_XYZ(wl, cmfs), XYZ, atol=TOLERANCE_ABSOLUTE_TESTS
        )
