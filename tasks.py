"""
Invoke - Tasks
==============
"""

from __future__ import annotations

import contextlib
import fnmatch
import inspect
import os
import re
import typing
import uuid

import biblib.bib

import colour
from colour.utilities import message_box

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec  # pyright: ignore

if typing.TYPE_CHECKING:
    from invoke.context import Context

from invoke.tasks import task

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "APPLICATION_NAME",
    "APPLICATION_VERSION",
    "PYTHON_PACKAGE_NAME",
    "PYPI_PACKAGE_NAME",
    "PYPI_ARCHIVE_NAME",
    "BIBLIOGRAPHY_NAME",
    "literalise",
    "clean",
    "formatting",
    "quality",
    "precommit",
    "tests",
    "examples",
    "preflight",
    "docs",
    "todo",
    "requirements",
    "build",
    "virtualise",
    "tag",
    "release",
    "sha256",
]

APPLICATION_NAME: str = colour.__application_name__

APPLICATION_VERSION: str = colour.__version__

PYTHON_PACKAGE_NAME: str = colour.__name__

PYPI_PACKAGE_NAME: str = "colour-science"
PYPI_ARCHIVE_NAME: str = PYPI_PACKAGE_NAME.replace("-", "_")

BIBLIOGRAPHY_NAME: str = "BIBLIOGRAPHY.bib"


@task
def literalise(ctx: Context) -> None:
    """
    Write various literals in the `colour.hints` module.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box("Literalising...")
    with ctx.cd("utilities"):
        ctx.run("./literalise.py")

    ctx.run("pre-commit run --files colour/hints/__init__.py", warn=True)


@task
def clean(
    ctx: Context,
    docs: bool = True,
    bytecode: bool = False,
    pytest: bool = True,
) -> None:
    """
    Clean the project.

    Parameters
    ----------
    ctx
        Context.
    docs
        Whether to clean the *docs* directory.
    bytecode
        Whether to clean the bytecode files, e.g., *.pyc* files.
    pytest
        Whether to clean the *Pytest* cache directory.
    """

    message_box("Cleaning project...")

    patterns = ["build", "*.egg-info", "dist"]

    if docs:
        patterns.append("docs/_build")
        patterns.append("docs/generated")

    if bytecode:
        patterns.append("**/__pycache__")
        patterns.append("**/*.pyc")

    if pytest:
        patterns.append(".pytest_cache")

    for pattern in patterns:
        ctx.run(f"rm -rf {pattern}")


@task
def formatting(
    ctx: Context,
    asciify: bool = True,
    bibtex: bool = True,
) -> None:
    """
    Convert unicode characters to ASCII and cleanup the *BibTeX* file.

    Parameters
    ----------
    ctx
        Context.
    asciify
        Whether to convert unicode characters to ASCII.
    bibtex
        Whether to cleanup the *BibTeX* file.
    """

    if asciify:
        message_box("Converting unicode characters to ASCII...")
        with ctx.cd("utilities"):
            ctx.run("./unicode_to_ascii.py")

    if bibtex:
        message_box('Cleaning up "BibTeX" file...')
        bibtex_path = BIBLIOGRAPHY_NAME
        with open(bibtex_path) as bibtex_file:
            entries = biblib.bib.Parser().parse(bibtex_file.read()).get_entries()

        for entry in sorted(entries.values(), key=lambda x: x.key):
            with contextlib.suppress(KeyError):
                del entry["file"]

            for key, value in entry.items():
                entry[key] = re.sub("(?<!\\\\)\\&", "\\&", value)

        with open(bibtex_path, "w") as bibtex_file:
            for entry in sorted(entries.values(), key=lambda x: x.key):
                bibtex_file.write(entry.to_bib())
                bibtex_file.write("\n")


@task
def quality(
    ctx: Context,
    pyright: bool = True,
    rstlint: bool = True,
) -> None:
    """
    Check the codebase with *Pyright* and lints various *restructuredText*
    files with *rst-lint*.

    Parameters
    ----------
    ctx
        Context.
    pyright
        Whether to check the codebase with *Pyright*.
    rstlint
        Whether to lint various *restructuredText* files with *rst-lint*.
    """

    if pyright:
        message_box('Checking codebase with "Pyright"...')
        ctx.run("pyright --threads --skipunannotated --level warning")

    if rstlint:
        message_box('Linting "README.rst" file...')
        ctx.run("rst-lint README.rst")


@task
def precommit(ctx: Context) -> None:
    """
    Run the "pre-commit" hooks on the codebase.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Running "pre-commit" hooks on the codebase...')
    ctx.run("pre-commit run --all-files")


@task
def tests(ctx: Context) -> None:
    """
    Run the unit tests with *Pytest*.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Running "Pytest"...')
    ctx.run(
        "pytest "
        "--doctest-modules "
        f"--ignore={PYTHON_PACKAGE_NAME}/examples "
        f"--cov={PYTHON_PACKAGE_NAME} "
        f"{PYTHON_PACKAGE_NAME}"
    )


@task
def examples(ctx: Context, plots: bool = False) -> None:
    """
    Run the examples.

    Parameters
    ----------
    ctx
        Context.
    plots
        Whether to skip or only run the plotting examples: This a mutually
        exclusive switch.
    """

    message_box("Running examples...")

    for root, _dirnames, filenames in os.walk(
        os.path.join(PYTHON_PACKAGE_NAME, "examples")
    ):
        for filename in fnmatch.filter(filenames, "*.py"):
            if not plots and (
                "plotting" in root
                or "examples_contrast" in filename
                or "examples_hke" in filename
                or "examples_interpolation" in filename
            ):
                continue

            ctx.run(f"python {os.path.join(root, filename)}")


@task(formatting, quality, precommit, tests, examples)
def preflight(ctx: Context) -> None:  # noqa: ARG001
    """
    Perform the preflight tasks.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Finishing "Preflight"...')


@task
def docs(
    ctx: Context,
    plots: bool = True,
    html: bool = True,
    pdf: bool = True,
) -> None:
    """
    Build the documentation.

    Parameters
    ----------
    ctx
        Context.
    plots
        Whether to generate the documentation plots.
    html
        Whether to build the *HTML* documentation.
    pdf
        Whether to build the *PDF* documentation.
    """

    if plots:
        with ctx.cd("utilities"):
            message_box("Generating plots...")
            ctx.run("./generate_plots.py")

    with ctx.prefix("export COLOUR_SCIENCE__DOCUMENTATION_BUILD=True"), ctx.cd("docs"):
        if html:
            message_box('Building "HTML" documentation...')
            ctx.run("make html")

        if pdf:
            message_box('Building "PDF" documentation...')
            ctx.run("make latexpdf")


@task
def todo(ctx: Context) -> None:
    """
    Export the TODO items.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Exporting "TODO" items...')

    with ctx.cd("utilities"):
        ctx.run("./export_todo.py")


@task
def requirements(ctx: Context) -> None:
    """
    Export the *requirements.txt* file.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Exporting "requirements.txt" file...')
    ctx.run('uv export --no-hashes --all-extras | grep -v "-e \\." > requirements.txt')

    message_box('Exporting "docs/requirements.txt" file...')
    ctx.run(
        'uv export --no-hashes --all-extras --no-dev | grep -v "-e \\." > '
        "docs/requirements.txt"
    )


@task(literalise, clean, preflight, docs, todo, requirements)
def build(ctx: Context) -> None:
    """
    Build the project and runs dependency tasks.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box("Building...")
    if "modified:   README.rst" in ctx.run("git status").stdout:  # pyright: ignore
        error = 'Please commit your changes to the "README.rst" file!'

        raise RuntimeError(error)

    with open("README.rst") as readme_file:
        readme_content = readme_file.read()

    with open("README.rst", "w") as readme_file:
        # Adding the *Colour* logo as the first content line because the *raw*
        # directive to support light and dark theme is later trimmed.
        readme_content = (
            "..  image:: https://raw.githubusercontent.com/colour-science/"
            "colour-branding/master/images/Colour_Logo_001.png\n" + readme_content
        )
        readme_file.write(
            re.sub(
                (
                    "(\\.\\. begin-trim-long-description.*?"
                    "\\.\\. end-trim-long-description)"
                ),
                "",
                readme_content,
                flags=re.DOTALL,
            )
        )

    ctx.run("uv build")
    ctx.run("git checkout -- README.rst")
    ctx.run("twine check dist/*")


@task
def virtualise(ctx: Context, tests: bool = True) -> None:
    """
    Create a virtual environment for the project build.

    Parameters
    ----------
    ctx
        Context.
    tests
        Whether to run tests on the virtual environment.
    """

    unique_name = f"{PYPI_PACKAGE_NAME}-{uuid.uuid1()}"
    with ctx.cd("dist"):
        ctx.run(f"tar -xvf {PYPI_ARCHIVE_NAME}-{APPLICATION_VERSION}.tar.gz")
        ctx.run(f"mv {PYPI_ARCHIVE_NAME}-{APPLICATION_VERSION} {unique_name}")
        with ctx.cd(unique_name):
            ctx.run("uv sync --all-extras --no-dev")
            ctx.run(
                'uv run python -c "import imageio;imageio.plugins.freeimage.download()"'
            )
            if tests:
                ctx.run(
                    "source .venv/bin/activate && "
                    "uv run pytest "
                    "--doctest-modules "
                    f"--ignore={PYTHON_PACKAGE_NAME}/examples "
                    f"{PYTHON_PACKAGE_NAME}",
                    env={"MPLBACKEND": "AGG"},
                )


@task
def tag(ctx: Context) -> None:
    """
    Tag the repository according to defined version using *git-flow*.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box("Tagging...")
    result = ctx.run("git rev-parse --abbrev-ref HEAD", hide="both")

    if result.stdout.strip() != "develop":  # pyright: ignore
        error = "Are you still on a feature or master branch?"

        raise RuntimeError(error)

    with open(os.path.join(PYTHON_PACKAGE_NAME, "__init__.py")) as file_handle:
        file_content = file_handle.read()
        major_version = re.search(
            '__major_version__\\s+=\\s+"(.*)"', file_content
        ).group(  # pyright: ignore
            1
        )
        minor_version = re.search(
            '__minor_version__\\s+=\\s+"(.*)"', file_content
        ).group(  # pyright: ignore
            1
        )
        change_version = re.search(
            '__change_version__\\s+=\\s+"(.*)"', file_content
        ).group(  # pyright: ignore
            1
        )

        version = f"{major_version}.{minor_version}.{change_version}"

        result = ctx.run("git ls-remote --tags upstream", hide="both")
        remote_tags = result.stdout.strip().split("\n")  # pyright: ignore
        tags = set()
        for remote_tag in remote_tags:
            tags.add(remote_tag.split("refs/tags/")[1].replace("refs/tags/", "^{}"))
        version_tags = sorted(tags)
        if f"v{version}" in version_tags:
            error = (
                f'A "{PYTHON_PACKAGE_NAME}" "v{version}" tag already exists in '
                f"remote repository!"
            )

            raise RuntimeError(error)

        ctx.run(f"git flow release start v{version}")
        ctx.run(f"git flow release finish v{version}")


@task(build)
def release(ctx: Context) -> None:
    """
    Release the project to *Pypi* with *Twine*.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box("Releasing...")
    with ctx.cd("dist"):
        ctx.run("twine upload *.tar.gz")
        ctx.run("twine upload *.whl")


@task
def sha256(ctx: Context) -> None:
    """
    Compute the project *Pypi* package *sha256* with *OpenSSL*.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Computing "sha256"...')
    with ctx.cd("dist"):
        ctx.run(f"openssl sha256 {PYPI_ARCHIVE_NAME}-*.tar.gz")
