"""
Define the unit tests for the
:mod:`colour.models.rgb.transfer_functions.common` module.
"""

import numpy as np
import pytest

from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.models.rgb.transfer_functions import (
    CCTF_DECODINGS,
    CCTF_ENCODINGS,
    EOTF_INVERSES,
    EOTFS,
    LOG_DECODINGS,
    LOG_ENCODINGS,
    OETF_INVERSES,
    OETFS,
    OOTF_INVERSES,
    OOTFS,
    cctf_decoding,
    cctf_encoding,
)
from colour.utilities import ColourUsageWarning

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Development"

__all__ = [
    "TestCctfEncoding",
    "TestCctfDecoding",
    "TestTransferFunctions",
]


class TestCctfEncoding:
    """
    Define :func:`colour.models.rgb.transfer_functions.cctf_encoding`
    definition unit tests methods.
    """

    def test_raise_exception_cctf_encoding(self) -> None:
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy` definition raised exception.
        """

        pytest.warns(
            ColourUsageWarning,
            cctf_encoding,
            0.18,
            function="ITU-R BT.2100 HLG",
        )
        pytest.warns(
            ColourUsageWarning,
            cctf_encoding,
            0.18,
            function="ITU-R BT.2100 PQ",
        )


class TestCctfDecoding:
    """
    Define :func:`colour.models.rgb.transfer_functions.cctf_decoding`
    definition unit tests methods.
    """

    def test_raise_exception_cctf_decoding(self) -> None:
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy` definition raised exception.
        """

        pytest.warns(
            ColourUsageWarning,
            cctf_decoding,
            0.18,
            function="ITU-R BT.2100 HLG",
        )
        pytest.warns(
            ColourUsageWarning,
            cctf_decoding,
            0.18,
            function="ITU-R BT.2100 PQ",
        )


class TestTransferFunctions:
    """Define the transfer functions unit tests methods."""

    def test_transfer_functions(self) -> None:
        """Test the transfer functions reciprocity."""

        ignored_transfer_functions = (
            "ACESproxy",
            "DICOM GSDF",
            "Filmic Pro 6",
        )

        tolerance = {"D-Log": 0.1, "F-Log": 5e-4, "L-Log": 5e-4, "N-Log": 5e-3}

        reciprocal_mappings = [
            (LOG_ENCODINGS, LOG_DECODINGS),
            (OETFS, OETF_INVERSES),
            (EOTFS, EOTF_INVERSES),
            (CCTF_ENCODINGS, CCTF_DECODINGS),
            (OOTFS, OOTF_INVERSES),
        ]

        samples = np.hstack(
            [np.linspace(0, 1, int(1e5)), np.linspace(0, 65504, 65504 * 10)]
        )

        for encoding_mapping, _decoding_mapping in reciprocal_mappings:
            for name in encoding_mapping:
                if name in ignored_transfer_functions:
                    continue

                samples_r = np.copy(samples)

                if name == "ITU-T H.273 Log":
                    samples_r = np.clip(samples_r, 0.1, np.inf)

                if name == "ITU-T H.273 Log Sqrt":
                    samples_r = np.clip(samples_r, np.sqrt(10) / 1000, np.inf)

                samples_e = CCTF_ENCODINGS[name](samples_r)
                samples_d = CCTF_DECODINGS[name](samples_e)

                np.testing.assert_allclose(
                    samples_r,
                    samples_d,
                    atol=tolerance.get(name, TOLERANCE_ABSOLUTE_TESTS),
                )
