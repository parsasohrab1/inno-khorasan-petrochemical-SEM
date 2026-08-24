"""سامانه مدیریت انرژی هوشمند (SEMS) پتروشیمی خراسان."""

import sys

# کنسول ویندوز معمولاً از codepage قدیمی (مثل cp1256) استفاده می‌کند که همه
# نویسه‌های فارسی/یونیکد را پشتیبانی نمی‌کند؛ خروجی را به UTF-8 تغییر می‌دهیم.
if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8")

__version__ = "0.1.0"
