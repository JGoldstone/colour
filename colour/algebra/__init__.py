# isort: skip_file

from __future__ import annotations

import sys

from colour.utilities.deprecation import ModuleAPI, build_API_changes
from colour.utilities.documentation import is_documentation_building

import typing

if typing.TYPE_CHECKING:
    from colour.hints import Any

from .common import (
    get_sdiv_mode,
    set_sdiv_mode,
    sdiv_mode,
    sdiv,
    is_spow_enabled,
    set_spow_enable,
    spow_enable,
    spow,
    normalise_vector,
    normalise_maximum,
    vecmul,
    euclidean_distance,
    manhattan_distance,
    linear_conversion,
    linstep_function,
    lerp,
    smoothstep_function,
    smooth,
    is_identity,
    eigen_decomposition,
)
from .coordinates import *  # noqa: F403
from . import coordinates
from .interpolation import (
    kernel_nearest_neighbour,
    kernel_linear,
    kernel_sinc,
    kernel_lanczos,
    kernel_cardinal_spline,
    KernelInterpolator,
    NearestNeighbourInterpolator,
    LinearInterpolator,
    SpragueInterpolator,
    CubicSplineInterpolator,
    PchipInterpolator,
    NullInterpolator,
    lagrange_coefficients,
    table_interpolation_trilinear,
    table_interpolation_tetrahedral,
    TABLE_INTERPOLATION_METHODS,
    table_interpolation,
)
from .extrapolation import Extrapolator
from .prng import random_triplet_generator
from .regression import least_square_mapping_MoorePenrose

__all__ = []
__all__ += [
    "get_sdiv_mode",
    "set_sdiv_mode",
    "sdiv_mode",
    "sdiv",
    "is_spow_enabled",
    "set_spow_enable",
    "spow_enable",
    "spow",
    "normalise_vector",
    "normalise_maximum",
    "vecmul",
    "euclidean_distance",
    "manhattan_distance",
    "linear_conversion",
    "linstep_function",
    "lerp",
    "smoothstep_function",
    "smooth",
    "is_identity",
    "eigen_decomposition",
]
__all__ += coordinates.__all__
__all__ += [
    "kernel_nearest_neighbour",
    "kernel_linear",
    "kernel_sinc",
    "kernel_lanczos",
    "kernel_cardinal_spline",
    "KernelInterpolator",
    "NearestNeighbourInterpolator",
    "LinearInterpolator",
    "SpragueInterpolator",
    "CubicSplineInterpolator",
    "PchipInterpolator",
    "NullInterpolator",
    "lagrange_coefficients",
    "table_interpolation_trilinear",
    "table_interpolation_tetrahedral",
    "TABLE_INTERPOLATION_METHODS",
    "table_interpolation",
]
__all__ += [
    "Extrapolator",
]
__all__ += [
    "random_triplet_generator",
]
__all__ += [
    "least_square_mapping_MoorePenrose",
]


# ----------------------------------------------------------------------------#
# ---                API Changes and Deprecation Management                ---#
# ----------------------------------------------------------------------------#
class algebra(ModuleAPI):
    """Define a class acting like the *algebra* module."""

    def __getattr__(self, attribute: str) -> Any:
        """Return the value from the attribute with given name."""

        return super().__getattr__(attribute)


# v0.4.5
API_CHANGES: dict = {
    "ObjectRenamed": [
        [
            "colour.algebra.vector_dot",
            "colour.algebra.vecmul",
        ],
    ]
}
"""Defines the *colour.algebra* sub-package API changes."""


API_CHANGES["ObjectRemoved"] = [  # pyright: ignore
    "colour.algebra.matrix_dot",
]

if not is_documentation_building():
    sys.modules["colour.algebra"] = algebra(  # pyright: ignore
        sys.modules["colour.algebra"], build_API_changes(API_CHANGES)
    )

    del ModuleAPI, is_documentation_building, build_API_changes, sys
