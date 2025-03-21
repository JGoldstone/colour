"""Define the unit tests for the :mod:`colour.adaptation.vonkries` module."""

from __future__ import annotations

from itertools import product

import numpy as np

from colour.adaptation import (
    chromatic_adaptation_VonKries,
    matrix_chromatic_adaptation_VonKries,
)
from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.utilities import domain_range_scale, ignore_numpy_errors

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestMatrixChromaticAdaptationVonKries",
    "TestChromaticAdaptationVonKries",
]


class TestMatrixChromaticAdaptationVonKries:
    """
    Define :func:`colour.adaptation.vonkries.\
matrix_chromatic_adaptation_VonKries` definition unit tests methods.
    """

    def test_matrix_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.\
matrix_chromatic_adaptation_VonKries` definition.
        """

        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
            ),
            np.array(
                [
                    [1.04257389, 0.03089108, -0.05281257],
                    [0.02219345, 1.00185663, -0.02107375],
                    [-0.00116488, -0.00342053, 0.76178907],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([1.09846607, 1.00000000, 0.35582280]),
            ),
            np.array(
                [
                    [1.17159793, 0.16088780, -0.16158366],
                    [0.11462057, 0.96182051, -0.06497572],
                    [-0.00413024, -0.00912739, 0.33871096],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.99144661, 1.00000000, 0.67315942]),
            ),
            np.linalg.inv(
                matrix_chromatic_adaptation_VonKries(
                    np.array([0.99144661, 1.00000000, 0.67315942]),
                    np.array([0.95045593, 1.00000000, 1.08905775]),
                )
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
                transform="XYZ Scaling",
            ),
            np.array(
                [
                    [1.01456117, 0.00000000, 0.00000000],
                    [0.00000000, 1.00000000, 0.00000000],
                    [0.00000000, 0.00000000, 0.75763163],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
                transform="Bradford",
            ),
            np.array(
                [
                    [1.04792979, 0.02294687, -0.05019227],
                    [0.02962781, 0.99043443, -0.01707380],
                    [-0.00924304, 0.01505519, 0.75187428],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
                transform="Von Kries",
            ),
            np.array(
                [
                    [1.01611856, 0.05535971, -0.05219186],
                    [0.00608087, 0.99555604, -0.00122642],
                    [0.00000000, 0.00000000, 0.75763163],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_matrix_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.\
matrix_chromatic_adaptation_VonKries` definition n-dimensional arrays support.
        """

        XYZ_w = np.array([0.95045593, 1.00000000, 1.08905775])
        XYZ_wr = np.array([0.96429568, 1.00000000, 0.82510460])
        M = matrix_chromatic_adaptation_VonKries(XYZ_w, XYZ_wr)

        XYZ_w = np.tile(XYZ_w, (6, 1))
        XYZ_wr = np.tile(XYZ_wr, (6, 1))
        M = np.reshape(np.tile(M, (6, 1)), (6, 3, 3))
        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(XYZ_w, XYZ_wr),
            M,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ_w = np.reshape(XYZ_w, (2, 3, 3))
        XYZ_wr = np.reshape(XYZ_wr, (2, 3, 3))
        M = np.reshape(M, (2, 3, 3, 3))
        np.testing.assert_allclose(
            matrix_chromatic_adaptation_VonKries(XYZ_w, XYZ_wr),
            M,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_matrix_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.\
matrix_chromatic_adaptation_VonKries` definition domain and range scale
        support.
        """

        XYZ_w = np.array([0.95045593, 1.00000000, 1.08905775])
        XYZ_wr = np.array([0.96429568, 1.00000000, 0.82510460])
        M = matrix_chromatic_adaptation_VonKries(XYZ_w, XYZ_wr)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    matrix_chromatic_adaptation_VonKries(
                        XYZ_w * factor, XYZ_wr * factor
                    ),
                    M,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_matrix_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.\
matrix_chromatic_adaptation_VonKries` definition nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=3))))
        matrix_chromatic_adaptation_VonKries(cases, cases)


class TestChromaticAdaptationVonKries:
    """
    Define :func:`colour.adaptation.vonkries.chromatic_adaptation_VonKries`
    definition unit tests methods.
    """

    def test_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.chromatic_adaptation_VonKries`
        definition.
        """

        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(
                np.array([0.20654008, 0.12197225, 0.05136952]),
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
            ),
            np.array([0.21638819, 0.12570000, 0.03847494]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(
                np.array([0.14222010, 0.23042768, 0.10495772]),
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([1.09846607, 1.00000000, 0.35582280]),
            ),
            np.array([0.18673833, 0.23111171, 0.03285972]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(
                np.array([0.07818780, 0.06157201, 0.28099326]),
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.99144661, 1.00000000, 0.67315942]),
            ),
            np.array([0.06385467, 0.05509729, 0.17506386]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(
                np.array([0.20654008, 0.12197225, 0.05136952]),
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
                transform="XYZ Scaling",
            ),
            np.array([0.20954755, 0.12197225, 0.03891917]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(
                np.array([0.20654008, 0.12197225, 0.05136952]),
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
                transform="Bradford",
            ),
            np.array([0.21666003, 0.12604777, 0.03855068]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(
                np.array([0.20654008, 0.12197225, 0.05136952]),
                np.array([0.95045593, 1.00000000, 1.08905775]),
                np.array([0.96429568, 1.00000000, 0.82510460]),
                transform="Von Kries",
            ),
            np.array([0.21394049, 0.12262315, 0.03891917]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.chromatic_adaptation_VonKries`
        definition n-dimensional arrays support.
        """

        XYZ = np.array([0.20654008, 0.12197225, 0.05136952])
        XYZ_w = np.array([0.95045593, 1.00000000, 1.08905775])
        XYZ_wr = np.array([0.96429568, 1.00000000, 0.82510460])
        XYZ_a = chromatic_adaptation_VonKries(XYZ, XYZ_w, XYZ_wr)

        XYZ = np.tile(XYZ, (6, 1))
        XYZ_w = np.tile(XYZ_w, (6, 1))
        XYZ_wr = np.tile(XYZ_wr, (6, 1))
        XYZ_a = np.tile(XYZ_a, (6, 1))
        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(XYZ, XYZ_w, XYZ_wr),
            XYZ_a,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.reshape(XYZ, (2, 3, 3))
        XYZ_w = np.reshape(XYZ_w, (2, 3, 3))
        XYZ_wr = np.reshape(XYZ_wr, (2, 3, 3))
        XYZ_a = np.reshape(XYZ_a, (2, 3, 3))
        np.testing.assert_allclose(
            chromatic_adaptation_VonKries(XYZ, XYZ_w, XYZ_wr),
            XYZ_a,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.chromatic_adaptation_VonKries`
        definition domain and range scale support.
        """

        XYZ = np.array([0.20654008, 0.12197225, 0.05136952])
        XYZ_w = np.array([0.95045593, 1.00000000, 1.08905775])
        XYZ_wr = np.array([0.96429568, 1.00000000, 0.82510460])
        XYZ_a = chromatic_adaptation_VonKries(XYZ, XYZ_w, XYZ_wr)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    chromatic_adaptation_VonKries(
                        XYZ * factor, XYZ_w * factor, XYZ_wr * factor
                    ),
                    XYZ_a * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_chromatic_adaptation_VonKries(self) -> None:
        """
        Test :func:`colour.adaptation.vonkries.chromatic_adaptation_VonKries`
        definition nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=3))))
        chromatic_adaptation_VonKries(cases, cases, cases)
