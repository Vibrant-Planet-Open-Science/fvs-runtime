"""Check every variant in the installed fvs-runtime against provenance.

Run with an installed wheel, not the source tree: each library must
load, and FVS's own build info must name the tag and commit that its
provenance records.
"""

import ctypes

import fvs_runtime


def build_info(variant: str) -> dict[str, str]:
    """Load a variant's library and return FVS's build info.

    Args:
        variant: Variant code, e.g. `pn`.

    Returns:
        Build-info fields by label: `Version`, `Org`, `Remote`,
        `Branch`, `Commit` and `Date`.
    """
    lib = ctypes.CDLL(fvs_runtime.library_path(variant))
    buf = ctypes.create_string_buffer(512)
    nch = ctypes.c_int()
    # FVS tags without USDAForestService/ForestVegetationSimulator#95
    # export fvsGetBuildInfo only under gfortran's mangled name.
    get_build_info = (
        getattr(lib, "fvsgetbuildinfo_", None)
        or lib["__fvsversion_MOD_fvsgetbuildinfo"]
    )
    get_build_info(buf, ctypes.byref(ctypes.c_int(len(buf))), ctypes.byref(nch))
    lines = buf.raw[: nch.value].decode().splitlines()
    return {
        label: value.strip()
        for label, value in (line.split(":", 1) for line in lines)
    }


if __name__ == "__main__":
    variants = fvs_runtime.variants()
    if not variants:
        msg = "no variants installed"
        raise SystemExit(msg)
    for variant in variants:
        info = build_info(variant)
        source = fvs_runtime.provenance(variant)["source"]
        if info["Version"] != source["ref"] or not source["sha"].startswith(
            info["Commit"]
        ):
            msg = (
                f"FVS{variant}: the library reports version"
                f" {info['Version']} at commit {info['Commit']}, but its"
                f" provenance says {source['ref']} at {source['sha']}"
            )
            raise SystemExit(msg)
