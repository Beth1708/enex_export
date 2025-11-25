"""enex_export package.

This package provides a command-line interface (CLI) entry point for the
enex-export tool. At this stage, it ships as a scaffold with a sample
subcommand to illustrate the recommended structure.
"""

from importlib.metadata import version, PackageNotFoundError

__all__ = ["__version__"]


def _detect_version():
    try:
        return version("enex-export")
    except PackageNotFoundError:
        # Fallback for editable installs or running from source without build
        return "0.1.0"


__version__ = _detect_version()
