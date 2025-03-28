"""Define the unit tests for the :mod:`colour.volume.pointer_gamut` module."""

from __future__ import annotations

from itertools import product

import numpy as np

from colour.utilities import ignore_numpy_errors
from colour.volume import is_within_pointer_gamut

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestIsWithinPointerGamut",
]


class TestIsWithinPointerGamut:
    """
    Define :func:`colour.volume.pointer_gamut.is_within_pointer_gamut`
    definition unit tests methods.
    """

    def test_is_within_pointer_gamut(self) -> None:
        """
        Test :func:`colour.volume.pointer_gamut.is_within_pointer_gamut`
        definition.
        """

        assert is_within_pointer_gamut(np.array([0.3205, 0.4131, 0.5100]))

        assert not is_within_pointer_gamut(np.array([0.0005, 0.0031, 0.0010]))

        assert is_within_pointer_gamut(np.array([0.4325, 0.3788, 0.1034]))

        assert not is_within_pointer_gamut(np.array([0.0025, 0.0088, 0.0340]))

    def test_n_dimensional_is_within_pointer_gamut(self) -> None:
        """
        Test :func:`colour.volume.pointer_gamut.is_within_pointer_gamut`
        definition n-dimensional arrays support.
        """

        a = np.array([0.3205, 0.4131, 0.5100])
        b = is_within_pointer_gamut(a)

        a = np.tile(a, (6, 1))
        b = np.tile(b, 6)
        np.testing.assert_allclose(is_within_pointer_gamut(a), b)

        a = np.reshape(a, (2, 3, 3))
        b = np.reshape(b, (2, 3))
        np.testing.assert_allclose(is_within_pointer_gamut(a), b)

    @ignore_numpy_errors
    def test_nan_is_within_pointer_gamut(self) -> None:
        """
        Test :func:`colour.volume.pointer_gamut.is_within_pointer_gamut`
        definition nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=3))))
        is_within_pointer_gamut(cases)
