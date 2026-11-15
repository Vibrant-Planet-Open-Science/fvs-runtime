"""Find the FVS variant libraries installed with `fvs-runtime`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

__all__ = ["library_path", "provenance", "variants"]

_HERE = Path(__file__).parent
_LIB = _HERE / "lib"
_PROVENANCE = _HERE / "provenance"
_EXT = "dll" if sys.platform == "win32" else "so"


def variants() -> list[str]:
    """Return the installed variant codes, e.g. `["ak", "bm", ...]`."""
    return sorted(
        p.name.removeprefix("FVS").removesuffix(f".{_EXT}")
        for p in _LIB.glob(f"FVS*.{_EXT}")
    )


def library_path(variant: str) -> Path:
    """Return the path to the variant's shared library (`FVS<v>.so`/`.dll`)."""
    return _existing(_LIB / f"FVS{variant.lower()}.{_EXT}", variant)


def provenance(variant: str) -> dict[str, Any]:
    """Return the variant's per-variant provenance JSON from fvs-build."""
    path = _existing(_PROVENANCE / f"FVS{variant.lower()}.json", variant)
    return json.loads(path.read_text(encoding="utf-8"))


def _existing(path: Path, variant: str) -> Path:
    if not path.is_file():
        msg = f"FVS variant {variant!r} is not in this fvs-runtime install"
        raise LookupError(msg)
    return path
