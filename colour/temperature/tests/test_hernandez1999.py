"""Define the unit tests for the :mod:`colour.temperature.hernandez1999` module."""

from __future__ import annotations

from itertools import product

import numpy as np

from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.temperature import CCT_to_xy_Hernandez1999, xy_to_CCT_Hernandez1999
from colour.utilities import ignore_numpy_errors

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "Testxy_to_CCT_Hernandez1999",
    "TestCCT_to_xy_Hernandez1999",
]


class Testxy_to_CCT_Hernandez1999:
    """
    Define :func:`colour.temperature.hernandez1999.xy_to_CCT_Hernandez1999`
    definition unit tests methods.
    """

    def test_xy_to_CCT_Hernandez1999(self) -> None:
        """
        Test :func:`colour.temperature.hernandez1999.xy_to_CCT_McCamy1992`
        definition.
        """

        np.testing.assert_allclose(
            xy_to_CCT_Hernandez1999(np.array([0.31270, 0.32900])),
            6500.74204318,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            xy_to_CCT_Hernandez1999(np.array([0.44757, 0.40745])),
            2790.64222533,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            xy_to_CCT_Hernandez1999(np.array([0.244162248213914, 0.240333674758318])),
            64448.11092565,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_xy_to_CCT_Hernandez1999(self) -> None:
        """
        Test :func:`colour.temperature.hernandez1999.xy_to_CCT_Hernandez1999`
        definition n-dimensional arrays support.
        """

        xy = np.array([0.31270, 0.32900])
        CCT = xy_to_CCT_Hernandez1999(xy)

        xy = np.tile(xy, (6, 1))
        CCT = np.tile(CCT, 6)
        np.testing.assert_allclose(
            xy_to_CCT_Hernandez1999(xy), CCT, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        xy = np.reshape(xy, (2, 3, 2))
        CCT = np.reshape(CCT, (2, 3))
        np.testing.assert_allclose(
            xy_to_CCT_Hernandez1999(xy), CCT, atol=TOLERANCE_ABSOLUTE_TESTS
        )

    @ignore_numpy_errors
    def test_nan_xy_to_CCT_Hernandez1999(self) -> None:
        """
        Test :func:`colour.temperature.hernandez1999.xy_to_CCT_Hernandez1999`
        definition nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=2))))
        xy_to_CCT_Hernandez1999(cases)


class TestCCT_to_xy_Hernandez1999:
    """
    Define :func:`colour.temperature.hernandez1999.CCT_to_xy_Hernandez1999`
    definition unit tests methods.
    """

    def test_CCT_to_xy_Hernandez1999(self) -> None:
        """
        Test :func:`colour.temperature.hernandez1999.CCT_to_xy_Hernandez1999`
        definition.
        """

        np.testing.assert_allclose(
            CCT_to_xy_Hernandez1999(6500.74204318, {"method": "Nelder-Mead"}),
            np.array([0.31269943, 0.32900373]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            CCT_to_xy_Hernandez1999(2790.64222533, {"method": "Nelder-Mead"}),
            np.array([0.42864308, 0.36754776]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            CCT_to_xy_Hernandez1999(64448.11092565, {"method": "Nelder-Mead"}),
            np.array([0.08269106, 0.36612620]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_CCT_to_xy_Hernandez1999(self) -> None:
        """
        Test :func:`colour.temperature.hernandez1999.CCT_to_xy_Hernandez1999`
        definition n-dimensional arrays support.
        """

        CCT = 6500.74204318
        xy = CCT_to_xy_Hernandez1999(CCT)

        CCT = np.tile(CCT, 6)
        xy = np.tile(xy, (6, 1))
        np.testing.assert_allclose(
            CCT_to_xy_Hernandez1999(CCT), xy, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        CCT = np.reshape(CCT, (2, 3))
        xy = np.reshape(xy, (2, 3, 2))
        np.testing.assert_allclose(
            CCT_to_xy_Hernandez1999(CCT), xy, atol=TOLERANCE_ABSOLUTE_TESTS
        )

    @ignore_numpy_errors
    def test_nan_CCT_to_xy_Hernandez1999(self) -> None:
        """
        Test :func:`colour.temperature.hernandez1999.CCT_to_xy_Hernandez1999`
        definition nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=2))))
        CCT_to_xy_Hernandez1999(cases)
