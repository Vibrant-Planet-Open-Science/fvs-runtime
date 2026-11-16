import sys

import pytest

import fvs_runtime

EXT = "dll" if sys.platform == "win32" else "so"


@pytest.fixture
def installed_lib_path(tmp_path, monkeypatch):
    """Lay out `lib/` and `provenance/` as the wheel installs them."""
    lib_path = tmp_path / "lib"
    provenance_path = tmp_path / "provenance"
    lib_path.mkdir()
    provenance_path.mkdir()
    for v in ("zz", "aa"):
        (lib_path / f"FVS{v}.{EXT}").write_bytes(b"")
        (provenance_path / f"FVS{v}.json").write_text(f'{{"variant": "{v}"}}')
    monkeypatch.setattr(fvs_runtime, "_LIB_PATH", lib_path)
    monkeypatch.setattr(fvs_runtime, "_PROVENANCE_PATH", provenance_path)
    return lib_path


@pytest.mark.usefixtures("installed_lib_path")
def test_variants_are_sorted():
    assert fvs_runtime.variants() == ["aa", "zz"]


def test_library_path_is_case_insensitive(installed_lib_path):
    path = fvs_runtime.library_path("ZZ")
    assert path == installed_lib_path / f"FVSzz.{EXT}"


@pytest.mark.usefixtures("installed_lib_path")
def test_provenance():
    assert fvs_runtime.provenance("zz") == {"variant": "zz"}


@pytest.mark.usefixtures("installed_lib_path")
@pytest.mark.parametrize(
    "func", [fvs_runtime.library_path, fvs_runtime.provenance]
)
def test_missing_variant_raises_lookup_error(func):
    with pytest.raises(LookupError, match="'qq' is not in this fvs-runtime"):
        func("qq")
