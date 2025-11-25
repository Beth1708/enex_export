import re
import sys
from enex_export import __version__
from enex_export.cli import _main, build_parser


def run(argv):
    # Capture stdout
    from io import StringIO
    old_out = sys.stdout
    try:
        buf = StringIO()
        sys.stdout = buf
        code = _main(argv)
        return code, buf.getvalue()
    finally:
        sys.stdout = old_out


def test_help_shows_usage():
    parser = build_parser()
    help_text = parser.format_help()
    assert "usage:" in help_text.lower()
    assert "enex-export" in help_text


def test_version_flag_prints_version_and_exits_zero():
    code, out = run(["--version"])
    assert code == 0
    # strip to be resilient to trailing newline
    assert out.strip() == __version__


def test_hello_default():
    code, out = run(["hello"])
    assert code == 0
    assert out.strip() == "Hello, world!"


def test_hello_with_name():
    code, out = run(["hello", "--name", "Beth"]) 
    assert code == 0
    assert out.strip() == "Hello, Beth!"
