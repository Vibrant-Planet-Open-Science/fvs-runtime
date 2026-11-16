"""Map an upstream FVS release tag and revision to a wheel version."""

import re

_FS_TAG = re.compile(r"FS(\d{4})\.(\d+)(?:\.(\d+))?([a-z])?")
_PLAIN_TAG = re.compile(r"(\d{4})\.(\d+)\.(\d+)")


def wheel_version(tag: str, revision: int) -> str:
    """Return the wheel version for an upstream tag and revision.

    Args:
        tag: Upstream FVS release tag. `FSYYYY.N[.P][letter]` maps a
            letter to `P` (`a` is 1), so `FS2025.4c` is `2025.4.3`;
            `YYYY.N.P` maps directly.
        revision: fvs-runtime revision `R` of that tag: 0 for its
            first release, incremented for each repackaging of the
            same source.

    Returns:
        The version `YYYY.N.P.R`, e.g. `2025.4.3.0`.

    Raises:
        ValueError: The tag matches neither format, has both a numeric
            patch and a letter, or the revision is negative.
    """
    if revision < 0:
        msg = f"revision must be 0 or more, got {revision}"
        raise ValueError(msg)
    if m := _FS_TAG.fullmatch(tag):
        year, minor, patch, letter = m.groups()
        if patch and letter:
            msg = f"{tag!r} has both a numeric patch and a letter"
            raise ValueError(msg)
        p = ord(letter) - ord("a") + 1 if letter else int(patch or 0)
    elif m := _PLAIN_TAG.fullmatch(tag):
        year, minor, patch = m.groups()
        p = int(patch)
    else:
        msg = f"{tag!r} is not FSYYYY.N[.P][a-z] or YYYY.N.P"
        raise ValueError(msg)
    return f"{year}.{int(minor)}.{p}.{revision}"
