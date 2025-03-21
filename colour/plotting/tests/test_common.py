"""Define the unit tests for the :mod:`colour.plotting.common` module."""

from __future__ import annotations

import os
import shutil
import tempfile
from functools import partial

import matplotlib.font_manager
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D

import colour
from colour.colorimetry import SDS_ILLUMINANTS
from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.hints import List, cast
from colour.io import read_image
from colour.models import RGB_COLOURSPACES, XYZ_to_sRGB, gamma_function
from colour.plotting import (
    ColourSwatch,
    XYZ_to_plotting_colourspace,
    artist,
    camera,
    colour_cycle,
    colour_style,
    filter_cmfs,
    filter_colour_checkers,
    filter_illuminants,
    filter_passthrough,
    filter_RGB_colourspaces,
    font_scaling,
    label_rectangles,
    override_style,
    plot_image,
    plot_multi_colour_swatches,
    plot_multi_functions,
    plot_single_colour_swatch,
    plot_single_function,
    render,
    uniform_axes3d,
    update_settings_collection,
)
from colour.utilities import attest

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestColourStyle",
    "TestOverrideStyle",
    "TestFontScaling",
    "TestXYZToPlottingColourspace",
    "TestColourCycle",
    "TestArtist",
    "TestCamera",
    "TestRender",
    "TestLabelRectangles",
    "TestUniformAxes3d",
    "TestFilterPassthrough",
    "TestFilterRgbColourspaces",
    "TestFilterCmfs",
    "TestFilterIlluminants",
    "TestFilterColourCheckers",
    "TestUpdateSettingsCollection",
    "TestPlotSingleColourSwatch",
    "TestPlotMultiColourSwatches",
    "TestPlotSingleFunction",
    "TestPlotMultiFunctions",
    "TestPlotImage",
]


class TestColourStyle:
    """
    Define :func:`colour.plotting.common.colour_style` definition unit tests
    methods.
    """

    def test_colour_style(self) -> None:
        """Test :func:`colour.plotting.common.colour_style` definition."""

        assert isinstance(colour_style(use_style=False), dict)


class TestOverrideStyle:
    """
    Define :func:`colour.plotting.common.override_style` definition unit tests
    methods.
    """

    def test_override_style(self) -> None:
        """Test :func:`colour.plotting.common.override_style` definition."""

        text_color = plt.rcParams["text.color"]
        try:

            @override_style(**{"text.color": "red"})
            def test_text_color_override() -> None:
                """Test :func:`colour.plotting.common.override_style` definition."""

                attest(plt.rcParams["text.color"] == "red")

            test_text_color_override()
        finally:
            plt.rcParams["text.color"] = text_color


class TestFontScaling:
    """
    Define :func:`colour.plotting.common.font_scaling` definition unit tests
    methods.
    """

    def test_font_scaling(self) -> None:
        """Test :func:`colour.plotting.common.font_scaling` definition."""

        with font_scaling("medium-colour-science", 2):
            assert matplotlib.font_manager.font_scalings["medium-colour-science"] == 2

        assert matplotlib.font_manager.font_scalings["medium-colour-science"] == 1


class TestXYZToPlottingColourspace:
    """
    Define :func:`colour.plotting.common.XYZ_to_plotting_colourspace`
    definition unit tests methods.
    """

    def test_XYZ_to_plotting_colourspace(self) -> None:
        """
        Test :func:`colour.plotting.common.XYZ_to_plotting_colourspace`
        definition.
        """

        XYZ = np.random.random(3)
        np.testing.assert_allclose(
            XYZ_to_sRGB(XYZ),
            XYZ_to_plotting_colourspace(XYZ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestColourCycle:
    """
    Define :func:`colour.plotting.common.colour_cycle` definition unit tests
    methods.
    """

    def test_colour_cycle(self) -> None:
        """Test :func:`colour.plotting.common.colour_cycle` definition."""

        cycler = colour_cycle()

        np.testing.assert_allclose(
            next(cycler),
            np.array([0.95686275, 0.26274510, 0.21176471, 1.00000000]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            next(cycler),
            np.array([0.61582468, 0.15423299, 0.68456747, 1.00000000]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            next(cycler),
            np.array([0.25564014, 0.31377163, 0.70934256, 1.00000000]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        cycler = colour_cycle(colour_cycle_map="viridis")

        np.testing.assert_allclose(
            next(cycler),
            np.array([0.26700400, 0.00487400, 0.32941500, 1.00000000]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestArtist:
    """
    Define :func:`colour.plotting.common.artist` definition unit tests
    methods.
    """

    def test_artist(self) -> None:
        """Test :func:`colour.plotting.common.artist` definition."""

        figure_1 = plt.figure()
        axes = figure_1.subfigures().subfigures().gca()  # pyright: ignore

        figure_2, _axes = artist(axes=axes)

        assert figure_1 is figure_2

        plt.figure()

        figure_2, _axes = artist(axes=axes)
        assert figure_1 is figure_2

        figure_1, axes_1 = artist()

        assert isinstance(figure_1, Figure)
        assert isinstance(axes_1, Axes)

        _figure_2, axes_2 = artist(axes=axes_1, uniform=True)
        assert axes_1 is axes_2

        figure_3, _axes_3 = artist(uniform=True)
        assert figure_3.get_figwidth() == figure_3.get_figheight()


class TestCamera:
    """
    Define :func:`colour.plotting.common.camera` definition unit tests
    methods.
    """

    def test_camera(self) -> None:
        """Test :func:`colour.plotting.common.camera` definition."""

        figure, _axes = artist()
        axes = figure.add_subplot(111, projection="3d")

        _figure, axes = camera(axes=axes, elevation=45, azimuth=90)

        assert axes.elev == 45
        assert axes.azim == 90


class TestRender:
    """
    Define :func:`colour.plotting.common.render` definition unit tests
    methods.
    """

    def setup_method(self) -> None:
        """Initialise the common tests attributes."""

        self._temporary_directory = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        """After tests actions."""

        shutil.rmtree(self._temporary_directory)

    def test_render(self) -> None:
        """Test :func:`colour.plotting.common.render` definition."""

        figure, axes = artist()

        render(
            figure=figure,
            axes=axes,
            standalone=False,
            aspect="equal",
            axes_visible=True,
            bounding_box=[0, 1, 0, 1],
            tight_layout=False,
            legend=True,
            legend_columns=2,
            transparent_background=False,
            title="Render Unit Test",
            wrap_title=True,
            x_label="x Label",
            y_label="y Label",
            x_ticker=False,
            y_ticker=False,
        )

        render(standalone=True)

        render(
            filename=os.path.join(self._temporary_directory, "render.png"),
            axes_visible=False,
        )


class TestLabelRectangles:
    """
    Define :func:`colour.plotting.common.label_rectangles` definition unit
    tests methods.
    """

    def test_label_rectangles(self) -> None:
        """Test :func:`colour.plotting.common.label_rectangles` definition."""

        figure, axes = artist()

        samples = np.linspace(0, 1, 10)

        _figure, axes = label_rectangles(
            cast(List[float], samples.tolist()),
            axes.bar(samples, 1),
            figure=figure,
            axes=axes,
        )

        assert len(axes.texts) == len(samples)


class TestUniformAxes3d:
    """
    Define :func:`colour.plotting.common.uniform_axes3d` definition unit tests
    methods.
    """

    def test_uniform_axes3d(self) -> None:
        """Test :func:`colour.plotting.common.uniform_axes3d` definition."""

        figure, _axes = artist()
        axes = cast(Axes3D, figure.add_subplot(111, projection="3d"))

        uniform_axes3d(axes=axes)

        assert axes.get_xlim() == axes.get_ylim()
        assert axes.get_xlim() == axes.get_zlim()


class TestFilterPassthrough:
    """
    Define :func:`colour.plotting.common.filter_passthrough` definition unit
    tests methods.
    """

    def test_filter_passthrough(self) -> None:
        """Test :func:`colour.plotting.common.filter_passthrough` definition."""

        assert sorted(
            colourspace.name
            for colourspace in filter_passthrough(
                RGB_COLOURSPACES, ["ACES2065-1"]
            ).values()
        ) == ["ACES2065-1"]

        assert sorted(filter_passthrough(RGB_COLOURSPACES, ["aces2065-1"]).keys()) == [
            "ACES2065-1"
        ]

        assert sorted(filter_passthrough(RGB_COLOURSPACES, ["aces20651"]).keys()) == [
            "ACES2065-1"
        ]

        assert filter_passthrough(
            SDS_ILLUMINANTS,
            [SDS_ILLUMINANTS["D65"], {"Is": "Excluded"}],
            allow_non_siblings=False,
        ) == {"D65": SDS_ILLUMINANTS["D65"]}

        assert filter_passthrough(
            SDS_ILLUMINANTS,
            [SDS_ILLUMINANTS["D65"], {"Is": "Included"}],
            allow_non_siblings=True,
        ) == {"D65": SDS_ILLUMINANTS["D65"], "Is": "Included"}

        assert sorted(
            element
            for element in filter_passthrough(
                {"John": "Doe", "Luke": "Skywalker"}, ["John"]
            ).values()
        ) == ["Doe", "John"]


class TestFilterRgbColourspaces:
    """
    Define :func:`colour.plotting.common.filter_RGB_colourspaces` definition
    unit tests methods.
    """

    def test_filter_RGB_colourspaces(self) -> None:
        """
        Test :func:`colour.plotting.common.filter_RGB_colourspaces`
        definition.
        """

        assert sorted(
            colourspace.name
            for colourspace in filter_RGB_colourspaces(["ACES2065-1"]).values()
        ) == ["ACES2065-1"]


class TestFilterCmfs:
    """
    Define :func:`colour.plotting.common.filter_cmfs` definition unit tests
    methods.
    """

    def test_filter_cmfs(self) -> None:
        """Test :func:`colour.plotting.common.filter_cmfs` definition."""

        assert sorted(
            cmfs.name
            for cmfs in filter_cmfs(["CIE 1931 2 Degree Standard Observer"]).values()
        ) == [
            "CIE 1931 2 Degree Standard Observer",
        ]


class TestFilterIlluminants:
    """
    Define :func:`colour.plotting.common.filter_illuminants` definition unit
    tests methods.
    """

    def test_filter_illuminants(self) -> None:
        """Test :func:`colour.plotting.common.filter_illuminants` definition."""

        assert sorted(filter_illuminants(["D50"]).keys()) == ["D50"]


class TestFilterColourCheckers:
    """
    Define :func:`colour.plotting.common.filter_colour_checkers` definition
    unit tests methods.
    """

    def test_filter_colour_checkers(self) -> None:
        """Test :func:`colour.plotting.common.filter_colour_checkers` definition."""

        assert sorted(
            colour_checker.name
            for colour_checker in filter_colour_checkers(
                ["ColorChecker24 - After November 2014"]
            ).values()
        ) == [
            "ColorChecker24 - After November 2014",
        ]


class TestUpdateSettingsCollection:
    """
    Define :func:`colour.plotting.common.update_settings_collection`
    definition unit tests methods.
    """

    def test_update_settings_collection(self) -> None:
        """
        Test :func:`colour.plotting.common.update_settings_collection`
        definition.
        """

        settings_collection = [{1: 2}, {3: 4}]
        keyword_arguments = {5: 6}
        update_settings_collection(settings_collection, keyword_arguments, 2)
        assert settings_collection == [{1: 2, 5: 6}, {3: 4, 5: 6}]

        settings_collection = [{1: 2}, {3: 4}]
        keyword_arguments = [{5: 6}, {7: 8}]
        update_settings_collection(settings_collection, keyword_arguments, 2)
        assert settings_collection == [{1: 2, 5: 6}, {3: 4, 7: 8}]


class TestPlotSingleColourSwatch:
    """
    Define :func:`colour.plotting.common.plot_single_colour_swatch` definition
    unit tests methods.
    """

    def test_plot_single_colour_swatch(self) -> None:
        """
        Test :func:`colour.plotting.common.plot_single_colour_swatch`
        definition.
        """

        figure, axes = plot_single_colour_swatch(
            ColourSwatch((0.45620519, 0.03081071, 0.04091952))
        )

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)

        figure, axes = plot_single_colour_swatch(
            np.array([0.45620519, 0.03081071, 0.04091952])
        )

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)


class TestPlotMultiColourSwatches:
    """
    Define :func:`colour.plotting.common.plot_multi_colour_swatches`
    definition unit tests methods.
    """

    def test_plot_multi_colour_swatches(self) -> None:
        """
        Test :func:`colour.plotting.common.plot_multi_colour_swatches`
        definition.
        """

        figure, axes = plot_multi_colour_swatches(
            [
                ColourSwatch((0.45293517, 0.31732158, 0.26414773)),
                ColourSwatch((0.77875824, 0.57726450, 0.50453169)),
            ]
        )

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)

        figure, axes = plot_multi_colour_swatches(
            np.array(
                [
                    [0.45293517, 0.31732158, 0.26414773],
                    [0.77875824, 0.57726450, 0.50453169],
                ]
            ),
            direction="-y",
        )

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)


class TestPlotSingleFunction:
    """
    Define :func:`colour.plotting.common.plot_single_function` definition unit
    tests methods.
    """

    def test_plot_single_function(self) -> None:
        """Test :func:`colour.plotting.common.plot_single_function` definition."""

        figure, axes = plot_single_function(partial(gamma_function, exponent=1 / 2.2))

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)


class TestPlotMultiFunctions:
    """
    Define :func:`colour.plotting.common.plot_multi_functions` definition unit
    tests methods.
    """

    def test_plot_multi_functions(self) -> None:
        """Test :func:`colour.plotting.common.plot_multi_functions` definition."""

        functions = {
            "Gamma 2.2": lambda x: x ** (1 / 2.2),
            "Gamma 2.4": lambda x: x ** (1 / 2.4),
            "Gamma 2.6": lambda x: x ** (1 / 2.6),
        }
        plot_kwargs = {"c": "r"}
        figure, axes = plot_multi_functions(functions, plot_kwargs=plot_kwargs)

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)

        plot_kwargs = [{"c": "r"}, {"c": "g"}, {"c": "b"}]
        figure, axes = plot_multi_functions(
            functions, log_x=10, log_y=10, plot_kwargs=plot_kwargs
        )

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)

        figure, axes = plot_multi_functions(functions, log_x=10)

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)

        figure, axes = plot_multi_functions(functions, log_y=10)

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)


class TestPlotImage:
    """
    Define :func:`colour.plotting.common.plot_image` definition unit tests
    methods.
    """

    def test_plot_image(self) -> None:
        """Test :func:`colour.plotting.common.plot_image` definition."""

        path = os.path.join(
            colour.__path__[0],  # pyright: ignore
            "..",
            "docs",
            "_static",
            "Logo_Medium_001.png",
        )

        # Distribution does not ship the documentation thus we are skipping
        # this unit test if the image does not exist.
        if not os.path.exists(path):  # pragma: no cover
            return

        figure, axes = plot_image(read_image(path))

        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)
