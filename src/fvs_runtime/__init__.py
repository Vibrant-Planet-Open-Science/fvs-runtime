"""Find the FVS variant libraries installed with `fvs-runtime`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

__all__ = ["library_path", "provenance", "variants"]

_PACKAGE_PATH = Path(__file__).parent
_LIB_PATH = _PACKAGE_PATH / "lib"
_PROVENANCE_PATH = _PACKAGE_PATH / "provenance"
_EXT = "dll" if sys.platform == "win32" else "so"


def variants() -> list[str]:
    """Return the installed variant codes, e.g. `["ak", "bm", ...]`."""
    return sorted(
        lib_path.name.removeprefix("FVS").removesuffix(f".{_EXT}")
        for lib_path in _LIB_PATH.glob(f"FVS*.{_EXT}")
    )


def library_path(variant: str) -> Path:
    """Return the variant's `FVS<v>.so` path (`.dll` on Windows)."""
    return _existing(_LIB_PATH / f"FVS{variant.lower()}.{_EXT}", variant)


def provenance(variant: str) -> dict[str, Any]:
    """Return the variant's provenance JSON from fvs-build."""
    path = _existing(_PROVENANCE_PATH / f"FVS{variant.lower()}.json", variant)
    return json.loads(path.read_text(encoding="utf-8"))


def _existing(path: Path, variant: str) -> Path:
    if not path.is_file():
        msg = f"FVS variant {variant!r} is not in this fvs-runtime install"
        raise LookupError(msg)
    return path
