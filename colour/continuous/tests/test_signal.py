"""Define the unit tests for the :mod:`colour.continuous.signal` module."""

from __future__ import annotations

import pickle
import textwrap

import numpy as np
import pytest

from colour.algebra import CubicSplineInterpolator, Extrapolator, KernelInterpolator
from colour.constants import DTYPE_FLOAT_DEFAULT, TOLERANCE_ABSOLUTE_TESTS
from colour.continuous import Signal
from colour.utilities import ColourRuntimeWarning, attest, is_pandas_installed

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestSignal",
]


class TestSignal:
    """Define :class:`colour.continuous.signal.Signal` class unit tests methods."""

    def setup_method(self) -> None:
        """Initialise the common tests attributes."""

        self._range = np.linspace(10, 100, 10)
        self._domain = np.arange(100, 1100, 100)

        self._signal = Signal(self._range)

    def test_required_attributes(self) -> None:
        """Test the presence of required attributes."""

        required_attributes = (
            "dtype",
            "domain",
            "range",
            "interpolator",
            "interpolator_kwargs",
            "extrapolator",
            "extrapolator_kwargs",
            "function",
        )

        for attribute in required_attributes:
            assert attribute in dir(Signal)

    def test_required_methods(self) -> None:
        """Test the presence of required methods."""

        required_methods = (
            "__init__",
            "__str__",
            "__repr__",
            "__hash__",
            "__getitem__",
            "__setitem__",
            "__contains__",
            "__iter__",
            "__eq__",
            "__ne__",
            "arithmetical_operation",
            "signal_unpack_data",
            "fill_nan",
            "domain_distance",
            "to_series",
        )

        for method in required_methods:
            assert method in dir(Signal)

    def test_pickling(self) -> None:
        """
        Test whether the :class:``colour.continuous.signal.Signal` class can be
        pickled.
        """

        data = pickle.dumps(self._signal)
        data = pickle.loads(data)  # noqa: S301
        assert self._signal == data

    def test_dtype(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.dtype` property."""

        assert self._signal.dtype == DTYPE_FLOAT_DEFAULT

        signal = self._signal.copy()
        signal.dtype = np.float32
        assert signal.dtype == np.float32

    def test_domain(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.domain` property."""

        signal = self._signal.copy()

        np.testing.assert_allclose(
            signal[np.array([0, 1, 2])],
            np.array([10.0, 20.0, 30.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal.domain = np.arange(0, 10, 1) * 10

        np.testing.assert_array_equal(signal.domain, np.arange(0, 10, 1) * 10)

        np.testing.assert_allclose(
            signal[np.array([0, 1, 2]) * 10],
            np.array([10.0, 20.0, 30.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        domain = np.linspace(0, 1, 10)
        domain[0] = -np.inf

        def assert_warns() -> None:
            """Help to test the runtime warning."""

            signal.domain = domain

        pytest.warns(ColourRuntimeWarning, assert_warns)

    def test_range(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.range` property."""

        signal = self._signal.copy()

        np.testing.assert_allclose(
            signal[np.array([0, 1, 2])],
            np.array([10.0, 20.0, 30.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal.range = self._range * 10

        np.testing.assert_array_equal(signal.range, self._range * 10)

        np.testing.assert_allclose(
            signal[np.array([0, 1, 2])],
            np.array([10.0, 20.0, 30.0]) * 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        def assert_warns() -> None:
            """Help to test the runtime warning."""

            signal.range = self._range * np.inf

        pytest.warns(ColourRuntimeWarning, assert_warns)

    def test_interpolator(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.interpolator` property."""

        signal = self._signal.copy()

        np.testing.assert_allclose(
            signal[np.linspace(0, 5, 5)],
            np.array(
                [
                    10.00000000,
                    22.83489024,
                    34.80044921,
                    47.55353925,
                    60.00000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal.interpolator = CubicSplineInterpolator

        np.testing.assert_allclose(
            signal[np.linspace(0, 5, 5)],
            np.array([10.0, 22.5, 35.0, 47.5, 60.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_interpolator_kwargs(self) -> None:
        """
        Test :func:`colour.continuous.signal.Signal.interpolator_kwargs`
        property.
        """

        signal = self._signal.copy()

        np.testing.assert_allclose(
            signal[np.linspace(0, 5, 5)],
            np.array(
                [
                    10.00000000,
                    22.83489024,
                    34.80044921,
                    47.55353925,
                    60.00000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal.interpolator_kwargs = {"window": 1, "kernel_kwargs": {"a": 1}}

        np.testing.assert_allclose(
            signal[np.linspace(0, 5, 5)],
            np.array(
                [
                    10.00000000,
                    18.91328761,
                    28.36993142,
                    44.13100443,
                    60.00000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_extrapolator(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.extrapolator` property."""

        assert isinstance(self._signal.extrapolator(), Extrapolator)

    def test_extrapolator_kwargs(self) -> None:
        """
        Test :func:`colour.continuous.signal.Signal.extrapolator_kwargs`
        property.
        """

        signal = self._signal.copy()

        attest(np.all(np.isnan(signal[np.array([-1000, 1000])])))

        signal.extrapolator_kwargs = {
            "method": "Linear",
        }

        np.testing.assert_allclose(
            signal[np.array([-1000, 1000])],
            np.array([-9990.0, 10010.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_function(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.function` property."""

        attest(callable(self._signal.function))

    def test_raise_exception_function(self) -> None:
        """
        Test :func:`colour.continuous.signal.Signal.function` property raised
        exception.
        """

        pytest.raises(ValueError, Signal().function, 0)

    def test__init__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__init__` method."""

        signal = Signal(self._range)
        np.testing.assert_array_equal(signal.domain, np.arange(0, 10, 1))
        np.testing.assert_array_equal(signal.range, self._range)

        signal = Signal(self._range, self._domain)
        np.testing.assert_array_equal(signal.domain, self._domain)
        np.testing.assert_array_equal(signal.range, self._range)

        signal = Signal(dict(zip(self._domain, self._range, strict=True)))
        np.testing.assert_array_equal(signal.domain, self._domain)
        np.testing.assert_array_equal(signal.range, self._range)

        signal = Signal(signal)
        np.testing.assert_array_equal(signal.domain, self._domain)
        np.testing.assert_array_equal(signal.range, self._range)

        if is_pandas_installed():
            from pandas import Series

            signal = Signal(Series(dict(zip(self._domain, self._range, strict=True))))
            np.testing.assert_array_equal(signal.domain, self._domain)
            np.testing.assert_array_equal(signal.range, self._range)

    def test__hash__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__hash__` method."""

        assert isinstance(hash(self._signal), int)

    def test__str__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__str__` method."""

        assert (
            str(self._signal)
            == (
                textwrap.dedent(
                    """
                [[   0.   10.]
                 [   1.   20.]
                 [   2.   30.]
                 [   3.   40.]
                 [   4.   50.]
                 [   5.   60.]
                 [   6.   70.]
                 [   7.   80.]
                 [   8.   90.]
                 [   9.  100.]]"""
                )[1:]
            )
        )

        assert isinstance(str(Signal()), str)

    def test__repr__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__repr__` method."""

        assert repr(self._signal) == (
            textwrap.dedent(
                """
                Signal([[   0.,   10.],
                        [   1.,   20.],
                        [   2.,   30.],
                        [   3.,   40.],
                        [   4.,   50.],
                        [   5.,   60.],
                        [   6.,   70.],
                        [   7.,   80.],
                        [   8.,   90.],
                        [   9.,  100.]],
                       KernelInterpolator,
                       {},
                       Extrapolator,
                       {'method': 'Constant', 'left': nan, 'right': nan})
                """
            ).strip()
        )

        assert isinstance(repr(Signal()), str)

    def test__getitem__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__getitem__` method."""

        assert self._signal[0] == 10.0

        np.testing.assert_allclose(
            self._signal[np.array([0, 1, 2])],
            np.array([10.0, 20.0, 30.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            self._signal[np.linspace(0, 5, 5)],
            np.array(
                [
                    10.00000000,
                    22.83489024,
                    34.80044921,
                    47.55353925,
                    60.00000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        attest(np.all(np.isnan(self._signal[np.array([-1000, 1000])])))

        signal = self._signal.copy()
        signal.extrapolator_kwargs = {
            "method": "Linear",
        }
        np.testing.assert_array_equal(
            signal[np.array([-1000, 1000])], np.array([-9990.0, 10010.0])
        )

        signal.extrapolator_kwargs = {
            "method": "Constant",
            "left": 0,
            "right": 1,
        }
        np.testing.assert_array_equal(
            signal[np.array([-1000, 1000])], np.array([0.0, 1.0])
        )

    def test__setitem__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__setitem__` method."""

        signal = self._signal.copy()

        signal[0] = 20
        np.testing.assert_allclose(
            signal.range,
            np.array([20.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]),
        )

        signal[np.array([0, 1, 2])] = 30
        np.testing.assert_allclose(
            signal.range,
            np.array([30.0, 30.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal[0:3] = 40
        np.testing.assert_allclose(
            signal.range,
            np.array([40.0, 40.0, 40.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal[np.linspace(0, 5, 5)] = 50
        np.testing.assert_allclose(
            signal.domain,
            np.array(
                [
                    0.00,
                    1.00,
                    1.25,
                    2.00,
                    2.50,
                    3.00,
                    3.75,
                    4.00,
                    5.00,
                    6.00,
                    7.00,
                    8.00,
                    9.00,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        np.testing.assert_allclose(
            signal.range,
            np.array(
                [
                    50.0,
                    40.0,
                    50.0,
                    40.0,
                    50.0,
                    40.0,
                    50.0,
                    50.0,
                    50.0,
                    70.0,
                    80.0,
                    90.0,
                    100.0,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal[np.array([0, 1, 2])] = np.array([10, 20, 30])
        np.testing.assert_allclose(
            signal.range,
            np.array(
                [
                    10.0,
                    20.0,
                    50.0,
                    30.0,
                    50.0,
                    40.0,
                    50.0,
                    50.0,
                    50.0,
                    70.0,
                    80.0,
                    90.0,
                    100.0,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test__contains__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__contains__` method."""

        assert 0 in self._signal
        assert 0.5 in self._signal
        assert 1000 not in self._signal

    def test__iter__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__iter__` method."""

        domain = np.arange(0, 10)
        for i, (domain_value, range_value) in enumerate(self._signal):
            np.testing.assert_array_equal(domain_value, domain[i])
            np.testing.assert_array_equal(range_value, self._range[i])

    def test__len__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__len__` method."""

        assert len(self._signal) == 10

    def test__eq__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__eq__` method."""

        signal_1 = self._signal.copy()
        signal_2 = self._signal.copy()

        assert signal_1 == signal_2

    def test__ne__(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.__ne__` method."""

        signal_1 = self._signal.copy()
        signal_2 = self._signal.copy()

        signal_2[0] = 20
        assert signal_1 != signal_2

        signal_2[0] = 10
        assert signal_1 == signal_2

        signal_2.interpolator = CubicSplineInterpolator
        assert signal_1 != signal_2

        signal_2.interpolator = KernelInterpolator
        assert signal_1 == signal_2

        signal_2.interpolator_kwargs = {"window": 1}
        assert signal_1 != signal_2

        signal_2.interpolator_kwargs = {}
        assert signal_1 == signal_2

        class NotExtrapolator(Extrapolator):
            """Not :class:`Extrapolator` class."""

        signal_2.extrapolator = NotExtrapolator
        assert signal_1 != signal_2

        signal_2.extrapolator = Extrapolator
        assert signal_1 == signal_2

        signal_2.extrapolator_kwargs = {}
        assert signal_1 != signal_2

        signal_2.extrapolator_kwargs = {
            "method": "Constant",
            "left": np.nan,
            "right": np.nan,
        }
        assert signal_1 == signal_2

    def test_arithmetical_operation(self) -> None:
        """
        Test :meth:`colour.continuous.signal.Signal.arithmetical_operation`
        method.
        """

        np.testing.assert_allclose(
            self._signal.arithmetical_operation(10, "+", False).range,
            self._range + 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            self._signal.arithmetical_operation(10, "-", False).range,
            self._range - 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            self._signal.arithmetical_operation(10, "*", False).range,
            self._range * 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            self._signal.arithmetical_operation(10, "/", False).range,
            self._range / 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            self._signal.arithmetical_operation(10, "**", False).range,
            self._range**10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            (self._signal + 10).range,
            self._range + 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            (self._signal - 10).range,
            self._range - 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            (self._signal * 10).range,
            self._range * 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            (self._signal / 10).range,
            self._range / 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            (self._signal**10).range,
            self._range**10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal = self._signal.copy()

        np.testing.assert_allclose(
            signal.arithmetical_operation(10, "+", True).range,
            self._range + 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            signal.arithmetical_operation(10, "-", True).range,
            self._range,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            signal.arithmetical_operation(10, "*", True).range,
            self._range * 10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            signal.arithmetical_operation(10, "/", True).range,
            self._range,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            signal.arithmetical_operation(10, "**", True).range,
            self._range**10,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal = self._signal.copy()

        np.testing.assert_allclose(
            signal.arithmetical_operation(self._range, "+", False).range,
            signal.range + self._range,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            signal.arithmetical_operation(signal, "+", False).range,
            signal.range + signal.range,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_is_uniform(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.is_uniform` method."""

        assert self._signal.is_uniform()

        signal = self._signal.copy()
        signal[0.5] = 1.0
        assert not signal.is_uniform()

    def test_copy(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.copy` method."""

        assert self._signal is not self._signal.copy()
        assert self._signal == self._signal.copy()

    def test_signal_unpack_data(self) -> None:
        """
        Test :meth:`colour.continuous.signal.Signal.signal_unpack_data`
        method.
        """

        domain, range_ = Signal.signal_unpack_data(self._range)
        np.testing.assert_array_equal(range_, self._range)
        np.testing.assert_array_equal(domain, np.arange(0, 10, 1))

        domain, range_ = Signal.signal_unpack_data(self._range, self._domain)
        np.testing.assert_array_equal(range_, self._range)
        np.testing.assert_array_equal(domain, self._domain)

        domain, range_ = Signal.signal_unpack_data(
            self._range, dict(zip(self._domain, self._range, strict=True)).keys()
        )
        np.testing.assert_array_equal(domain, self._domain)

        domain, range_ = Signal.signal_unpack_data(
            dict(zip(self._domain, self._range, strict=True))
        )
        np.testing.assert_array_equal(range_, self._range)
        np.testing.assert_array_equal(domain, self._domain)

        domain, range_ = Signal.signal_unpack_data(Signal(self._range, self._domain))
        np.testing.assert_array_equal(range_, self._range)
        np.testing.assert_array_equal(domain, self._domain)

        if is_pandas_installed():
            from pandas import Series

            domain, range_ = Signal.signal_unpack_data(
                Series(dict(zip(self._domain, self._range, strict=True)))
            )
            np.testing.assert_array_equal(range_, self._range)
            np.testing.assert_array_equal(domain, self._domain)

    def test_fill_nan(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.fill_nan` method."""

        signal = self._signal.copy()

        signal[3:7] = np.nan

        np.testing.assert_allclose(
            signal.fill_nan().range,
            np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        signal[3:7] = np.nan

        np.testing.assert_allclose(
            signal.fill_nan(method="Constant").range,
            np.array([10.0, 20.0, 30.0, 0.0, 0.0, 0.0, 0.0, 80.0, 90.0, 100.0]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_distance(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.domain_distance` method."""

        np.testing.assert_allclose(
            self._signal.domain_distance(0.5),
            0.5,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            self._signal.domain_distance(np.linspace(0, 9, 10) + 0.5),
            np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_to_series(self) -> None:
        """Test :func:`colour.continuous.signal.Signal.to_series` method."""

        if is_pandas_installed():
            from pandas import Series

            assert (
                Signal(self._range, self._domain).to_series().all()
                == Series(dict(zip(self._domain, self._range, strict=True))).all()
            )
