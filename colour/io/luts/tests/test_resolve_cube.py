"""Define the unit tests for the :mod:`colour.io.luts.resolve_cube` module."""

from __future__ import annotations

import os
import shutil
import tempfile

import numpy as np
import pytest

from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.hints import cast
from colour.io import (
    LUT1D,
    LUT3D,
    LUT3x1D,
    LUTSequence,
    read_LUT_ResolveCube,
    write_LUT_ResolveCube,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "ROOT_LUTS",
    "TestReadLUTResolveCube",
    "TestWriteLUTResolveCube",
]

ROOT_LUTS: str = os.path.join(os.path.dirname(__file__), "resources", "resolve_cube")


class TestReadLUTResolveCube:
    """
    Define :func:`colour.io.luts.resolve_cube.read_LUT_ResolveCube` definition
    unit tests methods.
    """

    def test_read_LUT_ResolveCube(self) -> None:
        """
        Test :func:`colour.io.luts.resolve_cube.read_LUT_ResolveCube`
        definition.
        """

        LUT_1 = cast(
            LUT3x1D,
            read_LUT_ResolveCube(os.path.join(ROOT_LUTS, "ACES_Proxy_10_to_ACES.cube")),
        )

        np.testing.assert_allclose(
            LUT_1.table,
            np.array(
                [
                    [4.88300000e-04, 4.88300000e-04, 4.88300000e-04],
                    [7.71400000e-04, 7.71400000e-04, 7.71400000e-04],
                    [1.21900000e-03, 1.21900000e-03, 1.21900000e-03],
                    [1.92600000e-03, 1.92600000e-03, 1.92600000e-03],
                    [3.04400000e-03, 3.04400000e-03, 3.04400000e-03],
                    [4.80900000e-03, 4.80900000e-03, 4.80900000e-03],
                    [7.59900000e-03, 7.59900000e-03, 7.59900000e-03],
                    [1.20100000e-02, 1.20100000e-02, 1.20100000e-02],
                    [1.89700000e-02, 1.89700000e-02, 1.89700000e-02],
                    [2.99800000e-02, 2.99800000e-02, 2.99800000e-02],
                    [4.73700000e-02, 4.73700000e-02, 4.73700000e-02],
                    [7.48400000e-02, 7.48400000e-02, 7.48400000e-02],
                    [1.18300000e-01, 1.18300000e-01, 1.18300000e-01],
                    [1.86900000e-01, 1.86900000e-01, 1.86900000e-01],
                    [2.95200000e-01, 2.95200000e-01, 2.95200000e-01],
                    [4.66500000e-01, 4.66500000e-01, 4.66500000e-01],
                    [7.37100000e-01, 7.37100000e-01, 7.37100000e-01],
                    [1.16500000e00, 1.16500000e00, 1.16500000e00],
                    [1.84000000e00, 1.84000000e00, 1.84000000e00],
                    [2.90800000e00, 2.90800000e00, 2.90800000e00],
                    [4.59500000e00, 4.59500000e00, 4.59500000e00],
                    [7.26000000e00, 7.26000000e00, 7.26000000e00],
                    [1.14700000e01, 1.14700000e01, 1.14700000e01],
                    [1.81300000e01, 1.81300000e01, 1.81300000e01],
                    [2.86400000e01, 2.86400000e01, 2.86400000e01],
                    [4.52500000e01, 4.52500000e01, 4.52500000e01],
                    [7.15100000e01, 7.15100000e01, 7.15100000e01],
                    [1.13000000e02, 1.13000000e02, 1.13000000e02],
                    [1.78500000e02, 1.78500000e02, 1.78500000e02],
                    [2.82100000e02, 2.82100000e02, 2.82100000e02],
                    [4.45700000e02, 4.45700000e02, 4.45700000e02],
                    [7.04300000e02, 7.04300000e02, 7.04300000e02],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        assert LUT_1.name == "ACES Proxy 10 to ACES"
        assert LUT_1.dimensions == 2
        np.testing.assert_array_equal(LUT_1.domain, np.array([[0, 0, 0], [1, 1, 1]]))
        assert LUT_1.size == 32
        assert LUT_1.comments == []

        LUT_2 = cast(
            LUT3x1D, read_LUT_ResolveCube(os.path.join(ROOT_LUTS, "Demo.cube"))
        )
        assert LUT_2.comments == ["Comments can't go anywhere"]
        np.testing.assert_array_equal(LUT_2.domain, np.array([[0, 0, 0], [3, 3, 3]]))

        LUT_3 = cast(
            LUT3D,
            read_LUT_ResolveCube(
                os.path.join(ROOT_LUTS, "Three_Dimensional_Table.cube")
            ),
        )
        assert LUT_3.dimensions == 3
        assert LUT_3.size == 2

        LUT_4 = cast(
            LUTSequence,
            read_LUT_ResolveCube(os.path.join(ROOT_LUTS, "LogC_Video.cube")),
        )
        np.testing.assert_allclose(
            LUT_4[0].table,
            np.array(
                [
                    [0.00000000, 0.00000000, 0.00000000],
                    [0.02708500, 0.02708500, 0.02708500],
                    [0.06304900, 0.06304900, 0.06304900],
                    [0.11314900, 0.11314900, 0.11314900],
                    [0.18304900, 0.18304900, 0.18304900],
                    [0.28981100, 0.28981100, 0.28981100],
                    [0.41735300, 0.41735300, 0.41735300],
                    [0.54523100, 0.54523100, 0.54523100],
                    [0.67020500, 0.67020500, 0.67020500],
                    [0.78963000, 0.78963000, 0.78963000],
                    [0.88646800, 0.88646800, 0.88646800],
                    [0.94549100, 0.94549100, 0.94549100],
                    [0.97644900, 0.97644900, 0.97644900],
                    [0.98924800, 0.98924800, 0.98924800],
                    [0.99379700, 0.99379700, 0.99379700],
                    [1.00000000, 1.00000000, 1.00000000],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        assert LUT_4[1].size == 4


class TestWriteLUTResolveCube:
    """
    Define :func:`colour.io.luts.resolve_cube.write_LUT_ResolveCube`
    definition unit tests methods.
    """

    def setup_method(self) -> None:
        """Initialise the common tests attributes."""

        self._temporary_directory = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        """After tests actions."""

        shutil.rmtree(self._temporary_directory)

    def test_write_LUT_ResolveCube(self) -> None:
        """
        Test :func:`colour.io.luts.resolve_cube.write_LUT_ResolveCube`
        definition.
        """

        LUT_1_r = read_LUT_ResolveCube(
            os.path.join(ROOT_LUTS, "ACES_Proxy_10_to_ACES.cube")
        )

        write_LUT_ResolveCube(
            LUT_1_r,
            os.path.join(self._temporary_directory, "ACES_Proxy_10_to_ACES.cube"),
        )

        LUT_1_t = read_LUT_ResolveCube(
            os.path.join(self._temporary_directory, "ACES_Proxy_10_to_ACES.cube")
        )

        assert LUT_1_r == LUT_1_t

        LUT_2_r = cast(
            LUT3x1D, read_LUT_ResolveCube(os.path.join(ROOT_LUTS, "Demo.cube"))
        )

        write_LUT_ResolveCube(
            LUT_2_r, os.path.join(self._temporary_directory, "Demo.cube")
        )

        LUT_2_t = cast(
            LUT3x1D,
            read_LUT_ResolveCube(os.path.join(self._temporary_directory, "Demo.cube")),
        )

        assert LUT_2_r == LUT_2_t
        assert LUT_2_r.comments == LUT_2_t.comments

        LUT_3_r = cast(
            LUT3D,
            read_LUT_ResolveCube(
                os.path.join(ROOT_LUTS, "Three_Dimensional_Table.cube")
            ),
        )

        write_LUT_ResolveCube(
            LUT_3_r,
            os.path.join(self._temporary_directory, "Three_Dimensional_Table.cube"),
        )

        LUT_3_t = cast(
            LUT3D,
            read_LUT_ResolveCube(
                os.path.join(self._temporary_directory, "Three_Dimensional_Table.cube")
            ),
        )
        assert LUT_3_r == LUT_3_t

        LUT_4_r = cast(
            LUTSequence,
            read_LUT_ResolveCube(
                os.path.join(ROOT_LUTS, "Three_Dimensional_Table_With_Shaper.cube")
            ),
        )

        LUT_4_r.sequence[0] = LUT_4_r.sequence[0].convert(  # pyright: ignore
            LUT1D, force_conversion=True
        )

        write_LUT_ResolveCube(
            LUT_4_r,
            os.path.join(
                self._temporary_directory,
                "Three_Dimensional_Table_With_Shaper.cube",
            ),
        )

        LUT_4_t = cast(
            LUTSequence,
            read_LUT_ResolveCube(
                os.path.join(
                    self._temporary_directory,
                    "Three_Dimensional_Table_With_Shaper.cube",
                )
            ),
        )

        LUT_4_r = cast(
            LUTSequence,
            read_LUT_ResolveCube(
                os.path.join(ROOT_LUTS, "Three_Dimensional_Table_With_Shaper.cube")
            ),
        )

        assert LUT_4_r == LUT_4_t

        LUT_5_r = cast(
            LUT3x1D,
            read_LUT_ResolveCube(os.path.join(ROOT_LUTS, "ACES_Proxy_10_to_ACES.cube")),
        )

        write_LUT_ResolveCube(
            cast(LUT1D, LUT_5_r.convert(LUT1D, force_conversion=True)),
            os.path.join(self._temporary_directory, "ACES_Proxy_10_to_ACES.cube"),
        )

        LUT_5_t = cast(
            LUT3x1D,
            read_LUT_ResolveCube(
                os.path.join(self._temporary_directory, "ACES_Proxy_10_to_ACES.cube")
            ),
        )

        assert LUT_5_r == LUT_5_t

    def test_raise_exception_write_LUT_ResolveCube(self) -> None:
        """
        Test :func:`colour.io.luts.resolve_cube.write_LUT_ResolveCube`
        definition raised exception.
        """

        pytest.raises(TypeError, write_LUT_ResolveCube, object(), "")
