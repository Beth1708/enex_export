enex-export

A minimal, modern Python command-line application scaffold using a src/ package layout and a console script entry point.

Features
- Modern packaging with pyproject.toml (hatchling)
- src/ layout for clean imports
- Console script entry point: enex-export
- python -m enex_export module execution
- argparse-based CLI with an example hello subcommand
- Basic tests with pytest

Quick start
1) Create and activate a virtual environment.
2) Install in editable mode with dev extras: pip install -e .[dev]
3) Run the CLI: enex-export --help, enex-export --version, enex-export hello --name Beth
4) Run tests: pytest

Project structure
- pyproject.toml — project metadata, build configuration, and entry points
- src/enex_export/ — package source code
  - __init__.py — version exposure
  - cli.py — CLI implementation
  - __main__.py — allows python -m enex_export
- tests/ — pytest-based tests

License
MIT
