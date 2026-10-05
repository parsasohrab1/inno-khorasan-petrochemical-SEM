"""Smart Energy Management System (SEMS) for Khorasan Petrochemical."""

import sys

# The Windows console usually uses an old codepage (such as cp1256) that does not support all
# Persian/Unicode characters; we switch the output to UTF-8.
if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8")

__version__ = "0.1.0"
