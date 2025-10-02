"""
Compatibility shim for Python 3.13 removal of stdlib imghdr.
Provides a minimal `what(file, h=None)` function.

If Pillow is available, it uses Pillow to detect image type.
If not, it falls back to a very small magic-bytes check for common types.
"""

from __future__ import annotations

from typing import Optional, Union

try:
    from PIL import Image
except Exception:  # Pillow not installed or failing
    Image = None  # type: ignore


_MAGIC_PREFIXES = [
    (b"\xFF\xD8\xFF", "jpeg"),   # JPEG
    (b"\x89PNG\r\n\x1a\n", "png"),  # PNG
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"BM", "bmp"),
    (b"II*\x00", "tiff"),
    (b"MM\x00*", "tiff"),
    (b"RIFF", "webp"),  # Needs further check, but good enough for fallback
]


def what(file: Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"], h: Optional[bytes] = None) -> Optional[str]:
    """Return image type for given file or header bytes.

    Parameters
    - file: path to file (str or PathLike). Ignored if h is provided.
    - h: optional header bytes; if provided, detection runs on these bytes.
    """
    if Image is not None:
        try:
            if h is None:
                with Image.open(file) as img:  # type: ignore[arg-type]
                    fmt = (img.format or "").lower()
                    return fmt or None
            else:
                # Use Pillow's frombytes requires size; instead use BytesIO
                from io import BytesIO
                with Image.open(BytesIO(h)) as img:
                    fmt = (img.format or "").lower()
                    return fmt or None
        except Exception:
            pass

    # Fallback magic-bytes detection
    data: Optional[bytes] = h
    if data is None:
        try:
            with open(file, "rb") as f:  # type: ignore[arg-type]
                data = f.read(16)
        except Exception:
            return None

    for prefix, label in _MAGIC_PREFIXES:
        if data.startswith(prefix):
            return label
    return None




