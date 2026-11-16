import sys

import pytest

import fvs_runtime

EXT = "dll" if sys.platform == "win32" else "so"


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """Lay out `lib/` and `provenance/` as the wheel installs them."""
    lib = tmp_path / "lib"
    prov = tmp_path / "provenance"
    lib.mkdir()
    prov.mkdir()
    for v in ("zz", "aa"):
        (lib / f"FVS{v}.{EXT}").write_bytes(b"")
        (prov / f"FVS{v}.json").write_text(f'{{"variant": "{v}"}}')
    monkeypatch.setattr(fvs_runtime, "_LIB", lib)
    monkeypatch.setattr(fvs_runtime, "_PROVENANCE", prov)
    return lib


@pytest.mark.usefixtures("installed")
def test_variants_are_sorted():
    assert fvs_runtime.variants() == ["aa", "zz"]


def test_library_path_is_case_insensitive(installed):
    path = fvs_runtime.library_path("ZZ")
    assert path == installed / f"FVSzz.{EXT}"


@pytest.mark.usefixtures("installed")
def test_provenance():
    assert fvs_runtime.provenance("zz") == {"variant": "zz"}


@pytest.mark.usefixtures("installed")
@pytest.mark.parametrize(
    "func", [fvs_runtime.library_path, fvs_runtime.provenance]
)
def test_missing_variant_raises_lookup_error(func):
    with pytest.raises(LookupError, match="'qq' is not in this fvs-runtime"):
        func("qq")
